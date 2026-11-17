# 06 - Crear una ontologia del negocio

**Objetivo:** representar productos, tiendas y lineas de venta como entidades
relacionadas y vinculadas a datos reales del taller. Una ontologia no es un
modelo Power BI ni transforma automaticamente las tablas.

## Requisitos y limite de automatizacion

Necesitas las tablas originales y `workshop_sales_clean` publicadas por 03 o 04,
la experiencia Ontology habilitada, capacidad y permisos compatibles. Sigue
los requisitos vigentes del [tutorial oficial](../referencias-avanzadas.md).
Si no aparece el item, no intentes habilitarlo ni cambiar el tenant desde el taller.

**Importante:** la `ontology-cli` disponible al preparar este material crea
definiciones **legacy V1** y consume ontologias **V2** existentes mediante
Ontology Agent MCP. No puede crear, convertir ni actualizar V2. Este modulo
crea V2 **manualmente en el portal**, no con un payload V1 disfrazado de V2.
Si el portal solo ofrece otra experiencia, detente y revisa la compatibilidad.

`plantillas/ontologia.json` es un mapa conceptual para revisar, **no** una
definicion importable de Fabric.

## Prompt de diseno

```text
Lee los dos contratos de datos y plantillas/ontologia.json.
Usa ontology-cli solo dentro de su alcance real. Propone entidades,
identificadores, propiedades, relaciones y bindings de productos, tiendas
y lineas limpias. Comprueba que cada propiedad tenga una columna de origen.
Si tu skill no crea V2, explica el limite y prepara pasos manuales del portal.
No consultes Fabric ni crees recursos. No inventes clientes ni inventario.
```

## Crear y vincular en el portal

Tras confirmar la operacion y el workspace dedicado:

1. Crea un item **Ontology** nuevo llamado `workshop_ventas_ontology`.
2. Anade los tipos `Productos`, `Tiendas` y `LineasVenta`, sin herencia.
3. En **Bind data**, elige el Lakehouse y esquema confirmados. Vincula cada
   entidad a su tabla del mapa conceptual; revisa propiedades y tipos
   propuestos antes de guardar.
4. Configura o comprueba los identificadores unicos que permita la experiencia:
   `product_id`, `store_id` y `sale_id`, respectivamente. Si el servicio no
   puede resolverlos de manera unica, no aceptes una clave inventada.
5. Crea `LineasVenta correspondeA Productos` por `product_id` y
   `LineasVenta ocurreEn Tiendas` por `store_id`.
6. Guarda y comprueba los bindings y la direccion de ambas relaciones.

El identificador de linea se conserva; no agrupes por producto para simular
una entidad venta. No enlaces la tabla raw: contiene copias y lineas no elegibles.
`category_raw` y `city_raw` no son propiedades canonicas del negocio.

## Preguntar con grounding

Primero inspecciona el grafo y sus bindings en el portal. Si despues autorizas
consulta conectada con `ontology-cli`, verifica que Ontology Agent MCP exponga
`ask_ontology`. Si no aparece, **detente**; no sustituyas la pregunta ontologica
por SQL/KQL/PySpark sobre las tablas ni por `search_ontology`.

Preguntas de prueba: "Que entidades y relaciones describe esta ontologia?",
"Que productos se relacionan con las lineas de una tienda?" y "Que significa
net_amount y de donde procede?". Contrasta sus respuestas con los bindings;
si una capacidad no esta soportada, registra la limitacion sin inventar respuesta.

Una metrica ontologica no aparece por existir un decimal: si quieres importar
metricas desde el modelo semantico, hazlo como ampliacion especifica, revisando
la funcionalidad actual y sin duplicar la regla del importe.

**Cierre:** tres entidades con origen trazable y dos relaciones correctas.
La parte consultada solo se marca validada si hay respuestas reales del agente.
Referencia: `soluciones/06_ontologia.md`.
