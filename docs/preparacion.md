# Preparacion para desplegar desde Copilot

La conexion con Fabric es parte del taller para **cada participante**.
No necesitas conocer IDs ni escribir REST: das el nombre del workspace y
Copilot utiliza las skills y herramientas autenticadas para descubrirlos.

## 1. Entorno Fabric

- Workspace dedicado al taller, capacidad activa y permisos de creacion y
  ejecucion. Usa una ubicacion distinta por participante para evitar colisiones.
- Lakehouse vacio o con las tres tablas del notebook 01. Si no existe,
  Copilot puede crearlo e importar/ejecutar el generador tras aprobar el plan.
- Permisos de acceso a los datos y de autoria del modelo/informe. El acceso
  a Fabric no sustituye las licencias y permisos Power BI aplicables.
- Para completar todas las ramas, servicios y configuraciones siguientes:

| Componente | Comprobar antes |
|---|---|
| Spark | Capacidad, permisos de notebook/tablas y Lakehouse predeterminado |
| Osmos | Acceso al servicio y capacidad elegible; trial confirmada FTL64 bloqueada por la skill revisada |
| Direct Lake / Power BI | Capacidad/modo soportados y autoria, lectura y consultas del modelo |
| Ontologia | Preview habilitada y version de autoria soportada por la skill |
| Data Agent | Capacidad pagada soportada, ajustes IA/regionales y permiso de crear/publicar |
| Native App | Fabric Apps habilitado, region/capacidad soportadas y derechos de despliegue; modelo con Read y Build para la consulta delegada |

Pide a quien administra el entorno que prepare lo que falte. Copilot no debe
cambiar tenant, capacidad o permisos para superar un bloqueo del laboratorio.
Poder ejecutar Spark no garantiza acceso a Osmos o a otra preview.

## 2. Copilot CLI y Fabric Skills

Abre el repo en VS Code o una terminal. Necesitas GitHub Copilot CLI instalado
y autenticado; sigue la [guia oficial](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started).
Instala el bundle oficial si no lo tienes, con autorizacion de tu organizacion:

```powershell
copilot plugin marketplace add microsoft/skills-for-fabric
copilot plugin install fabric-skills@fabric-collection
```

Inicia `copilot` desde la raiz y comprueba `/skills list`. Busca:
`workshop-ventas`, `spark-cli`, `sqldw-cli`, `project-osmos`,
`semantic-model-authoring`, `powerbi-report-cli`, `ontology-cli` y `fabriciq`.
Los nombres pueden incluir el prefijo del plugin.

El inventario real manda. `powerbi-report-cli` existe en el repositorio oficial,
pero una instalacion anterior puede no incluirla: actualiza el bundle mediante
el procedimiento oficial aprobado antes de la sesion. No copies solo un
SKILL.md: las referencias compartidas tambien son necesarias.

El plugin puede incluir agentes y configuracion MCP. Revisa lo instalado:
**las skills son instrucciones, no autenticacion ni permisos**. La skill local
coordina las oficiales, sin sustituirlas. No autorices globalmente todas las
herramientas por comodidad.

## 3. Herramientas y autenticacion que ejecutan

Prepara las herramientas que requieran las skills:

- CLI/API Fabric soportados y una sesion autenticada. Para la ruta Azure CLI,
  usa `az login` cuando corresponda. Nunca copies access tokens.
- MCP de modelado configurado/autorizado si se usa esa ruta. Tener el servidor
  anunciado no demuestra que conecte al modelo; Copilot debe probarlo.
- Para informes, las herramientas de autoria/validacion que indique la version
  instalada de `powerbi-report-cli`.
- Para Data Agent, SDK oficial `fabric-data-agent-sdk` en un entorno Python
  dedicado, o REST publico soportado. Para evaluar, cliente MCP autorizado.
- Para Native App, Node.js 20+ y scaffold/CLI Rayfin; sus paquetes se instalan
  con versiones coherentes en un proyecto privado fuera de este repo.

Copilot puede preparar y ejecutar instalaciones **cuando las autorices**;
presenta antes paquetes y destino. No instales dependencias SDK en este repo
solo por leer el laboratorio. Las pruebas locales no necesitan esos SDK.

Consulta el [MCP setup oficial](https://github.com/microsoft/skills-for-fabric/tree/main/mcp-setup).
El repo no incluye credenciales ni un `.vscode/mcp.json` con conexiones reales.
No todos los clientes comparten sesion: `az login` no autentica automaticamente
cada MCP ni Rayfin.

## 4. Prueba de preparacion con el workspace por nombre

```text
Mi workspace del taller es "<nombre de tu workspace>".
Usa workshop-ventas. Te autorizo a descubrir solo ese workspace, sus items,
capacidad y esquemas. Verifica las herramientas conectadas y los requisitos
por artefacto. Resuelve los IDs sin pedirmelos. No crees ni cambies recursos
en este preflight; dame el inventario listo/bloqueado y el alcance a aprobar.
```

Esta fase de lectura conduce a la ejecucion del
[laboratorio](laboratorio.md), no es el resultado final del taller.

| Bloqueo | Accion concreta |
|---|---|
| 401 / sesion caducada | Autenticar el cliente correcto, sin publicar tokens |
| 403 / workspace no visible | Confirmar nombre e identidad y pedir acceso a la persona responsable |
| Skill o herramienta ausente | Identificarla e instalar/configurar con consentimiento |
| Destino existente | Inspeccionar; reanudar solo lo validado de esta ejecucion o elegir otro destino explicitamente |
| SQL aun sin tablas recien creadas | Esperar sincronizacion; no escribirlas con T-SQL |
| Preview/capacidad no compatible | Marcar esa rama bloqueada; continuar las independientes |

No sustituimos automaticamente el taller conectado por una demo offline.
Si el entorno impide desplegar, se declara que la entrega esta bloqueada.
Fuentes y compatibilidad: [referencias](referencias-avanzadas.md).
