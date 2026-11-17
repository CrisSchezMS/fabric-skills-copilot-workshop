# Fuentes y limites de los modulos avanzados

Referencias publicas consultadas el **17 de noviembre de 2026**. Las previews,
CLI, permisos y nombres de interfaz cambian: contrasta tu version antes de la
sesion. Consultar documentacion publica no equivale a consultar un tenant.
No se han desplegado estos artefactos en el entorno de la persona participante.

| Area | Fuente |
|---|---|
| Skills, instalacion y alcance actual | [Microsoft Skills for Fabric](https://github.com/microsoft/skills-for-fabric) |
| Project Osmos | Skill instalada `project-osmos`, sus referencias de casos de uso y capacity-preflight; revisar la version instalada, sin copiarla a este repo |
| Crear una ontologia | [Tutorial oficial de Ontology](https://learn.microsoft.com/en-us/fabric/iq/ontology/tutorial-1-create-ontology) |
| Crear y publicar Data Agent | [Guia oficial](https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent) |
| Contexto del modelo y Prep for AI | [Buenas practicas de modelos para Data Agent](https://learn.microsoft.com/en-us/fabric/data-science/semantic-model-best-practices) |
| Fabric Apps preview | [Descripcion y requisitos](https://learn.microsoft.com/en-us/fabric/apps/overview) |
| Crear App con portal o CLI | [Primer proyecto Fabric Apps](https://learn.microsoft.com/en-us/fabric/apps/create-app) |
| SDK/CLI Rayfin, versiones y precauciones | [Referencia de desarrollo](https://rayfin.ai/docs/reference/agent-rules.md) |
| Conectores y registro del cliente | [Conectores Rayfin](https://rayfin.ai/docs/connectors.md) |
| Conector al modelo y forma de respuesta | [Semantic models en Rayfin](https://rayfin.ai/docs/connectors/semantic-models.md) |

## Compatibilidad que hay que explicar

- **Osmos:** la skill dirige tareas de ingenieria de datos, no todos los
  artefactos de Fabric. En produccion publica bloquea la trial confirmada
  FTL64 y exige verificar la asignacion actual. No deducir elegibilidad por nombre.
- **Ontologia:** el contrato de la ontology-cli instalada distingue autoria
  legacy V1 y consulta V2. La creacion V2 del taller se hace en el portal.
  No se ofrece un payload V1 como conversion o upgrade.
- **Informe:** el repo contiene un diseno y medidas, no un `.pbix`/PBIP
  funcional inventado. `fabriciq` consulta modelos/informes, no los crea.
- **Data Agent:** las reglas DAX van en metadata/Prep for AI del modelo.
  No se ofrecen ejemplos pregunta/DAX para un panel Example queries que
  no los admite en modelos semanticos. Su ruta documentada usa Read para
  consumir modelos; otras herramientas pueden requerir Build o Write.
- **Native App:** se sigue el scaffold oficial y la referencia especifica
  Rayfin 2.x para el adaptador, sin mezclar APIs 1.x/2.x. El resumen de alguna
  pagina describe desarrollo local de forma general; la referencia actual
  especifica advierte que `dev` puede provisionar backend remoto y que los
  conectores se prueban desplegados. No se presupone un backend offline.
- **Importes:** el conector devuelve importes formateados como texto solo
  para presentacion. Los calculos y reconciliacion siguen en decimal en
  Spark/modelo; no se usa Number/float para calcular dinero en la app.

No se incluyen copias de las skills oficiales, tokens, configuraciones de
autenticacion ni recursos preexistentes. Los JSON de diseno son propios del
taller, no formatos oficiales de intercambio.
