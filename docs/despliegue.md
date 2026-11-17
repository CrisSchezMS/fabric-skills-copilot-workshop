# Runbook: desplegar el taller desde Copilot

**Entrada:** nombre del workspace; Lakehouse por nombre si ya lo conoces.
**Salida:** artefactos persistidos, ejecutados y comprobados en ese workspace.
Este documento guia la ejecucion con skills, no es un script que se autoejecute.

## 1. Descubrimiento y preflight de solo lectura

Con el permiso de descubrimiento del prompt inicial:

1. Inventaria skills y herramientas disponibles; lee las referencias del modo
   de cada skill antes de sus operaciones. Comprueba autenticacion sin imprimir
   tokens. Si no hay sesion, guia el inicio de sesion del cliente real.
2. Lista `/v1/workspaces` con paginacion y compara el nombre exacto. Cero resultados
   no prueba que el workspace no exista: puede faltar acceso. Varios requieren
   elegir; nunca tomes el primero. No uses Catalog Search para buscar workspaces.
3. Lista items del workspace y descubre Lakehouse, esquema y tablas. Si faltan,
   incluye creacion de Lakehouse/importacion/ejecucion del generador en el plan.
   No crees nada en esta fase. Si hay varios Lakehouses, pide elegir.
4. Comprueba capacidad asignada actual y requisitos de cada workload. Contributor
   suele ser necesario para crear items; Direct Lake, autoria Power BI, Apps,
   Data Agent y Osmos tienen requisitos adicionales. Una lectura exitosa no
   demuestra permiso de escritura. Si no puedes comprobar un permiso, marcalo
   pendiente de la operacion, no como aprobado.
5. Inspecciona nombres existentes. Presenta por artefacto: listo, bloqueado o
   requisito pendiente, con evidencia de servicio. Un 401/403 se diagnostica;
   no se cambia a otro workspace ni se elevan permisos automaticamente.

Cada llamada de una Fabric Skill usa su `x-ms-fabric-skill`, tambien al paginar,
reintentar o sondear. Usa herramientas registradas o CLI oficiales autenticadas.
No inventes endpoints, cuerpos de definicion ni IDs.

## 2. Inventario que se presenta para aprobar

Los siguientes nombres son **destinos propuestos**, no recursos descubiertos:

| Artefacto | Nombre | Depende de | Ruta |
|---|---|---|---|
| Datos originales, si faltan | notebook 01 y tres tablas de datos.md | Lakehouse dedicado | `spark-cli`, generador intacto |
| Notebook de ingenieria | `workshop_03_base_analitica` | Datos originales | `spark-cli` **o** `project-osmos` |
| Detalle / agregado / calendario | `workshop_sales_clean`, `workshop_sales_daily`, `workshop_calendar` | Notebook ejecutado | Spark, Delta, sin overwrite |
| Modelo | `workshop_ventas_model` | Detalle, dimensiones, calendario | `semantic-model-authoring` |
| Informe | `workshop_ventas_report` | Modelo validado | `powerbi-report-cli` |
| Ontologia | `workshop_ventas_ontology` | Detalle y dimensiones | `ontology-cli`, version declarada |
| Data Agent | `workshop_ventas_agent` | Modelo validado | SDK oficial o REST documentado |
| Native App | `workshop_ventas_app` | Modelo validado | Fabric Apps/Rayfin |

Muestra el workspace/Lakehouse/esquema reales y sus IDs en la sesion privada.
Incluye lectura de fuentes, creacion, ejecucion Spark/Osmos, publicacion de
agente/App y consultas de validacion. Describe servicios internos que Rayfin
vaya a aprovisionar. Explica consumo de capacidad y posibles costes; no inventes
una estimacion monetaria sin datos. No incluye compartir ni borrar al terminar.

Pide elegir **Spark u Osmos**, no ambos contra los mismos destinos. Si la persona
ha elegido, no lo vuelvas a preguntar. Si Osmos esta bloqueado, propone Spark
como alternativa conectada y obtiene la decision; no simules una tarea Osmos.

## 3. Aprobar para ejecutar, no para volver a planificar

Ejemplo de aprobacion tras ver el inventario real:

```text
Apruebo crear y ejecutar los artefactos y consultas de validacion del inventario
que acabas de mostrar en ese workspace y Lakehouse. Usa la ruta Spark acordada.
Continua las dependencias aprobadas hasta validarlas. Detente solo ante una
decision nueva, un bloqueo o una revision obligatoria de la skill. No borres,
sobrescribas, compartas ni cambies permisos o capacidad.
```

