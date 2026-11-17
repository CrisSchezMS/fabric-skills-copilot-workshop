# Facilitacion: construir en Fabric con Copilot

## Preparacion obligatoria

Prueba autenticacion, skills, capacidad y permisos antes del taller.
Cada participante debe conocer **el nombre de su workspace**, no sus IDs.
Prepara un Lakehouse dedicado por persona y verifica las previews elegidas.
No dependas de instalar herramientas durante una demo cronometrada.

El notebook generador se conserva intacto. Puede ejecutarse antes o mediante
Copilot al iniciar, con aprobacion. No presentes datos/artefactos preparados
por facilitacion como si se hubieran desplegado en directo.

## Primera sesion: un bloque conectado de 60 minutos

| Minutos | Accion real | Aprendizaje |
|---|---|---|
| 0-10 | Nombre del workspace, descubrimiento y preflight | Skills no son permisos; no hace falta copiar IDs |
| 10-18 | Inventario y aprobacion del alcance | Autorizar un despliegue concreto permite avanzar |
| 18-40 | Crear y ejecutar notebook Spark o tarea Osmos | Perfilado, copias, conflictos, dimensiones y decimal |
| 40-53 | Releer las tres tablas y reconciliar | Una respuesta o job iniciado no prueban una entrega |
| 53-60 | Inventario de evidencias y siguiente bloque | Reanudar desde lo validado sin sobrescribir |

Si Spark/Osmos tarda mas, conserva la identidad del job/tarea y continua su
seguimiento en la siguiente sesion. No declares exito ni uses cifras de
referencia como si fueran observadas para cumplir el horario.

## Siguientes sesiones

1. Modelo Direct Lake y dashboard Power BI. Reserva el turno de aprobacion de
   especificacion del informe que exige la skill antes de construir/publicar.
2. Ontologia. Declara V1/V2 y muestra preview antes de cada `yes`; verifica
   entidades/relaciones/bindings, sin prometer chat V2 sobre V1.
3. Data Agent. Crear/configurar/publicar desde SDK o REST y evaluar casos reales.
4. Native App. Copilot genera proyecto Rayfin, integra conector, compila,
   despliega y prueba la URL publicada con SSO.

Usa [el mapa](modulos-avanzados.md) y [el runbook](despliegue.md).
Pide en cada bloque mostrar item, origen, operacion final y evidencia.
Para Osmos no basta tarea arrancada; para App no basta una pantalla local;
para Data Agent no basta una respuesta verosimil.

## Explicar Copilot sin conocimientos previos

Muestra instrucciones del repo, `applyTo` y skill local. Explica que sus
reglas aportan contexto, las skills oficiales aportan procedimientos y las
herramientas autenticadas actuan con los permisos de la identidad.
Los prompts son texto normal del [laboratorio](laboratorio.md).

No pulses aceptar todo ni desactives protecciones para ganar tiempo.
Ante un mal join, float o rechazo de nulos recuperables, vuelve al contrato.
Ante bloqueo de preview, continua las ramas independientes y marca la pendiente.

## Fallos, cierre y costes

Sin conexion o permiso, diagnostica el bloqueo concreto; no conviertas la
sesion en generacion offline y la declares completada. Puedes explicar codigo
para aprender, pero la entrega conectada sigue pendiente.
No muestres otros workspaces, tokens ni datos de terceros.

Conserva las evidencias privadas y deten sesiones Spark al terminar.
La limpieza de recursos no es automatica: requiere revisar nombres y aprobar
la eliminacion especifica. No se incluyen scripts de borrado masivo.
