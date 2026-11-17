---
applyTo: "**/*.sql"
---
# T-SQL para el SQL analytics endpoint del Lakehouse

- Los archivos de `sql/` son T-SQL, NO Spark SQL. No uses backticks, LIMIT,
  USING DELTA, DESCRIBE ni comandos %%sql en estos archivos.
- Antes de ejecutar, confirma el endpoint y descubre tablas/columnas con
  INFORMATION_SCHEMA. `dbo` es el esquema previsto, no una prueba del esquema real.
- Mantente en solo lectura: SELECT y CTE. No generes CREATE, INSERT, UPDATE,
  DELETE, MERGE, DROP, TRUNCATE ni GRANT para este ejercicio.
- Usa `TOP (N)` y `ORDER BY` para muestras; selecciona columnas explicitas.
  No uses GO ni comandos de sqlcmd en lotes enviados mediante MCP.
- Usa decimal(18,2), no float o money, para ingresos. Redondea por linea y luego suma.
- Evita duplicar ingresos por joins: comprueba unicidad de las dimensiones.
  Quita copias exactas; detecta versiones distintas de un sale_id y detente.
- Las cancelaciones no son errores de calidad, pero no producen ingresos.
  No rechaces una venta recuperable por category_raw/city_raw nulos.
- Un SQL analytics endpoint puede tardar en sincronizar tablas recien escritas.
  No intentes arreglarlo escribiendo tablas base desde T-SQL.
- Si no hay herramientas conectadas, entrega el SQL como propuesta y declara
  que no se ha ejecutado. Nunca inventes resultados.
