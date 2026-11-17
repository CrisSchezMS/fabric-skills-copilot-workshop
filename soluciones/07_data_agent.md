# Referencia 07: agente con evaluacion, no solo instrucciones

Configura un item Data Agent nuevo con una unica fuente:
`workshop_ventas_model`. Revisa primero el
[modulo 07](../docs/modulos/07-data-agent.md) y sus requisitos.

## Dos sitios distintos para las instrucciones

En el **modelo**, las descripciones y medidas explicitas fijan significados.
Las recomendaciones de `plantillas/instrucciones-modelo-ia.txt` se revisan
y aplican manualmente en Prep for AI. Esa es la ruta de contexto para DAX.

En el **Data Agent**, usa `plantillas/instrucciones-data-agent.txt` para idioma,
presentacion, fuente y limites. No uses ese campo como unica forma de excluir
cancelaciones: ya se excluyeron del detalle fisico. Tampoco es un permiso
para consultar otros datos o ejecutar escrituras.

El JSON de evaluacion no se importa como Example queries del modelo.
Los modelos semanticos no admiten esos pares pregunta/DAX en ese panel segun
la documentacion consultada. Si se usan Verified Answers, deben configurarse
y probarse por la experiencia soportada en Prep for AI.

## Referencias de evaluacion

| Caso | Referencia real que hay que obtener | Fallo significativo |
|---|---|---|
| Total | Informe ejecutado del notebook 01 | Usa raw o redondea solo al final |
| Categorias | Resumen PySpark y consulta DAX | Usa category_raw o repite hechos |
| Online, enero, por ciudad | Informe con los mismos filtros | Ignora fecha, canal o ciudad |
| "Cuantas ventas" | Aclaracion de la metrica | Afirma que filas son pedidos |
| Margen | Contrato de datos | Inventa costes o llama margen al ingreso |
| Causas | Variables disponibles | Atribuye causas no medidas |
| Periodo ausente | Rango observado | Inventa observaciones o extrapola |

Abre el detalle de la respuesta, identifica la fuente y revisa la consulta
generada. Un texto convincente con una consulta equivocada es un fallo.
No compares con un total general si se aplicaron filtros.

Para cada caso usa los campos de registro de
`plantillas/evaluacion-agente.json`. Deja la respuesta observada y pasa/falla
sin rellenar hasta la ejecucion. Al corregir metadata o instrucciones, repite
los casos afectados y alguno ya correcto para detectar regresiones.

Publica solo tras revisar las evidencias. La version publicada y el borrador
son distintos; publicar no autoriza compartir ni cambiar permisos.
Este documento no demuestra que exista un agente en Fabric.
