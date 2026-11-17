---
applyTo: "src/**/*.py,notebooks/**/*.ipynb,soluciones/**/*.ipynb"
---
# PySpark y Fabric

- En las celdas usa la sesion `spark` que proporciona Fabric. No crees otra
  SparkSession, no anadas `__main__` ni instales paquetes para esta demo.
- Conserva los esquemas explicitos: claves enteras, fecha `date`, importes
  `decimal(18,2)` y descuento `decimal(4,2)`.
- Usa funciones nativas de Spark y joins; evita UDFs, collect() de ventas y pandas
  para las transformaciones. El generador Python es intencionadamente pequeno:
  no lo presentes como generador distribuido para millones de filas.
- Comprueba Lakehouse predeterminado y esquema. `dbo` es la configuracion para
  Lakehouses con esquemas; una cadena vacia corresponde al modo sin esquemas.
  No crees esquemas para intentar corregir un destino desconocido.
- No mezcles rutas de Files/OneLake con identificadores de tablas.
- Guarda con `format("delta")`. Conserva la comprobacion previa de TODAS las
  tablas y `errorifexists`; overwrite solo con consentimiento explicito.
- Usa `notebookutils`, no APIs inventadas. No anadas REST ni credenciales si la
  tarea se resuelve con el Lakehouse predeterminado.
- No cambies los datos raw para ocultar incidencias. Separa perfilado y limpieza.
- Las tablas derivadas siguen `docs/contrato-analitico.md`. El notebook
  desplegado publica al ejecutarse tras aprobar el alcance; no permite overwrite.
  Los helpers de bajo nivel requieren `approved=True` desde ese flujo autorizado.
- El calendario y agregado no cambian la granularidad del detalle; reconcilia
  filas, unidades e ingresos antes y despues de publicar.
