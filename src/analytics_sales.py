"""Analytics outputs deployed separately from the unchanged raw-data generator."""

from datetime import date
from re import fullmatch

ANALYTICS_TABLE_NAMES = {
    "sales_clean": "workshop_sales_clean",
    "sales_daily": "workshop_sales_daily",
    "calendar": "workshop_calendar",
}


def analytics_table_names(schema):
    if not isinstance(schema, str) or (schema and not fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", schema)):
        raise ValueError("SCHEMA debe ser un identificador simple o una cadena vacia.")
    prefix = f"`{schema}`." if schema else ""
    return {key: f"{prefix}`{value}`" for key, value in ANALYTICS_TABLE_NAMES.items()}


def build_analytics_frames(sales_clean):
    from pyspark.sql import functions as F

    required = (
        "sale_id",
        "sale_date",
        "product_id",
        "store_id",
        "channel",
        "quantity",
        "net_amount",
        "category",
        "city",
    )
    invalid = F.col("status").isNull() | (F.col("status") != "completed")
    for column in required:
        invalid = invalid | F.col(column).isNull()
    invalid = invalid | (F.col("quantity") <= 0)
    if sales_clean.filter(invalid).limit(1).count():
        raise ValueError("La entrada limpia contiene nulos o lineas no elegibles.")
    if sales_clean.groupBy("sale_id").count().filter(F.col("count") > 1).limit(1).count():
        raise ValueError("La entrada limpia contiene sale_id repetidos.")

    bounds = sales_clean.agg(
        F.min("sale_date").alias("start"), F.max("sale_date").alias("end")
    ).first()
    if bounds.start is None:
        raise ValueError("No hay ventas limpias; no se publican tablas vacias.")
    calendar = (
        sales_clean.sparkSession.range(1)
        .select(
            F.explode(
                F.sequence(
                    F.lit(date(bounds.start.year, 1, 1)),
                    F.lit(date(bounds.end.year, 12, 31)),
                )
            ).alias("calendar_date")
        )
        .select(
            "calendar_date",
            F.year("calendar_date").alias("calendar_year"),
            F.quarter("calendar_date").alias("calendar_quarter"),
            F.month("calendar_date").alias("month_number"),
            F.date_format("calendar_date", "yyyy-MM").alias("year_month"),
        )
    )
    daily = sales_clean.groupBy("sale_date", "product_id", "store_id", "channel").agg(
        F.count("*").alias("sales_count"),
        F.sum("quantity").alias("units"),
        F.sum("net_amount").cast("decimal(38,2)").alias("net_revenue"),
    )
    return {"sales_clean": sales_clean, "sales_daily": daily, "calendar": calendar}


def validate_analytics_frames(frames):
    from pyspark.sql import functions as F

    clean = (
        frames["sales_clean"]
        .agg(
            F.count("*").alias("lines"),
            F.sum("quantity").alias("units"),
            F.sum("net_amount").alias("revenue"),
        )
        .first()
    )
    daily = (
        frames["sales_daily"]
        .agg(
            F.sum("sales_count").alias("lines"),
            F.sum("units").alias("units"),
            F.sum("net_revenue").alias("revenue"),
        )
        .first()
    )
    if tuple(clean) != tuple(daily):
        raise ValueError("El agregado diario no reconcilia con el detalle limpio.")
    return {"clean_rows": clean.lines, "units": clean.units, "net_revenue": clean.revenue}


def write_analytics_tables(spark, frames, schema, approved=False):
    if approved is not True:
        raise PermissionError("La publicacion requiere un alcance de despliegue aprobado.")
    names = analytics_table_names(schema)
    if set(frames) != set(names):
        raise ValueError("Se requieren exactamente sales_clean, sales_daily y calendar.")
    if schema:
        spark.sql(f"SHOW TABLES IN `{schema}`").limit(1).count()
    existing = [name for name in names.values() if spark.catalog.tableExists(name)]
    if existing:
        raise FileExistsError(
            "No se ha escrito ninguna tabla. Ya existen: "
            + ", ".join(existing)
            + ". No se permite sobrescribir; revisa el destino."
        )
    expected = validate_analytics_frames(frames)
    expected_counts = {key: frame.count() for key, frame in frames.items()}
    for key, name in names.items():
        frames[key].write.format("delta").mode("errorifexists").saveAsTable(name)
    saved = {key: spark.table(name) for key, name in names.items()}
    for key, frame in saved.items():
        if frame.count() != expected_counts[key]:
            raise RuntimeError(f"Recuento incorrecto tras publicar {names[key]}.")
    if validate_analytics_frames(saved) != expected:
        raise RuntimeError("Los totales publicados no coinciden con la entrada.")
    return expected
