-- Ejecutar SOLO despues de comprobar que sql/03_validar_claves.sql no devuelve filas.
-- Solucion T-SQL de solo lectura; no crea ni modifica tablas.
WITH exact_sales AS (
    SELECT DISTINCT
        sale_id, sale_date, product_id, store_id, channel, quantity,
        unit_price, discount_rate, status, category_raw, city_raw
    FROM dbo.workshop_sales_raw
),
clean_sales AS (
    SELECT
        s.sale_id,
        s.quantity,
        p.category,
        CAST(
            ROUND(s.quantity * s.unit_price * (1 - s.discount_rate), 2)
            AS decimal(18, 2)
        ) AS net_amount
    FROM exact_sales AS s
    INNER JOIN dbo.workshop_products AS p ON s.product_id = p.product_id
    INNER JOIN dbo.workshop_stores AS t ON s.store_id = t.store_id
    WHERE s.status = 'completed' AND s.quantity > 0
)
SELECT
    category,
    COUNT_BIG(*) AS sales_count,
    SUM(quantity) AS units,
    SUM(net_amount) AS net_revenue
FROM clean_sales
GROUP BY category
ORDER BY net_revenue DESC, category;
