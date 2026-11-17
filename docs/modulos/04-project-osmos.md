# 04 - Delegar un resultado completo a Project Osmos

**Objetivo:** comparar escribir y ejecutar celdas con encargar a un agente remoto
un resultado completo de ingenieria: inspeccion, notebook, tablas y validaciones.
Osmos no se usa aqui para crear informes, ontologias, Data Agents ni Native Apps.

## Preparacion

Usa `project-osmos` desde Copilot CLI local, si esta instalada. Necesitas un
Lakehouse que contenga las tres tablas originales y **ninguno de los tres
destinos derivados**. Si ya completaste 03, prepara otro entorno de taller:
no borres tablas para que este modulo funcione.

En produccion publica, la skill exige comprobar asignacion actual y SKU.
Una capacidad trial confirmada `FTL64` bloquea su ejecucion; un SKU no trial
no garantiza toda la elegibilidad de IA. La falta de visibilidad de capacidad
no prueba que sea trial ni elegible. No se cambia capacidad ni se evita el control.
Comprueba siempre las reglas de la version instalada.

## Plan primero, ejecucion despues

```text
Usa project-osmos solo para preparar un encargo, sin autenticarte ni consultar
Fabric. Lee docs/datos.md, docs/contrato-analitico.md y
plantillas/encargo-osmos.txt. Explica origenes, destinos, permisos, coste,
artefactos de salida y como verificarias las reglas. Conserva todo el resultado
de ingenieria en una unica tarea. No la crees ni la arranques.
```

Revisa el [encargo de referencia](../../plantillas/encargo-osmos.txt).
Las tablas raw siguen siendo fuentes de solo lectura. El prefijo permitido
no basta: el encargo limita las escrituras a **tres nombres exactos**.

Si quieres ejecutar, proporciona los nombres reales de workspace/Lakehouse
fuera del repositorio o elige el contexto confirmado y autoriza su descubrimiento.
No pegues tokens. La creacion y arranque de una tarea requieren otra aprobacion,
despues de revisar el contrato de ejecucion que prepare la skill.

```text
Quiero pasar del plan a una ejecucion de Project Osmos en mi entorno de taller.
Antes de crear o arrancar la tarea, confirma conmigo el workspace y Lakehouse,
verifica requisitos con la skill y presenta el encargo completo, los tres
destinos y el notebook de salida. No reemplaces recursos existentes.
Espera mi aprobacion del contrato final; no interpretes este mensaje como
autorizacion para instalar herramientas o cambiar permisos/capacidad.
```

## Evidencia y seguimiento

Tras un arranque autorizado, conserva el identificador de la tarea remota y
su enlace de Fabric fuera del repo. Pide estado y mensajes de **esa misma tarea**.
Una tarea local de Copilot no es una tarea Osmos. No crees otra para reintentar
un fallo o para cada tabla.

Compara los resultados capturados por el servicio con el informe del notebook
01: detalle unico, cantidades y relaciones validas, ingresos decimales,
agregado reconciliado y calendario continuo. Comprueba tambien que el notebook
se guardo donde se acordo y que no hubo mutaciones en las tablas originales.
Un texto que diga "terminado" no sustituye estas evidencias.

**Cierre:** distingue contrato aceptado, tarea arrancada y artefactos comprobados.
Una cancelacion o borrado de tarea requiere su propia confirmacion; no se
incluyen scripts de borrado. Sin elegibilidad o conexion, completa el encargo
offline y usa 03 como alternativa explicita, no como una ejecucion Osmos simulada.
