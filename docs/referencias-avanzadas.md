# Fuentes y limites del despliegue conectado

Las previews, CLI y permisos cambian: contrasta la version instalada antes
de impartir. Consultar documentacion publica no prueba acceso a un tenant.
La aceptacion real se registra durante el despliegue del participante.

| Area | Fuente oficial |
|---|---|
| Skills, instalacion y referencias | [Microsoft Skills for Fabric](https://github.com/microsoft/skills-for-fabric) |
| Autoria de informes | [powerbi-report-cli](https://github.com/microsoft/skills-for-fabric/tree/main/skills/powerbi-report-cli) |
| Osmos | Skill instalada `project-osmos`, casos de uso y capacity-preflight |
| Ontologia | [Tutorial](https://learn.microsoft.com/en-us/fabric/iq/ontology/tutorial-1-create-ontology), skill instalada y sus limites V1/V2 |
| Definicion Ontology nueva | [Contrato publico](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/ontology-definition) |
| Data Agent SDK: crear/configurar/publicar/consultar | [Guia del SDK](https://learn.microsoft.com/en-us/fabric/data-science/fabric-data-agent-sdk) |
| Crear Data Agent REST | [Create](https://learn.microsoft.com/en-us/rest/api/fabric/dataagent/items/create-data-agent) |
| Definicion Data Agent | [Partes y schemas](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/data-agent-definition) |
| Leer definicion | [GetDefinition](https://learn.microsoft.com/en-us/rest/api/fabric/dataagent/items/get-data-agent-definition) |
| Publicar staging | [Publish](https://learn.microsoft.com/en-us/rest/api/fabric/dataagent/items/publish-data-agent) |
| Metadata/Prep for AI | [Buenas practicas](https://learn.microsoft.com/en-us/fabric/data-science/semantic-model-best-practices) |
| Fabric Apps | [Requisitos](https://learn.microsoft.com/en-us/fabric/apps/overview) y [crear App](https://learn.microsoft.com/en-us/fabric/apps/create-app) |
| Rayfin CLI/SDK | [Referencia](https://rayfin.ai/docs/reference/agent-rules.md) |
| Conectores Rayfin | [Registro](https://rayfin.ai/docs/connectors.md) y [modelo semantico](https://rayfin.ai/docs/connectors/semantic-models.md) |

## Alcance que no se debe confundir

- **Osmos** ejecuta una tarea completa de ingenieria, no construye toda la solucion
  BI/App. La skill revisada bloquea trial confirmada FTL64; comprueba la capacidad
  actual sin inferir elegibilidad por nombre o por falta de visibilidad.
- **Informe** tiene ruta oficial de autoria/publicacion por `powerbi-report-cli`.
  La skill existe upstream pero puede faltar en una instalacion anterior.
  Exige especificacion aprobada en otro turno antes de construir; FabricIQ no
  sustituye esa autoria. El JSON del taller no es un PBIR importable.
- **Ontologia**: la skill revisada crea V1 y consulta V2. Este taller ofrece
  creacion V1 declarada, sin prometer chat V2. Tener documentacion publica V2
  no permite saltar el limite de la skill instalada. No convertimos importes
  decimal a Double para adaptar V1.
- **Data Agent** no es portal-only: SDK/REST permiten crear, configurar y publicar.
  La consulta del agente publicado usa su endpoint MCP (o cliente de consumo
  oficialmente soportado), no una consulta directa FabricIQ al modelo.
  Publicado y evaluado son estados distintos. El SDK de consumo antiguo de
  Assistants no se usa como referencia de implementacion actual.
- **Modelo**: metadata y Prep for AI gobiernan el contexto DAX. No inventes
  pares Example queries de modelos/ontologias. Prep for AI/Verified Answers
  se configuran solo por rutas soportadas; esa mejora no bloquea la creacion
  normal del agente. Permisos de consumo Data Agent no son los de Rayfin.
- **Native App** usa proyecto scaffold oficial y herramientas Rayfin, no una
  pagina local ni una Power BI App. `dev` y `up` pueden aprovisionar remotamente.
  No mezcles SDK 1.x/2.x. El adaptador sigue respuesta normalizada 2.x; importes
  formateados como texto son solo presentacion, nunca aritmetica en JS.

Se conservan los gates de cada skill y no se cambian permisos/capacidad para
forzar una demo. Sin capacidad compatible o herramienta soportada, esa entrega
queda bloqueada con evidencia; el resto de ramas puede continuar.
No se incluyen copias de skills oficiales, tokens ni conexiones de tenant.
