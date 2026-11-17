---
name: workshop-ventas
description: Despliega el taller de ventas en un workspace indicado por nombre usando Fabric Skills, Project Osmos y herramientas oficiales. Descubre, pide aprobacion, ejecuta y verifica artefactos reales.
---
# Taller conectado: del nombre del workspace a una solucion funcionando

Skill LOCAL del taller. Coordina las Microsoft Fabric Skills oficiales; no las
instala, no proporciona credenciales y no sustituye sus procedimientos.

## Flujo principal

1. Lee `docs/datos.md`, `docs/contrato-analitico.md` y `docs/despliegue.md`.
   El objetivo normal es desplegar y ejecutar, no limitarse a escribir propuestas.
2. Recoge el nombre del workspace. Si ya se proporciono, usalo. Descubre sus IDs
   mediante herramientas autenticadas: lista workspaces con paginacion y filtra
   displayName exacto. Si hay ambiguedad, pide elegir. Catalog Search busca items,
   no workspaces. Resuelve Lakehouse y esquema reales; no pidas IDs al principiante.
3. Inventaria skills, herramientas, identidad, permisos efectivos y capacidad.
   Una skill instalada o un rol visible no prueban acceso a todos los servicios.
   Explica bloqueos por artefacto con la respuesta real, sin inventar resultados.
4. Presenta nombres, dependencias, lecturas, escrituras, coste de capacidad y
   recursos de App del alcance concreto. Obtiene aprobacion antes de escribir.
   No vuelvas a pedir aprobacion generica para cada comando ya cubierto.
   Respeta ademas los gates obligatorios de cada skill: especificacion del
   informe en otro turno; preview y `yes` de ontologia; intake de Osmos.
5. Ejecuta las operaciones aprobadas con las skills correspondientes. Guarda,
   arranca, espera operaciones largas y relee los resultados. El codigo mostrado
   o guardado localmente no completa un despliegue. No dejes flags desactivados
   como entrega final cuando se ha autorizado ejecutar.
6. Valida contra fuentes reales, registra IDs/enlaces/estado fuera del repo
   publico y continua las dependencias disponibles. Un bloqueo de ontologia
   no debe detener el informe, Data Agent ni App.
7. En una reanudacion, descubre y verifica lo ya creado. No sobrescribas, borres,
   cambies nombres o repitas creaciones de resultado ambiguo automaticamente.
   Informa de publicacion parcial y pide una decision concreta.

## Enrutamiento

| Resultado | Skill / herramienta |
|---|---|
| Notebook desplegado, perfilado y tres tablas Delta | `spark-cli`, modo authoring; fuentes `src/` y constructor de notebook |
| Mismo resultado delegado a un agente remoto | `project-osmos`, una unica tarea completa; alternativa a Spark, no segunda carga |
| Consultas T-SQL de contraste | `sqldw-cli`, solo lectura del SQL analytics endpoint |
| Modelo Direct Lake, relaciones y medidas | `semantic-model-authoring`, MCP de modelado o ruta de despliegue soportada por la skill |
| Informe Power BI real | `powerbi-report-cli`, si esta instalada; plan aprobado, PBIR validado y publicacion |
| Preguntas sobre modelo/informe existente | `fabriciq`, no autoria de informes |
| Ontologia | `ontology-cli`, solo la version que realmente permita crear; ver modulo 06 |
| Data Agent creado, configurado y publicado | SDK oficial `fabric-data-agent-sdk` o REST publico documentado; no inventar una skill |
| Fabric Native App | Scaffold y CLI oficial Fabric Apps/Rayfin, con SSO y conector delegado |

Si falta una skill, indica cual y pide aprobacion para instalarla; no simules
su uso ni saltes sus limites mediante una API improvisada. Native App y Data
Agent tienen rutas oficiales propias aunque no haya una skill dedicada.

## Invariantes

- Conserva el notebook generador y las tres tablas originales.
- Comprueba esquemas antes de perfilar; separa incidencias raw, copias y ventas
  unicas. Ante sale_id nulo o versiones diferentes, detente.
- Dimensiones canonicas, completed, cantidad positiva, claves validas,
  decimal y redondeo por linea. Lee el contrato; no inventes metricas.
- Escribe solo los destinos exactos aprobados. Delta con `errorifexists`,
  todos los destinos comprobados antes de escribir y reconciliacion posterior.
- No crees workspaces, cambies permisos/capacidad/tenant ni instales herramientas
  implicitamente. Los recursos internos de Rayfin requieren alcance aprobado.
- Si se pide expresamente solo preparar o no conectar, respeta ese modo.
  Una peticion de editar este repo tampoco autoriza actuar sobre un tenant.
