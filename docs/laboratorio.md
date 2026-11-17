# Laboratorio: dile el workspace y construye con Copilot

Abre la raiz del repo. Completa la [preparacion](preparacion.md).
Cada bloque es un prompt para Copilot, no un comando que se autoejecute.
Los nombres reales y evidencias se quedan en tu sesion privada.

## 1. Conectar por nombre y decidir el alcance

```text
Mi workspace es "<nombre de tu workspace>". Quiero desplegar el taller completo.
Usa workshop-ventas. Lee docs/datos.md, docs/contrato-analitico.md y
docs/despliegue.md. Explica brevemente instrucciones, skills y herramientas.
Te autorizo a descubrir ese workspace, items, capacidad y esquemas en lectura.
Resuelve los IDs, comprueba los permisos y prepara el inventario de despliegue.
Si hay varios Lakehouses, pide elegir. Quiero un Lakehouse dedicado al taller.
Si faltan datos, incluye crear el Lakehouse necesario e importar y ejecutar
el notebook 01 sin modificarlo. No escribas antes de presentar el alcance.
```

Copilot debe mostrar un destino real y los requisitos por artefacto, no afirmar
que tiene acceso solo porque conoce una skill. Revisa colisiones, capacidad,
servicios preview, nombres y costes de ejecucion.

## 2. Aprobar e iniciar

Elige **una** ruta de ingenieria: [Spark](modulos/03-base-analitica.md)
o [Project Osmos](modulos/04-project-osmos.md). Tras revisar el plan:

```text
Apruebo el inventario de creacion, ejecucion y validacion que acabas de mostrar.
Elijo Spark para la base analitica. Ejecuta las operaciones aprobadas en ese
workspace/Lakehouse y continua despues con modelo, informe, ontologia, Data
Agent y App. No quiero solo codigo ni instrucciones manuales.
Respeta los gates especificos de cada skill. No instales nada no acordado,
no sobrescribas, borres, compartas ni cambies permisos o capacidad.
```

Si prefieres Osmos, sustituye la eleccion; Copilot verifica elegibilidad e
intake antes de lanzar una unica tarea. La aprobacion no elimina las revisiones
obligatorias del informe o de la ontologia.

## 3. Crear, ejecutar y entender la base

```text
Continua el alcance aprobado usando spark-cli en modo authoring.
Usa las fuentes del repo y tools/build_deployment_notebook.py para construir
el notebook operativo fuera del repo, con esquema y Lakehouse descubiertos.
Crealo como workshop_03_base_analitica, vincula el Lakehouse y ejecutalo.
Comprueba primero el esquema. Necesito raw, sale_id distintos, copias,
nulos, cantidades invalidas y productos/tiendas huerfanos. Separa incidencias
raw de las observadas sin copias; si hay versiones de un sale_id, detente.
Publica los tres destinos exactos aprobados, sin overwrite. Espera al job,
relee las tablas y reconcilia filas, unidades e ingresos decimales.
```

Copilot no debe quedarse en una celda con escritura desactivada. El notebook
se ejecuta tras la aprobacion, recupera categoria/ciudad de dimensiones y guarda
Delta. Las fuentes raw no se modifican. Compara los resultados observados con
el informe real del generador; el JSON solo aplica a su configuracion original.

Para contrastar por otra herramienta:

```text
Usa sqldw-cli y el SQL analytics endpoint descubierto del mismo Lakehouse.
Ejecuta descubrimiento de esquema, perfilado, validacion de claves y resumen
de sql/ en ese orden, cada SELECT por separado. Adapta el esquema al real.
Si falla la validacion de claves, detente antes del resumen.
Compara ingresos por categoria con Spark bajo los mismos filtros.
```

Estas consultas son de lectura. T-SQL no escribe las tablas Delta.

## 4. Crear el modelo y el informe

```text
Continua el modulo 05. Con semantic-model-authoring, crea y despliega
workshop_ventas_model Direct Lake desde las tablas validadas. Aplica las
relaciones, nombres y medidas de plantillas/modelo-semantico.json.
Ejecuta validar-modelo.dax y contrasta con Spark.
Despues usa powerbi-report-cli para planificar el informe de dos paginas
de plantillas/informe.json. Guarda la especificacion y pide mi aprobacion.
```

Revisa y aprueba la especificacion en **otro turno**. Entonces:

```text
Apruebo la especificacion del informe que acabas de guardar.
Continua el diseno y autoria, valida el PBIR, revisa la previsualizacion
y publica workshop_ventas_report vinculado al modelo confirmado.
Comprueba paginas, visuales, filtros y totales en el informe publicado.
```

## 5. Desplegar las ramas de negocio

```text
Continua los modulos 06, 07 y 08 dentro del alcance aprobado:
ontologia con ontology-cli, Data Agent con SDK/REST oficial y Native App
con Fabric Apps/Rayfin. No uses FabricIQ para crear informes ni Osmos para
crear estos items. Comprueba las versiones y presenta los gates requeridos.
Si falta instalar una herramienta, pide aprobar los paquetes y destino.
Ejecuta y verifica lo soportado; un bloqueo de una rama no para las demas.
```

En ontologia revisa la version y preview antes del `yes` exigido por la skill.
En Data Agent comprueba publicacion **y** respuestas reales. En Native App
revisa los recursos que `up` aprovisiona y valida la URL publicada con SSO.
No basta un JSON, un chatbot simulado o una pantalla local.

## 6. Cerrar o reanudar con evidencia

```text
Muestra el inventario final con nombres, enlaces privados, estado real y
comprobacion realizada. Separa creado, ejecutado, validado y bloqueado.
Explica cualquier diferencia con el plan, que recursos consumen capacidad
y como detener las sesiones. No borres recursos.
```

Para reanudar otra sesion, indica el mismo workspace y pide descubrir/verificar
lo ya creado antes de continuar. No vuelvas a ejecutar el publicador sobre
tablas existentes. Sigue [el procedimiento de reanudacion](despliegue.md).
