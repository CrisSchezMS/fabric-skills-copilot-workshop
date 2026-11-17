# Referencia 06: autoria conectada de ontologia

Copilot utiliza `ontology-cli`, esquema real y
`plantillas/ontologia.json` en el [modulo 06](../docs/modulos/06-ontologia.md).
La ruta revisada es **legacy V1 explicita**, no autoria V2 ni chat V2.

| Entidad | Fuente | Clave | Propiedades adicionales |
|---|---|---|---|
| Productos | workshop_products | product_id | product_name, category |
| Tiendas | workshop_stores | store_id | store_name, city |
| LineasVenta | workshop_sales_clean | sale_id | sale_date, product_id, store_id, channel, quantity |

Relaciona LineasVenta con Productos por product_id y con Tiendas por store_id.
Ambas contextualizaciones se basan en el detalle limpio. No inventes una
entidad Pedido ni enlaces raw como si fuera negocio elegible.

La V1 de la skill no ofrece decimal: se omiten precios, descuento e importe,
sin convertirlos a Double. Esos datos permanecen exactos en tablas y modelo.
Los tipos de entidad no son tablas nuevas ni fabrican observaciones.

Copilot descubre las fuentes, genera el arbol de definicion completo y su
mapa estable de IDs de concepto, presenta preview, obtiene `yes` y ejecuta
la creacion. Relee `getDefinition`, decodifica partes y contrasta claves,
tipos y bindings. El mapa de conceptos puede versionarse sin bindings de tenant;
payloads, IDs de recursos y snapshots del entorno se conservan privados.
Un fallo de escritura consume el intento: nuevo preview antes de repetir.

Vincular y refrescar/materializar instancias pueden ser pasos distintos:
marca el estado real de cada uno. Si solo hay herramientas de autoria,
no declares validada una consulta que no se ha ejecutado.
Para consulta V2 autorizada se exige `ask_ontology` por Ontology Agent MCP;
no uses SQL/KQL/PySpark ni `search_ontology` como sustituto.

Si el servicio requiere V2 y la skill no la crea, informa del bloqueo sin
eludir el limite. Continua las otras ramas del taller.
