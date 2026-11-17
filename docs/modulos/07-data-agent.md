# 07 - Crear y evaluar un Fabric Data Agent

**Objetivo:** permitir preguntas sobre ventas sin perder las definiciones
validadas del modelo. No se trata de pegar un prompt y aceptar la primera respuesta.

## Requisitos y entregables

Completa 05. El agente inicial usara **solo `workshop_ventas_model`**, no raw,
agregado y modelo a la vez. La ontologia es una ampliacion independiente.

La documentacion consultada requiere capacidad Fabric pagada F2 o superior,
o Premium P1 o superior con Fabric habilitado, y los ajustes de IA/regiones
indicados por Microsoft. Deben prepararlos los administradores, no el agente.
Para consumir el modelo desde Data Agent basta Read segun la ruta documentada;
modificar el modelo o Prep for AI requiere Write. No generalices ese minimo
a la app Rayfin, al editor de informes ni al MCP de modelado.

No se presupone una skill de creacion de Data Agent instalada. Usaremos el
portal para crear el item y `semantic-model-authoring` para preparar metadata
del modelo dentro de sus capacidades.

## Preparar el modelo antes del agente

```text
Usa semantic-model-authoring si esta instalada. Con los contratos y
plantillas/modelo-semantico.json, prepara una revision de nombres,
descripciones, medidas explicitas y relaciones para informe y preguntas.
Separa metadata editable por herramientas de la configuracion manual
en Prep data for AI. No conectes, consultes ni modifiques modelos todavia.
```

Comprueba las descripciones y medidas de 05. Revisa
`plantillas/instrucciones-modelo-ia.txt` y, si procede, aplicalas manualmente
en **Prep data for AI** del modelo. Incluye los objetos y dependencias
necesarios, evitando fuentes duplicadas. No edites su representacion interna.

**Distincion importante:** la generacion DAX se apoya en metadata y Prep for AI;
no confies en instrucciones generales del Data Agent para imponer reglas DAX.
Los pares pregunta/consulta de **Example queries** no estan soportados para
modelos semanticos ni ontologias en la documentacion consultada.
Las consultas DAX de este repo son referencias de validacion, no ejemplos
que se puedan importar en ese panel. Verified Answers se configura y prueba
manualmente en Prep for AI si la experiencia esta disponible.

## Crear, probar y publicar

1. Tras aprobar el destino, crea un item **Fabric data agent** nuevo llamado
   `workshop_ventas_agent` en el workspace del taller.
2. Anade el modelo semantico confirmado. Selecciona solo las tablas relevantes
   de la plantilla del modelo, coherentes con su configuracion para IA.
3. Revisa y aplica `plantillas/instrucciones-data-agent.txt` en las instrucciones
   generales: idioma, fuentes, ambiguedad y limites. No son un control de acceso.
4. Ejecuta los casos de `plantillas/evaluacion-agente.json` uno a uno,
   empezando sin filtros. Abre los pasos intermedios y la consulta generada.
5. Compara importes exactos con PySpark y medidas DAX bajo **los mismos filtros**.
   Registra fallo, correccion y repeticion; no inventes una tasa de acierto.
6. Solo despues de aprobar las pruebas, confirma la publicacion del agente.
   Compartirlo o cambiar permisos es otra decision; no viene autorizado por crear.

```text
Prepara un plan de evaluacion usando plantillas/evaluacion-agente.json.
Para cada pregunta indica que medida/filtro deberia usarse, con que referencia
comparar y que respuesta seria incorrecta. No rellenes respuestas observadas
ni marques pasa/falla sin ejecucion real. No publiques ni cambies permisos.
```

## Cierre

Debe responder con cifras contrastadas y reconocer que no hay margen, pedidos,
clientes ni causas medidas. "No puedo responder con estas fuentes" es una
respuesta correcta cuando falta informacion.

Conserva las evidencias del entorno fuera del repo publico. Si no dispones de
la capacidad o configuracion necesaria, entrega el diseno y plan de evaluacion
como **no ejecutados**, no un chatbot simulado.
Referencia: `soluciones/07_data_agent.md`.
