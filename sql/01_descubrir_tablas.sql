-- Ejecutar en el SQL analytics endpoint del Lakehouse del taller.
-- Confirmar el esquema real antes de usar los otros ejemplos.
SELECT
    TABLE_SCHEMA AS table_schema,
    TABLE_NAME AS table_name,
    COLUMN_NAME AS column_name,
    DATA_TYPE AS data_type,
    NUMERIC_PRECISION AS numeric_precision,
    NUMERIC_SCALE AS numeric_scale
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN ('workshop_products', 'workshop_stores', 'workshop_sales_raw')
ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION;
