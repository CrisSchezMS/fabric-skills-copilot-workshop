# Contrato de la ampliacion analitica

Este contrato propone **nuevos destinos**. No afirma que existan en tu Fabric.
Conserva el generador y las tres tablas de [datos.md](datos.md) sin cambios.
Los modulos avanzados no introducen clientes, pedidos, costes ni inventario.

## Tablas propuestas

Todas se publican con Spark, en el esquema confirmado del mismo Lakehouse
dedicado al taller. `dbo` no se asume como prueba del esquema real.

| Tabla | Granularidad | Columnas |
|---|---|---|
| `workshop_sales_clean` | Una linea elegible por `sale_id` | `sale_id`, `sale_date`, `product_id`, `store_id`, `channel`, `quantity`, `unit_price`, `discount_rate`, `status`, `category`, `city`, `net_amount` |
| `workshop_sales_daily` | Fecha, producto, tienda y canal | `sale_date`, `product_id`, `store_id`, `channel`, `sales_count`, `units`, `net_revenue` |
| `workshop_calendar` | Un dia por `calendar_date` | `calendar_date`, `calendar_year`, `calendar_quarter`, `month_number`, `year_month` |

En el detalle se mantienen los tipos raw; `category` y `city` son string
canonicos de las dimensiones. `net_amount` es decimal(18,2), calculado con
HALF_UP por linea antes de sumar. La solucion 02 ya produce este esquema en
memoria; el nuevo notebook 03 permite publicarlo tras aprobacion.

En el agregado, `sales_count` y `units` son long/bigint; `net_revenue` es
decimal(38,2), conversion explicita tras sumar importes decimal(18,2). Las cuatro columnas
de agrupacion conservan los tipos del detalle. No se promedian descuentos.
Las unidades y los ingresos del agregado deben reconciliar exactamente con
el detalle; la suma de `sales_count` debe coincidir con sus filas.

En calendario, `calendar_date` es date, los campos numericos son int y
`year_month` es string `yyyy-MM`. Incluye los anios completos que abarcan
las fechas observadas en ventas limpias, con dias contiguos y sin duplicados.
Los dias sin ventas no son observaciones de ingresos cero. No se publican
tablas si no hay ninguna venta elegible.

## Reglas que no cambian

Primero se quitan copias exactas y se comprueba que no hay versiones distintas
del mismo `sale_id`. Las dimensiones deben tener claves unicas y no nulas.
Solo se aceptan lineas completed, quantity > 0 y con ambas claves existentes.
Los nulos o textos desnormalizados raw no se usan como dimensiones canonicas.

El calendario no permite inventar ventas fuera del rango observado. Con la
configuracion original no hay un anio anterior para evaluar crecimiento
interanual ni datos suficientes para afirmar estacionalidad.

## Publicacion y reejecucion

`WRITE_ANALYTICS = False` deja todo en memoria. Tras revisar los totales y el
destino, la persona participante puede autorizar la publicacion.
La referencia comprueba **los tres destinos antes de escribir ninguno** y usa
`errorifexists`; no ofrece una opcion de sobrescritura.

Las tres escrituras no son una transaccion. Una colision concurrente o un
fallo intermedio puede dejar tablas parciales. Detente, inspecciona el estado
y decide con la persona facilitadora; no borres ni reintentes automaticamente.
La aprobacion local no concede permisos ni sustituye la confirmacion remota.

## Artefactos que consumen estas tablas

| Nombre propuesto | Tipo | Fuente |
|---|---|---|
| `workshop_ventas_model` | Modelo semantico Direct Lake | Detalle limpio, productos, tiendas y calendario |
| `workshop_ventas_report` | Informe Power BI | Solo el modelo semantico |
| `workshop_ventas_ontology` | Ontologia | Productos, tiendas y lineas limpias |
| `workshop_ventas_agent` | Fabric Data Agent | Inicialmente solo el modelo semantico |
| `workshop_ventas_app` | Fabric Native App, Fabric Apps preview | Conector delegado al modelo semantico |

Los nombres son propuestas para recursos nuevos, no IDs ni recursos
descubiertos. Una colision exige detenerse, no reemplazar un artefacto existente.
No cargues detalle y agregado como dos hechos sumables del mismo modelo:
contarias dos veces los mismos ingresos. El agregado se usa para contrastar.

Las plantillas JSON de `plantillas/` son **contratos de diseno**, no payloads
importables en las APIs de Fabric. La excepcion es
`native-app/ingresos-categoria.json`: es un payload DAX para el conector Rayfin
documentado, que requiere un modelo ya creado y validado.
