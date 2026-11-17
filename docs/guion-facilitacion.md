# Guion de facilitacion: 60 minutos

## Preparacion previa

- Prueba el notebook en tu capacidad Fabric y confirma las tres tablas y el
  esquema antes de la sesion. Este repo no crea recursos por ti.
- Prepara VS Code con una de las rutas de instalacion de skills y el repo abierto.
- Ten el notebook 01 descargado y un Lakehouse limpio de reserva.
- Si usaras conexion en vivo, prueba autenticacion, herramientas y permisos.
  No dependas de ella: la ruta de generacion local cubre el objetivo del taller.
- Mantiene la solucion separada hasta que hayas explicado las reglas.
- No muestres tokens, tenants privados, otros workspaces ni datos de terceros.

## Agenda

| Minutos | Que mostrar | Mensaje |
|---|---|---|
| 0-10 | Chat y primer prompt | Copilot necesita contexto y revision |
| 10-20 | Instrucciones, skill local y skills oficiales | Instrucciones no son herramientas ni permisos |
| 20-25 | Parametros e informe del notebook 01 ya preparado | Datos ficticios, repetibles y con errores conocidos |
| 25-35 | Prompts 1-2 del laboratorio | Perfilar antes de modificar |
| 35-45 | Prompts 3-4 y ejecucion manual revisada | Reglas de negocio y comprobaciones |
| 45-50 | Resultado por categoria, referencia si hace falta | Generar, ejecutar y validar son pasos distintos |
| 50-60 | Preguntas y cierre | Como repetirlo en un Lakehouse propio |

El arranque de Spark y la generacion se preparan antes de la sesion.
Si tienes que generarlos en directo, recorta el bloque SQL opcional, no la
explicacion de permisos ni la validacion.

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
