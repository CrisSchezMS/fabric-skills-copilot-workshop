# 06 - Copilot crea la ontologia y verifica sus bindings

**Entrega:** `workshop_ventas_ontology`, tres entidades y dos relaciones
persistidas, con claves y fuentes trazables. Requiere tablas limpias/dimensiones,
capacidad, preview y permisos de autoria compatibles.

## Version explicita, sin prometer una API que la skill no implementa

La `ontology-cli` revisada **crea legacy V1** y **consulta V2** por Ontology
Agent MCP. No crea ni convierte V2. Este modulo usa autoria **V1 explicita**
si esa es la capacidad instalada y el servicio la admite; no lo presenta
como V2 ni como un chat ontologico.

Si necesitas V2, comprueba si hay una version de la skill/herramienta que permita
autoria V2 y revisa su procedimiento. La existencia de documentacion publica
V2 no amplia por si sola la skill instalada. No eludas su limite mediante
REST improvisado ni crees V1 cuando la persona requiera V2.
Si no hay ruta compatible, bloquea solo esta entrega y sigue agente/App.

## Construccion conectada

```text
Usa ontology-cli en modo authoring para crear workshop_ventas_ontology.
Comprueba la version soportada y explica que V1 no da el chat V2.
Usa plantillas/ontologia.json y las tablas/esquema reales ya validados.
Prepara tres entidades con sus claves y dos relaciones con contextualizaciones.
Descubre columnas y tipos antes de generar bindings. Genera la definicion
completa y el mapa estable de IDs de concepto; guarda el payload con bindings
reales fuera del repo publico. Muestra el preview completo exigido por la
skill y espera mi yes antes de la escritura.
```

Revisa el preview y responde `yes` cuando el destino/version sean correctos.
Entonces Copilot envia **una vez** el payload aprobado, sigue la LRO y ejecuta
`getDefinition` para verificar lo creado. El greenfield admite la definicion
completa en una sola creacion, sin dejar un item vacio como resultado.
Cada intento fallido necesita nuevo preview/confirmacion antes de otra escritura.

| Entidad | Fuente | Clave |
|---|---|---|
| Productos | workshop_products | product_id |
| Tiendas | workshop_stores | store_id |
| LineasVenta | workshop_sales_clean | sale_id |

`correspondeA`: LineasVenta.product_id -> Productos.product_id.
`ocurreEn`: LineasVenta.store_id -> Tiendas.store_id.
Ambas contextualizaciones se apoyan en el detalle limpio; no en raw.
Comprueba unicidad y relaciones antes de vincular.

## Tipos e importes

El mapa incluye solo propiedades compatibles con V1: identidades, textos,
fecha y cantidad. La skill permite String, Boolean, DateTime, Object, BigInt
y Double, pero **no decimal**. Por eso no vinculamos precios, descuento ni
net_amount como Double: los importes siguen exactos en las tablas/modelo.
No se transforma ni pierde precision para forzar este modulo.
La plantilla es un mapa conceptual, no una definicion importable.

## Aceptacion y consulta

Relee y decodifica la definicion: tres entidades, dos relaciones, IDs estables,
bindings al Lakehouse/esquema correcto y claves coincidentes con las columnas.
Un binding guardado no demuestra que las instancias esten materializadas:
comprueba el estado/refresh que permita el servicio; si requiere accion de UI
no automatizable con las herramientas disponibles, declaralo pendiente.

No prometas preguntas naturales sobre V1. Para una ontologia V2 existente
y consulta expresamente autorizada, `ontology-cli` exige descubrir `ask_ontology`
en Ontology Agent MCP. Sin esa herramienta, detente: SQL/KQL/PySpark ni
`search_ontology` son sustitutos de esa validacion.

[Referencia](../../soluciones/06_ontologia.md). Esta rama no es requisito
para el Data Agent ni para la App del taller.
