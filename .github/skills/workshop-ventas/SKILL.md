---
name: workshop-ventas
description: Guia el taller de ventas y sus modulos de base analitica, Project Osmos, Power BI, ontologia, Data Agent y Native App. No sustituye a las Microsoft Fabric Skills oficiales.
---
# Ejercicio guiado de ventas

Esta es una skill LOCAL del taller, no una skill oficial de Microsoft.
Orquesta el contexto educativo; para APIs y codigo Fabric utiliza las skills
oficiales instaladas. No las instala ni proporciona herramientas o autenticacion.

1. Lee `docs/datos.md` y `docs/laboratorio.md` antes de proponer una solucion.
2. Pregunta si se quiere generar codigo local o actuar contra un entorno Fabric.
   Si se pide actuar, confirma Lakehouse/endpoint y herramientas disponibles.
   No descubras ni cambies recursos remotos por iniciativa propia.
3. Para notebooks/PySpark usa la skill oficial `spark-cli`, si esta disponible.
   Para T-SQL de solo lectura usa `sqldw-cli`, si esta disponible.
   Si falta, declara la limitacion en vez de simular haberla usado.
4. Empieza por perfilado: filas, claves distintas, copias, nulos, cantidades
   invalidas y relaciones huerfanas. Distingue incidencias raw y ventas unicas.
5. Propone reglas antes de generar la transformacion. Usa dimensiones canonicas,
   decimal y redondeo por linea. Las cancelaciones quedan fuera de ingresos.
6. Espera aprobacion antes de ejecutar cambios remotos o sobrescribir archivos.
   Generar codigo no significa ejecutarlo; una respuesta no prueba un resultado.
7. Pide al asistente del taller que compare con el informe del notebook 01.
   No abras `soluciones/` salvo que el usuario pida ver la solucion.
8. Explica como comprobar recuentos, unicidad e ingresos. Si no has ejecutado,
   declara que el resultado es una propuesta pendiente de validacion.

## Ampliaciones opcionales

Lee `docs/modulos-avanzados.md`, `docs/contrato-analitico.md` y el modulo elegido.
Reutiliza el modo local/manual/conectado que haya indicado el usuario; no vuelvas
a preguntar si ya esta resuelto. La preparacion local no autoriza descubrimiento,
autenticacion ni ejecucion remota.

- 03 o 04 publican los mismos tres destinos: son alternativas, no dos cargas
  consecutivas. Conserva el generador y las fuentes originales.
- Para 04 utiliza `project-osmos`, si esta disponible, con un encargo completo
  de ingenieria. Verifica sus requisitos y aprobacion antes de iniciar una tarea.
- Para 05 utiliza `semantic-model-authoring` para el modelo. El informe tiene
  ruta manual; no uses FabricIQ como si fuera autoria de informes.
- Para 06 comprueba version y alcance de `ontology-cli`: no puede crear V2
  mediante el flujo legacy V1 disponible al preparar el taller.
- Para 07 separa metadata/Prep for AI del modelo e instrucciones del Data Agent.
  No inventes una skill de creacion ni pares Example queries para modelo semantico.
- Para 08 sigue Fabric Apps/Rayfin y el scaffold oficial, sin crear un supuesto
  item App con un HTML local. Dev/up pueden aprovisionar backend en Fabric.
- Usa las referencias de soluciones solo cuando se soliciten. Las plantillas
  de diseno no son payloads oficiales ni prueba de un recurso creado.