Esa aprobacion no instala herramientas implicitamente. Recoge antes o aparte
el consentimiento para las dependencias concretas que falten.
Las skills pueden exigir un gate mas especifico:

| Gate obligatorio | Que debe ocurrir |
|---|---|
| Informe nuevo | La skill guarda una especificacion; el usuario la aprueba en un turno posterior, antes de construir/publicar |
| Ontologia | Preview del payload completo y `yes` antes de cada intento de escritura; un fallo consume ese intento |
| Osmos | Intake, capacidad y contrato final aceptados antes de crear/arrancar la unica tarea |
| Cambio de alcance | Otra decision si cambian destinos, version, recursos, permisos o acciones destructivas |

No son excusas para entregar solo documentos: despues de cada aprobacion se
realizan las operaciones correspondientes y se comprueba su persistencia.

## 4. Ejecutar por dependencias

Sigue los [modulos](modulos-avanzados.md). En Spark, el constructor local:

```powershell
python -m tools.build_deployment_notebook --schema "<esquema descubierto>" --lakehouse-id "<ID descubierto>" --output "<ruta privada absoluta>\base_analitica.ipynb"
```

Copilot rellena esos valores con descubrimiento real. El archivo debe quedar
**fuera del repositorio**, pues contiene el ID aprobado; no reemplaza archivos.
Para Lakehouse sin esquemas, el argumento schema es una cadena vacia.
El directorio privado de destino debe existir.

El constructor solo guarda un archivo local. Con `spark-cli`, Copilot crea
el item Notebook, aplica su definicion y binding al Lakehouse confirmado,
verifica la definicion y arranca el job. El notebook comprueba el Lakehouse
esperado, valida esquemas, perfila, limpia, reconcilia y **publica al ejecutarse**.
No hay un parametro `WRITE_ANALYTICS=False` que deje el despliegue a medias.
No cambies los parametros del job respecto del alcance aprobado.

Sondea LRO/jobs con los tiempos indicados por el servicio hasta estado final.
202 o "job iniciado" no son exito final. Relee tablas/definiciones/items y valida.
Los IDs/bindings se inyectan en los artefactos de despliegue privados, nunca
en el notebook generador versionado ni en las plantillas publicas.

## 5. Evidencias de aceptacion

| Entrega | Evidencia necesaria |
|---|---|
| Base analitica | Job final correcto; perfil raw/sin copias; tres tablas releidas; filas, unidades e ingresos reconciliados |
| Modelo | Item/conexion reales, relaciones/medidas releidas, DAX contrastado con Spark bajo los mismos filtros |
| Informe | Item publicado y enlazado al modelo correcto; dos paginas, visuales y filtros revisados |
| Ontologia | Definicion releida con tres entidades, dos relaciones, claves y bindings correctos; no prometer chat V2 sobre V1 |
| Data Agent | Item configurado, publicacion confirmada y casos reales evaluados por su endpoint |
| Native App | Item desplegado, URL publicada con SSO y consulta real a traves del conector desplegado |

Anota por entrega nombre, ID/enlace privado, accion, estado final, comprobacion
y siguiente bloqueo si existe. Usa **creado / ejecutado / validado / bloqueado**;
un fichero JSON o una respuesta convincente no cuentan como artefacto validado.
No rellenes cifras observadas con `expected-results.json`.

## 6. Reanudar sin sobrescribir

No prometas una transaccion para todo el taller. Registra cada item creado
antes de avanzar. Si se pierde una respuesta de creacion, lista y relee antes
de considerar otro intento; no dupliques recursos.

Si una tabla derivada existe, el notebook se detiene antes de escribir ninguna.
Tras fallo parcial, inspecciona las tres tablas y el job: no relances todo ni
borres para despejar el error. Si las tres estan completas, validadas y pertenecen
a esta ejecucion, continua desde el modelo sin volver a publicarlas. Si no,
explica el estado y pide elegir otra ubicacion o una reparacion con alcance
explicito. No cambies silenciosamente los nombres del contrato.

Los bloqueos de ontologia, Apps u Osmos no invalidan lo creado en otras ramas.
No marques completo "todo" si falta alguna. Al terminar, deten las sesiones
Spark; retirar recursos o permisos es otra operacion que requiere aprobacion.
