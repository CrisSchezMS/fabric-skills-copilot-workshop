# 05 - Crear el modelo semantico y un informe Power BI

**Objetivo:** construir una capa de negocio compartida por informe, Data Agent
y Native App. Aqui "dashboard" significa un **informe Power BI de dos paginas**,
no un Real-Time Dashboard ni un dashboard del servicio con tiles.

## Requisitos y diseno

Completa 03 **o** 04 y verifica las tablas publicadas. Necesitas permisos para
crear modelo e informe, acceso a las tablas y capacidad compatible con Direct
Lake. Confirma los requisitos de licencia de autoria/consumo con la organizacion.

Lee `plantillas/modelo-semantico.json` y `plantillas/informe.json`: son disenos,
no archivos PBIP ni payloads para crear items. Sus nombres de negocio son
propuestos; `sourceColumn` indica la columna fisica real.

El modelo `workshop_ventas_model` usa:

| Tabla del modelo | Fuente | Funcion |
|---|---|---|
| Ventas | workshop_sales_clean | Unica tabla de hechos |
| Productos | workshop_products | Producto y categoria |
| Tiendas | workshop_stores | Tienda y ciudad |
| Calendario | workshop_calendar | Fecha y atributos temporales |

Relaciona cada dimension 1:* con Ventas, filtro unidireccional desde dimension.
No cargues raw ni el agregado diario como otros hechos. No crees tablas
calculadas DAX para sustituir el calendario disponible.

## Prompts para construir con contexto

```text
Usa semantic-model-authoring, si esta instalada. Lee ambos contratos de docs/
y plantillas/modelo-semantico.json. Prepara el modelo estrella Direct Lake y
las cuatro medidas con sus formatos y descripciones. Comprueba los mapeos.
No inventes conexiones ni IDs, no crees ni conectes modelos todavia.
Identifica que parte requiere MCP de modelado y que parte hare en el portal.
No generes un PBIP vacio ni presentes este JSON como un formato importable.
```

La skill prioriza MCP de modelado cuando esta disponible; tenerlo anunciado
no permite aplicar cambios sin autorizacion. Si falta, sigue la ruta manual.
No escribas TMDL a mano en paralelo a una sesion MCP que este editando el modelo.

## Ruta manual en Fabric

1. En el Lakehouse confirmado, inicia la creacion de un **nuevo modelo semantico**
   con las cuatro tablas. Revisa el modo Direct Lake disponible antes de guardar.
   Si no esta disponible, detente y consulta la preparacion; no cambies a Import
   o DirectQuery sin explicar y aprobar el cambio.
2. Nombra el modelo `workshop_ventas_model`, si no existe. Aplica los nombres
   y mapeos del diseno. Es una escritura remota: confirma antes.
3. Revisa las tres relaciones y sus tipos. Marca Calendario como tabla de fechas
   usando Fecha cuando la experiencia lo permita; desactiva fechas automaticas.
   Configura claves y atributos numericos sin agregacion implicita.
4. Crea las cuatro medidas explicitas del JSON en Ventas. Oculta claves y
   columnas monetarias/cantidades base; usa las medidas en los visuales.
5. Ejecuta `plantillas/validar-modelo.dax` en una vista/cliente DAX autorizado
   para **consultar** el modelo, no en el SQL analytics endpoint.
6. Desde el modelo, crea un informe nuevo `workshop_ventas_report` y monta
   las dos paginas de `plantillas/informe.json`. No sustituyas un informe existente.

Para pedir ayuda con el informe:

```text
Usa el modelo validado y plantillas/informe.json para preparar dos paginas:
Resumen y Exploracion. Si tienes powerbi-report-cli, confirma su disponibilidad
y alcance antes de usarla; si no, dame los pasos del editor de Power BI.
No uses fabriciq como si creara informes. No publiques, reemplaces ni cambies
vinculos hasta que revise los cambios. No inventes un archivo PBIP funcional.
```

## Pruebas que aportan profundidad

Compara ingresos, unidades y lineas por categoria con PySpark, sin filtros.
Despues aplica **los mismos** filtros de fecha, ciudad y canal en las dos
experiencias y comprueba otra vez. Los totales no deben multiplicarse al unir.
Seleccionar una categoria debe filtrar los otros visuales sin cambiar el total
general cuando se quita la seleccion.

Usa una ciudad ficticia como categoria textual, **sin geocodificarla en un mapa**.
No hay coordenadas. Tampoco construyas margen, clientes, pedidos ni crecimiento
interanual con columnas que no existen.

**Cierre:** cuatro medidas y dos paginas guardadas, con filtros y totales
contrastados. No basta una captura de un grafico. La referencia esta en
`soluciones/05_modelo_e_informe.md`.
