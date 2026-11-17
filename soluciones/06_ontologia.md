# Referencia 06: entidades y relaciones

Es un mapa revisable para aplicar manualmente en la experiencia V2 del portal,
no una definicion V1 ni un archivo importable. Consulta el
[modulo y su limite de skill](../docs/modulos/06-ontologia.md).

| Entidad | Fuente | Identidad de negocio |
|---|---|---|
| Productos | workshop_products | product_id |
| Tiendas | workshop_stores | store_id |
| LineasVenta | workshop_sales_clean | sale_id |

Productos incluye product_name, category y list_price; Tiendas incluye
store_name y city. LineasVenta incluye fecha, claves dimensionales, canal,
cantidad, precio, descuento e importe neto, ademas de su identificador.
El mapa detallado esta en `plantillas/ontologia.json`.

Las relaciones se orientan desde LineasVenta a las dimensiones:
`correspondeA` empareja product_id con product_id;
`ocurreEn` empareja store_id con store_id. Varias lineas pueden apuntar al
mismo producto o tienda, pero cada linea apunta a uno solo de cada.

El tipo ontologico no cambia la granularidad de origen. Crear otra entidad
llamada Pedido no fabrica un identificador de pedido ni una relacion real.
Las categorias y ciudades son propiedades canonicas de las dimensiones.

Antes de guardar, revisa cada binding en el portal: Lakehouse, esquema, tabla,
columna y tipo. Compara los identificadores seleccionados con la unicidad
verificada en Spark. Si un servicio no admite un binding o tipo, declara
la limitacion en vez de convertir el importe a float o inventar otro origen.

En la consulta de V2 con ontology-cli, solo `ask_ontology` por Ontology Agent
MCP permite seguir la ruta de grounding documentada. Si no esta disponible,
la consulta de ese tramo queda pendiente; responder desde SQL no prueba que
la ontologia funcione. Preguntar por costes o clientes debe revelar que
esas entidades/propiedades no existen en el escenario.

No se han creado entidades ni relaciones por guardar este documento.
