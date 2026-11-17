"""Schema-first profiling with separate raw-row and distinct-line counters."""


def profile_sales(frames, expected_frames):
    from pyspark.sql import functions as F

    if set(frames) != set(expected_frames):
        raise ValueError("Las tablas de origen no coinciden con el contrato.")
    for key, frame in frames.items():
        actual = {field.name: field.dataType for field in frame.schema.fields}
        expected = {field.name: field.dataType for field in expected_frames[key].schema.fields}
        if actual != expected:
            raise ValueError(f"Esquema distinto del contrato: {key}")

    raw = frames["sales_raw"]
    unique = raw.dropDuplicates()
    raw_rows = raw.count()
    unique_rows = unique.count()

    def incidents(frame):
        counts = frame.agg(
            *[F.count(F.when(F.col(column).isNull(), 1)).alias(column) for column in frame.columns],
            F.count(F.when(F.col("quantity").isNull() | (F.col("quantity") <= 0), 1)).alias(
                "invalid_quantity_rows"
            ),
        ).first()
        return {
            "nulls": {column: counts[column] for column in frame.columns},
            "invalid_quantity_rows": counts.invalid_quantity_rows,
            "orphan_product_rows": frame.join(
                frames["products"].select("product_id").distinct(), "product_id", "left_anti"
            ).count(),
            "orphan_store_rows": frame.join(
                frames["stores"].select("store_id").distinct(), "store_id", "left_anti"
            ).count(),
        }

    return {
        "raw_rows": raw_rows,
        "distinct_sale_ids": raw.select("sale_id")
        .where(F.col("sale_id").isNotNull())
        .distinct()
        .count(),
        "exact_copies": raw_rows - unique_rows,
        "distinct_contents": unique_rows,
        "conflicting_sale_ids": unique.where(F.col("sale_id").isNotNull())
        .groupBy("sale_id")
        .count()
        .filter(F.col("count") > 1)
        .count(),
        "raw_incidents": incidents(raw),
        "deduplicated_incidents": incidents(unique),
    }
