-- Estos tres resultados deben estar vacios ANTES de ejecutar el resumen.
-- No se elige una version arbitraria de una venta con contenido diferente.
WITH exact_sales AS (
    SELECT DISTINCT
        sale_id, sale_date, product_id, store_id, channel, quantity,
        unit_price, discount_rate, status, category_raw, city_raw
    FROM dbo.workshop_sales_raw
)
SELECT TOP (20)
    sale_id,
    COUNT_BIG(*) AS different_versions
FROM exact_sales
GROUP BY sale_id
HAVING COUNT_BIG(*) > 1 OR sale_id IS NULL
ORDER BY sale_id;

SELECT TOP (20)
    product_id,
    COUNT_BIG(*) AS key_count
FROM dbo.workshop_products
GROUP BY product_id
HAVING COUNT_BIG(*) > 1 OR product_id IS NULL
ORDER BY product_id;

SELECT TOP (20)
    store_id,
    COUNT_BIG(*) AS key_count
FROM dbo.workshop_stores
GROUP BY store_id
HAVING COUNT_BIG(*) > 1 OR store_id IS NULL
ORDER BY store_id;
