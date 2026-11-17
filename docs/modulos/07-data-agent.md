# 07 - Copilot crea, publica y evalua el Fabric Data Agent

**Entrega:** `workshop_ventas_agent` con una sola fuente,
`workshop_ventas_model`, publicado y con preguntas evaluadas.
No necesitas crear el item manualmente en el portal.

## Requisitos

Modelo validado, permisos de creacion/escritura y capacidad compatible.
La documentacion consultada requiere Fabric pagada F2+ o Premium P1+ con
Fabric habilitado, junto a los ajustes IA/regionales aplicables. Comprueba
los requisitos vigentes y la identidad concreta; el taller no cambia politicas.

No se inventa una skill de creacion de Data Agent. Existe un **SDK oficial**
`fabric-data-agent-sdk` y REST publico de ciclo de vida. Copilot utiliza esas
interfaces documentadas con autenticacion real y alcance aprobado.
Si falta el SDK, pide aprobar instalacion en un entorno dedicado, fuera del repo.

## 1. Preparar el modelo sin frenar la creacion

Con `semantic-model-authoring`, comprueba nombres, descripciones, medidas y
relaciones. El detalle fisico ya excluye lineas no elegibles. La generacion
DAX usa metadata y Prep for AI del modelo, no solo el prompt general del agente.

`plantillas/instrucciones-modelo-ia.txt` orienta una mejora opcional mediante
la experiencia soportada de Prep for AI. No edites su representacion interna.
Si esa mejora requiere UI no automatizada, registrala aparte; no conviertas
la creacion/publicacion normal del Data Agent en un paso manual por ello.
Los pares Example queries no se admiten para modelos semanticos/ontologias
en la documentacion revisada: no importes el JSON de evaluacion como fewshots.

## 2. Ejecutar el ciclo de vida con SDK

```text
Continua el alcance aprobado. Crea y configura workshop_ventas_agent con el
SDK oficial fabric-data-agent-sdk o REST publico documentado.
Comprueba primero que no existe. Resuelve los IDs del workspace y del modelo
validado; no me pidas copiarlos ni los guardes en el repo.
Usa solo workshop_ventas_model como fuente y las instrucciones de
plantillas/instrucciones-data-agent.txt. Verifica la configuracion real,
publica el agente y relee su definicion. Despues ejecuta la evaluacion por
su endpoint MCP y compara con las referencias DAX/Spark ya observadas.
No entregues solo un item vacio ni un diseno.
```

La secuencia documentada del SDK, que **Copilot ejecuta** despues de comprobar
colisiones y obtener aprobacion, es:

```python
from fabric.dataagent.client import create_data_agent

# workspace_id y model_id proceden del descubrimiento real en la sesion privada.
agent = create_data_agent(
    data_agent_name="workshop_ventas_agent",
    workspace_id=workspace_id,
)
agent.update_settings(ai_instructions=agent_instructions)
agent.add_staging_datasource(
    artifact_name_or_id=model_id,
    workspace_id_or_name=workspace_id,
)
agent.publish_staging(description="Taller de ventas: modelo validado")
```

`agent_instructions` se lee del archivo del repo; los otros valores no son
constantes de ejemplo para subir a Git. Fuera de Fabric, autentica el SDK como
indique su guia, por ejemplo con AzureCliCredential; dentro de notebook aplica
la autenticacion de Fabric. No imprimas ni guardes tokens.
Comprueba que staging y publicacion contienen la unica fuente prevista.

## Ruta REST si es la herramienta disponible

Consulta los [contratos oficiales](../referencias-avanzadas.md) antes de componer
la definicion. Las operaciones publicas incluyen:

| Operacion | Ruta bajo `https://api.fabric.microsoft.com` |
|---|---|
| Crear con definicion | `POST /v1/workspaces/{workspaceId}/dataAgents` |
| Leer definicion | `POST /v1/workspaces/{workspaceId}/dataAgents/{dataAgentId}/getDefinition` |
| Publicar staging | `POST /v1/workspaces/{workspaceId}/dataAgents/{dataAgentId}/staging/publish` |

La definicion publica tiene `Files/Config/data_agent.json`, configuracion de
stage y datasource; no es el JSON de evaluacion. Usa los schemas actuales y
metadata real de fuente, nunca IDs de elemento inventados. Crear un item vacio
no completa el paso. No basta copiar partes "published" para afirmar publicacion:
usa el ciclo oficial y verifica el resultado.

Contributor y scopes de escritura aplicables son necesarios; una lectura no los
demuestra. Sigue 201/202, LRO y Retry-After segun cada operacion. Si falla tras
crear el item, conserva su ID e inspecciona el estado antes de otro intento.

## 3. Evaluar el agente realmente publicado

El endpoint MCP documentado es
`https://api.fabric.microsoft.com/v1/mcp/workspaces/{workspaceId}/dataagents/{dataAgentId}/agent`.
Copilot lo compone con los IDs reales, inicializa sesion y descubre sus
herramientas/schema antes de invocar; no asume un nombre/argumento fijo.
Solo funciona tras publicar. Tener FabricIQ no equivale a consultar este agente.

Ejecuta los casos de `plantillas/evaluacion-agente.json`: total, categorias,
mismos filtros, ambiguedad de "ventas", margen, causas y periodo ausente.
Registra respuesta, consulta/pasos si estan disponibles y pasa/falla contra DAX
y Spark **bajo los mismos filtros**. Si no se expone el SQL/DAX intermedio,
declara ese limite, no inventes una traza.

No inventes tasas de acierto ni resultados observados. Publicar permite
probar el endpoint, pero **publicado no significa validado**. Si fallan casos,
marca la entrega no aceptada, corrige con alcance autorizado, vuelve a publicar
y repite los afectados. No compartas ni otorgues permisos implicitamente.

[Referencia de evaluacion](../../soluciones/07_data_agent.md).
