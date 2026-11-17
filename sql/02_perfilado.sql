-- Una consulta por seleccion si el cliente solo devuelve el ultimo resultado.
SELECT
    COUNT_BIG(*) AS raw_rows,
    COUNT(DISTINCT sale_id) AS unique_sales,
    COUNT_BIG(*) - COUNT(DISTINCT sale_id) AS extra_duplicate_rows,
    SUM(CASE WHEN category_raw IS NULL THEN CAST(1 AS bigint) ELSE 0 END) AS null_category_rows,
    SUM(CASE WHEN city_raw IS NULL THEN CAST(1 AS bigint) ELSE 0 END) AS null_city_rows,
    SUM(CASE WHEN quantity <= 0 THEN CAST(1 AS bigint) ELSE 0 END) AS invalid_quantity_rows,
    SUM(CASE WHEN status = 'cancelled' THEN CAST(1 AS bigint) ELSE 0 END) AS cancelled_rows
FROM dbo.workshop_sales_raw;

SELECT
    COUNT_BIG(*) AS orphan_product_rows
FROM dbo.workshop_sales_raw AS s
LEFT JOIN dbo.workshop_products AS p ON s.product_id = p.product_id
WHERE p.product_id IS NULL;

SELECT TOP (10)
    sale_id,
    sale_date,
    product_id,
    quantity,
    category_raw,
    city_raw
FROM dbo.workshop_sales_raw
WHERE category_raw IS NULL OR city_raw IS NULL OR quantity <= 0
ORDER BY sale_id, product_id, quantity;
