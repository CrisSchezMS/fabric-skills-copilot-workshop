# Guion de facilitacion: 60 minutos

## Preparacion previa

- Prueba el notebook en tu capacidad Fabric y confirma las tres tablas y el
  esquema antes de la sesion. Este repo no crea recursos por ti.
- Prepara VS Code con una de las rutas de instalacion de skills y el repo abierto.
- Ten el notebook 01 descargado y un Lakehouse limpio de reserva.
- Si usaras conexion en vivo, prueba autenticacion, herramientas y permisos.
  No dependas de ella: la ruta de generacion local cubre el objetivo del taller.
- Para mostrar el resultado completo, prepara un modelo/informe validado
  y, opcionalmente, una Native App en un entorno de demostracion dedicado.
  Etiquetalos como preparados antes de la sesion, no creados en directo.
- Mantiene la solucion separada hasta que hayas explicado las reglas.
- No muestres tokens, tenants privados, otros workspaces ni datos de terceros.

## Agenda

| Minutos | Que mostrar | Mensaje |
|---|---|---|
| 0-8 | Objetivo, primer prompt y skills | Crear artefactos exige contexto, herramientas y revision |
| 8-18 | Informe del generador y perfilado | Filas raw no son ventas unicas ni pedidos |
| 18-30 | Reglas y limpieza en memoria | Dimensiones canonicas, decimal y comprobaciones |
| 30-42 | Plan de base analitica del modulo 03 | Granularidad, tres destinos y escritura protegida; publicar solo tras aprobacion |
| 42-53 | Consumo en un modelo/informe preparado | Mismas medidas y filtros; identificar que ya existia |
| 53-60 | Elegir siguiente modulo y cierre | Osmos, modelo/informe, ontologia, agente o Native App |

El arranque de Spark y la generacion se preparan antes de la sesion. No intentes
construir todos los artefactos en una hora con principiantes. El bloque de
publicacion puede quedar como codigo revisado si no hay tiempo o autorizacion.
Si generas datos en directo, recorta el bloque de consumo, no permisos ni validacion.

## Continuacion por modulos

Usa [el mapa avanzado](modulos-avanzados.md) para organizar sesiones posteriores.
03 y 04 comparan Spark guiado y Osmos para el mismo resultado de ingenieria.
05 construye desde cero el modelo y las dos paginas que se mostraron preparadas.
06 representa el negocio con entidades y relaciones. 07 evalua un agente contra
referencias observadas; 08 crea una App real con SSO y conector al modelo.

En cada entrega pide mostrar el artefacto, su fuente, la validacion y que
autorizacion permitio crearlo. Para Osmos no basta mostrar una tarea arrancada;
para Native App no basta mostrar una pantalla local; para Data Agent no basta
una respuesta verosimil. Las limitaciones de previews se convierten en estados
pendientes, no en un motivo para inventar APIs o saltar permisos.

## Mini-demo de personalizacion

Abre `.github/copilot-instructions.md` y luego `sql.instructions.md`.
Explica `applyTo` con un archivo `.sql` y un `.ipynb`.
Los globs se refieren a los archivos del repo, no a las tablas del workspace.
Muestra la skill local `workshop-ventas` como ejemplo pequeno, diferenciandola
del paquete oficial. No la presentes como una proteccion ejecutable.

No anadas archivos por acumular formatos: no hay CLAUDE.md/GEMINI.md duplicados,
ni servidores MCP activados por defecto, ni tokens de ejemplo.
Los prompts son texto copiable en `docs/laboratorio.md`, sin depender de un
formato de slash commands concreto del cliente.

## Plan alternativo

Si no hay capacidad o conexion, muestra los notebooks sin ejecutarlos y genera
codigo con Copilot usando el contrato local. El JSON de resultados es una
referencia calculada con datos sinteticos, no una prueba de una ejecucion en vivo.
Declara explicitamente que esa parte de la demo no se ha ejecutado en Fabric.

Si Copilot propone un mal join, elimina nulos recuperables o usa float,
conviertelo en aprendizaje: vuelve a las reglas y pide una correccion antes de
ejecutar. No pulses aceptar todo para intentar ganar tiempo.

Al finalizar, detened las sesiones Spark desde Fabric. Si se quieren eliminar
recursos del taller, que cada participante revise y borre solo su propio
Lakehouse/notebook; no hay script de borrado automatico.
