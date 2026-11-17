"""Reference solution: exact deduplication, canonical dimensions and decimal revenue."""


def clean_sales(sales_raw, products, stores):
    from pyspark.sql import functions as F

    for frame, key in ((products, "product_id"), (stores, "store_id")):
        if frame.filter(F.col(key).isNull()).limit(1).count():
            raise ValueError(f"La dimension contiene una clave nula: {key}")
        if frame.groupBy(key).count().filter(F.col("count") > 1).limit(1).count():
            raise ValueError(f"La dimension contiene claves duplicadas: {key}")

    deduplicated = sales_raw.dropDuplicates()
    if deduplicated.filter(F.col("sale_id").isNull()).limit(1).count():
        raise ValueError("Hay sale_id nulos. Revisa los datos antes de continuar.")
    if deduplicated.groupBy("sale_id").count().filter(F.col("count") > 1).limit(1).count():
        raise ValueError("Hay sale_id repetidos con contenido diferente. No se elige uno al azar.")

    eligible = deduplicated.filter((F.col("quantity") > 0) & (F.col("status") == "completed"))
    enriched = eligible.join(products.select("product_id", "category"), "product_id", "inner").join(
        stores.select("store_id", "city"), "store_id", "inner"
    )
    return enriched.select(
        "sale_id",
        "sale_date",
        "product_id",
        "store_id",
        "channel",
        "quantity",
        "unit_price",
        "discount_rate",
        "status",
        "category",
        "city",
        F.round(F.col("quantity") * F.col("unit_price") * (F.lit(1) - F.col("discount_rate")), 2)
        .cast("decimal(18,2)")
        .alias("net_amount"),
    )
