# De las ventas raw a artefactos de Fabric

La [ruta basica](laboratorio.md) sigue siendo de 60 minutos. Estos modulos
opcionales anaden construccion real: no son necesarios para generar los datos.
Se recomienda hacerlos en sesiones posteriores, no comprimirlos en una hora.

## Mapa de recorrido

```text
Notebook 01: tres tablas originales, sin cambios
    |
    +-- 03 Spark guiado --------+
    |                          |
    +-- 04 Project Osmos ------+--> detalle limpio + agregado + calendario
                                             |
                      +----------------------+----------------------+
                      |                                             |
                 05 Modelo + informe                           06 Ontologia
                      |                                        (independiente)
                 +----+----------------+
                 |                     |
            07 Data Agent        08 Fabric Native App
```

03 y 04 son **alternativas para obtener los mismos destinos**: no ejecutes
ambas en el mismo Lakehouse ya poblado. Ontologia no es un requisito del
Data Agent ni de la app; el recorrido principal reutiliza el modelo semantico.
Asi se puede completar una rama aunque otra preview no este habilitada.

| Modulo | Tiempo orientativo, sin instalaciones | Resultado verificable |
|---|---|---|
| [03 Base analitica](modulos/03-base-analitica.md) | 25-35 min | Tres tablas derivadas reconciliadas |
| [04 Project Osmos](modulos/04-project-osmos.md) | 30-45 min, mas ejecucion variable | Una tarea de ingenieria completa, notebook y tablas verificadas |
| [05 Modelo e informe](modulos/05-modelo-informe.md) | 35-50 min | Modelo estrella, cuatro medidas y dos paginas |
| [06 Ontologia](modulos/06-ontologia.md) | 25-40 min | Tres entidades, dos relaciones y vinculos revisados |
| [07 Data Agent](modulos/07-data-agent.md) | 25-40 min | Agente evaluado con preguntas positivas y negativas |
| [08 Native App](modulos/08-native-app.md) | 45-75 min, mas provisionamiento | Item App con autenticacion y consulta real al modelo |

Son estimaciones de facilitacion, no tiempos garantizados de servicio.
Cada modulo incluye objetivo, requisitos, prompts, pasos, comprobaciones,
criterio de cierre y referencia separada.

## Que puede hacer cada skill

| Trabajo | Ruta y limite |
|---|---|
| Notebook y tablas Delta | `spark-cli`; ejecucion manual revisada o herramientas autorizadas |
| Ingenieria autonoma | `project-osmos`; una tarea completa, no una tarea por capa |
| Modelo y medidas | `semantic-model-authoring`; MCP de modelado si esta disponible y autorizado |
| Crear el informe | Portal Power BI; `powerbi-report-cli` solo si esta realmente instalada y admite la operacion |
| Preguntar por informe/modelo | `fabriciq`; no confundir consulta con creacion de informes |
| Ontologia | `ontology-cli`, respetando la version: la instalada al preparar el material crea V1 y consulta V2; no crea ni actualiza V2 |
| Crear Data Agent | Ruta guiada en el portal; no se presupone una skill de creacion instalada |
| Native App | Herramientas oficiales Fabric Apps/Rayfin; no se presupone una skill especifica instalada |

La disponibilidad puede cambiar por version del plugin. Pide inventario real
al comenzar. No inventes nombres de skills ni llames exito a un borrador local.

## Tres modos de trabajo

1. **Preparar localmente:** leer contratos, generar propuestas y revisar
   plantillas; sin autenticarse, consultar el tenant, instalar ni desplegar.
2. **Ejecutar manualmente:** la persona revisa y ejecuta en Fabric. Copilot
   no puede afirmar haber comprobado esos resultados si no los ha recibido.
3. **Actuar conectado:** autorizar por separado descubrimiento de solo lectura
   y cada conjunto de escrituras, indicando nombres y alcance del entorno.

Los materiales publicados se han preparado localmente. Los notebooks se
distribuyen sin ejecutar; los disenos, DAX y la integracion Rayfin no constituyen
una certificacion de ejecucion en tu tenant.

## Preparacion avanzada

Verifica permisos y capacidad con antelacion. Osmos, ontologia, Data Agent y
Fabric Apps tienen requisitos propios; poder ejecutar Spark no garantiza
que esten disponibles. Un administrador prepara las configuraciones necesarias:
el taller no cambia politicas, capacidad, permisos ni habilita previews.

Para cada modulo registra fuera del repositorio publico: destino confirmado,
operacion autorizada, evidencia observada y estado:
**propuesto / guardado local / creado en Fabric / validado en Fabric**.
No publiques IDs, URLs privadas, tokens ni salidas del entorno.

Consulta las [fuentes y limitaciones](referencias-avanzadas.md) antes de impartir.
