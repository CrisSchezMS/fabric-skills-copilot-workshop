# 04 - Copilot encarga y ejecuta la ingenieria con Project Osmos

**Entrega:** una tarea Osmos real que inspecciona las tres fuentes, guarda
`workshop_03_base_analitica` y publica las tres tablas derivadas reconciliadas.
Es una alternativa al [modulo 03](03-base-analitica.md), no otro paso posterior.

## Elegibilidad y contrato

Usa la skill `project-osmos` desde Copilot CLI local. Antes de crear una tarea,
comprueba asignacion actual de capacidad y requisitos de servicio mediante el
preflight de la skill. Una trial confirmada `FTL64` bloquea su ejecucion en
produccion publica; no ver la capacidad no prueba ni trial ni elegibilidad.
Un SKU no trial tampoco garantiza todos los requisitos de IA.

Los tres destinos y el notebook deben estar ausentes. Si ya completaste Spark,
continua desde el modelo o elige explicitamente otro Lakehouse de taller con
sus datos originales; no borres tablas para probar Osmos.

```text
Elijo Project Osmos para la base analitica del workspace/Lakehouse confirmados.
Usa project-osmos y su preflight real. Lee plantillas/encargo-osmos.txt y los
dos contratos de datos. Completa el intake y presentame el contrato final:
una unica tarea con inspeccion, notebook, tres tablas y validaciones.
Tras mi aprobacion del contrato, crea y arranca esa tarea remota y sigue su
estado. No me entregues solo el texto del encargo.
```

El contrato de [referencia](../../plantillas/encargo-osmos.txt) fija fuentes,
reglas, tipos y nombres exactos. Copilot incorpora los destinos descubiertos
y explica consumo de capacidad antes de pedir la aprobacion requerida.
Osmos no crea informes, ontologias, Data Agents ni Apps en este encargo.

## Ejecutar y seguir la misma tarea

Una vez aprobado el contrato, usa las operaciones reales de la skill para
crear/arrancar. Conserva ID, enlace y mensajes privados de **esa tarea**.
No uses las APIs de agentes locales de Copilot como si consultaran Osmos.
No crees una tarea por capa ni otra para reintentar un fallo ambiguo.

Si requiere decisiones durante la ejecucion, contesta con el contrato; una
ampliacion de destino necesita aprobacion. No permitas sobreescritura ni
cambios de permisos/capacidad para avanzar.

## Aceptacion

Comprueba en el servicio tarea finalizada, notebook guardado y tres tablas
releidas. Valida claves, copias/conflictos, filtros de negocio, importe decimal,
sumas del agregado y calendario continuo. Contrasta con el generador real.
Un mensaje "terminado" no sustituye lectura y comprobaciones de artefactos.

Informa si queda publicacion parcial y no la borres ni relances automaticamente.
Si Osmos esta bloqueado, ofrece elegir **Spark conectado**; no declares ejecutado
un encargo local. Tras validacion, continua el modelo y las ramas de negocio.
