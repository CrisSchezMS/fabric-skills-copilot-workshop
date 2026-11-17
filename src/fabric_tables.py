"""Fabric notebook helpers. Uses the existing notebook Spark session."""

import re

TABLE_NAMES = {
    "products": "workshop_products",
    "stores": "workshop_stores",
    "sales_raw": "workshop_sales_raw",
}


def table_names(schema):
    if not isinstance(schema, str) or (
        schema and not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", schema)
    ):
        raise ValueError("SCHEMA debe ser un identificador simple o una cadena vacia.")
    prefix = f"`{schema}`." if schema else ""
    return {key: f"{prefix}`{value}`" for key, value in TABLE_NAMES.items()}


def require_default_lakehouse(context):
    if not context.get("defaultLakehouseId"):
        raise RuntimeError(
            "Adjunta un Lakehouse como predeterminado al notebook y reinicia la sesion Spark."
        )


def create_dataframes(spark, data):
    from pyspark.sql import types as T

    schemas = {
        "products": T.StructType(
            [
                T.StructField("product_id", T.IntegerType(), False),
                T.StructField("product_name", T.StringType(), False),
                T.StructField("category", T.StringType(), False),
                T.StructField("list_price", T.DecimalType(18, 2), False),
            ]
        ),
        "stores": T.StructType(
            [
                T.StructField("store_id", T.IntegerType(), False),
                T.StructField("store_name", T.StringType(), False),
                T.StructField("city", T.StringType(), False),
            ]
        ),
        "sales_raw": T.StructType(
            [
                T.StructField("sale_id", T.StringType(), False),
                T.StructField("sale_date", T.DateType(), False),
                T.StructField("product_id", T.IntegerType(), False),
                T.StructField("store_id", T.IntegerType(), False),
                T.StructField("channel", T.StringType(), False),
                T.StructField("quantity", T.IntegerType(), False),
                T.StructField("unit_price", T.DecimalType(18, 2), False),
                T.StructField("discount_rate", T.DecimalType(4, 2), False),
                T.StructField("status", T.StringType(), False),
                T.StructField("category_raw", T.StringType(), True),
                T.StructField("city_raw", T.StringType(), True),
            ]
        ),
    }
    return {key: spark.createDataFrame(data[key], schema) for key, schema in schemas.items()}


def write_tables(spark, frames, schema, allow_overwrite=False):
    if type(allow_overwrite) is not bool:
        raise ValueError("ALLOW_OVERWRITE debe ser True o False.")
    names = table_names(schema)
    if set(frames) != set(names):
        raise ValueError("Se requieren exactamente products, stores y sales_raw.")
    if schema:
        spark.sql(f"SHOW TABLES IN `{schema}`").limit(1).collect()
    existing = [name for name in names.values() if spark.catalog.tableExists(name)]
    if existing and not allow_overwrite:
        raise FileExistsError(
            "No se ha escrito ninguna tabla. Ya existen: "
            + ", ".join(existing)
            + ". Usa otro Lakehouse o revisa ALLOW_OVERWRITE."
        )
    mode = "overwrite" if allow_overwrite else "errorifexists"
    for key, name in names.items():
        writer = frames[key].write.format("delta").mode(mode)
        if allow_overwrite:
            writer = writer.option("overwriteSchema", "true")
        writer.saveAsTable(name)
    counts = {key: spark.table(name).count() for key, name in names.items()}
    for key, actual in counts.items():
        expected = frames[key].count()
        if actual != expected:
            raise RuntimeError(f"Recuento incorrecto en {names[key]}: {actual} != {expected}")
    return counts
