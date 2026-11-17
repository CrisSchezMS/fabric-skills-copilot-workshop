# Recorrido de construccion conectada

Estos modulos forman el taller principal de despliegue. No son un apendice
offline: Copilot usa el workspace indicado por nombre, ejecuta las operaciones
aprobadas y entrega artefactos reales. Empieza por el
[laboratorio](laboratorio.md) y el [runbook](despliegue.md).

```text
Notebook 01 intacto -> tres tablas originales
                        |
               Spark O Project Osmos
                        |
            detalle + agregado + calendario
                        |
           +------------+------------------+
           |                               |
    modelo Direct Lake                 ontologia
           |
     +-----+-----------+----------------+
     |                 |                |
 informe Power BI   Data Agent     Fabric Native App
```

Spark y Osmos son alternativas sobre los mismos destinos. La ontologia es
independiente del modelo: su disponibilidad no bloquea informe/agente/App.
El agregado diario sirve para contrastar, no se carga como otro hecho sumable.

| Modulo | Resultado persistido y verificado | Ruta |
|---|---|---|
| [03 Base analitica](modulos/03-base-analitica.md) | Notebook ejecutado y tres tablas reconciliadas | `spark-cli` |
| [04 Project Osmos](modulos/04-project-osmos.md) | Una tarea completa, notebook y mismas tablas | `project-osmos`, alternativa a 03 |
| [05 Modelo e informe](modulos/05-modelo-informe.md) | Modelo Direct Lake, cuatro medidas, informe de dos paginas | `semantic-model-authoring` + `powerbi-report-cli` |
| [06 Ontologia](modulos/06-ontologia.md) | Tres entidades, dos relaciones y bindings releidos | `ontology-cli`, version declarada |
| [07 Data Agent](modulos/07-data-agent.md) | Agente configurado, publicado y evaluado | SDK oficial o REST publico |
| [08 Native App](modulos/08-native-app.md) | Item App, SSO y consulta real desde la URL publicada | Fabric Apps/Rayfin |

Reserva varias sesiones: ingenieria 30-60 minutos; modelo/informe 45-75;
ontologia 30-45; agente 30-45; App 60-90, mas ejecucion/provisionamiento
variable. Son orientaciones, no compromisos de tiempo ni de disponibilidad.

Una aprobacion de alcance permite continuar las operaciones cubiertas.
Se mantienen las revisiones obligatorias de informe, ontologia y Osmos.
Si falta una skill, se instala con consentimiento; si falta elegibilidad,
se informa del bloqueo sin simular el resultado. No hay un modo manual como
sustitucion silenciosa del objetivo conectado.

Las plantillas son entradas para Copilot. La entrega requiere llamadas exitosas
y lectura posterior, no solo preparar archivos. Consulta las
[fuentes y limites](referencias-avanzadas.md).
