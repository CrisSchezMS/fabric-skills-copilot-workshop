# Copilot + Fabric Skills: despliega una solucion de ventas

Taller en espanol para principiantes. **Indica el nombre de tu workspace y pide
a Copilot que construya alli la solucion**, usando las Microsoft Fabric Skills
y herramientas oficiales. Copilot descubre los recursos, comprueba acceso,
presenta el alcance, obtiene tu aprobacion, despliega, ejecuta y verifica.
No es un ejercicio de copiar celdas que se quedan sin ejecutar.

El caso es una tienda ficticia. Partiendo de tres tablas sinteticas se crean:

| Resultado en Fabric | Como lo construye Copilot |
|---|---|
| Notebook y tablas limpias, agregado diario y calendario | `spark-cli` **o** una tarea completa de `project-osmos` |
| Modelo estrella Direct Lake y cuatro medidas | `semantic-model-authoring` |
| Informe Power BI de dos paginas, el dashboard del taller | `powerbi-report-cli` |
| Ontologia con tres entidades y dos relaciones | `ontology-cli`, respetando su version soportada |
| Fabric Data Agent publicado y evaluado | SDK oficial o REST publico de Data Agent |
| Fabric Native App con SSO y consulta al modelo | Scaffold y CLI oficial Fabric Apps/Rayfin |

Las skills no conceden acceso. Hacen falta herramientas autenticadas, permisos,
capacidad y funcionalidades habilitadas. Si falta algo, Copilot identifica
**el bloqueo de ese artefacto** y sigue con las ramas disponibles; no inventa
un despliegue. Consulta los [requisitos](docs/preparacion.md) y
[limites de version](docs/referencias-avanzadas.md).

## 1. Abre el repositorio y prepara la conexion

```powershell
git clone https://github.com/CrisSchezMS/fabric-skills-copilot-workshop.git
Set-Location fabric-skills-copilot-workshop
copilot
```

Antes necesitas Copilot CLI y las Fabric Skills instaladas. Sigue
[Preparacion](docs/preparacion.md): la ruta principal es **conectada para cada
participante**, no una conexion opcional reservada a facilitacion.

Las instrucciones del repo aportan las reglas de negocio; la skill local
`workshop-ventas` coordina el recorrido; las skills oficiales aportan los
procedimientos de cada producto. Las herramientas y tu identidad ejecutan
las operaciones reales. Clonar este repo no autentica ni autoejecuta nada.

## 2. Da el nombre del workspace a Copilot

Copia este prompt y sustituye solo el nombre:

```text
Quiero desplegar el taller completo en mi workspace "<nombre de tu workspace>".
Usa workshop-ventas y las Microsoft Fabric Skills disponibles. Lee las
instrucciones, docs/datos.md, docs/contrato-analitico.md y docs/despliegue.md.

Te autorizo a descubrir ese workspace, sus items, capacidad y esquemas de
solo lectura. Resuelve los IDs tu, no me pidas que los copie. Si hay varios
Lakehouses, ayudame a elegir el dedicado al taller. Comprueba herramientas,
autenticacion, permisos y requisitos de cada artefacto.

Quiero crear y ejecutar, no solo recibir codigo: base analitica con Spark
o Project Osmos, modelo Direct Lake, informe Power BI, ontologia, Data Agent
y Fabric Native App. Si faltan los datos, incluye importar y ejecutar el
notebook generador sin modificarlo. Presenta nombres exactos, dependencias,
recursos y coste esperado de capacidad antes de pedir mi aprobacion.
Tras aprobar, despliega y verifica todo lo soportado. Respeta las revisiones
obligatorias del informe, ontologia y Osmos. No sobrescribas, borres ni
cambies permisos. Informa de los bloqueos concretos y de lo realmente creado.
```

El nombre es suficiente para **empezar el descubrimiento**, no para saltarse
ambiguedades o permisos. La aprobacion cubre el alcance mostrado; instalar
herramientas, cambiar permisos o ampliar el destino necesita otra decision.

## 3. Generador de datos: el notebook que se conserva

El [notebook 01](notebooks/01_generar_datos_sinteticos.ipynb) se mantiene
**sin cambios** y es el unico notebook distribuido. Copilot puede importarlo,
asignarle el Lakehouse predeterminado confirmado y ejecutarlo con `spark-cli`
tras aprobar ese alcance. Tambien puedes
[descargarlo](https://raw.githubusercontent.com/CrisSchezMS/fabric-skills-copilot-workshop/main/notebooks/01_generar_datos_sinteticos.ipynb)
e importarlo desde Fabric.

Requiere un Lakehouse vacio dedicado al taller, kernel PySpark y esquema
confirmado: `SCHEMA = "dbo"` para ese esquema existente o `""` sin esquemas.
No necesita paquetes externos. La configuracion original genera 12 productos,
4 tiendas y 10.200 filas raw: 10.000 lineas base y 200 copias exactas.
Son parametros del generador, **no resultados observados en tu workspace**.

Si existe alguna tabla de destino, se detiene antes de escribir.
En este recorrido no se activa `ALLOW_OVERWRITE`. Las escrituras no son
atomicas; cualquier carga parcial se inspecciona antes de decidir.

## Recorrido y materiales

| Material | Uso |
|---|---|
| [Laboratorio conectado](docs/laboratorio.md) | Conversacion completa: descubrir, aprobar, ejecutar y cerrar |
| [Runbook de despliegue](docs/despliegue.md) | Inventario, dependencias, gates, reanudacion y pruebas remotas |
| [Mapa de modulos](docs/modulos-avanzados.md) | Spark/Osmos, modelo/informe, ontologia, agente y App |
| [Contrato original](docs/datos.md) y [analitico](docs/contrato-analitico.md) | Tablas, granularidad y reglas sin inventar columnas |
| [Plantillas](plantillas/) | Disenos e instrucciones que Copilot convierte en artefactos reales |
| [Referencias de implementacion](soluciones/) | Decisiones de modelo, ontologia, agente y App |
| [Guion de facilitacion](docs/guion-facilitacion.md) | Sesion conectada y recorrido completo por bloques |
| [Desarrollo](docs/desarrollo.md) | Fuentes, constructor del notebook de despliegue y pruebas |

No se distribuyen notebooks de solucion para ejecutar a mano: Copilot genera
el notebook operativo desde `src/` con
`python -m tools.build_deployment_notebook`, lo despliega y lo arranca.
Los bindings y evidencias reales se guardan fuera del repositorio publico.
Los JSON de diseno no son payloads importables ni demuestran un despliegue.

Reserva varias sesiones para el recorrido completo; una hora permite
completar un bloque conectado, no garantiza todas las previews funcionando.
Osmos y Spark son alternativas para las mismas tablas, no cargas consecutivas.
La ontologia no bloquea el Data Agent ni la App, que reutilizan el modelo.

Las comprobaciones de este repo son locales. La validacion del despliegue
se obtiene de las respuestas de tu Fabric durante el taller. Al terminar,
deten las sesiones Spark; eliminar recursos requiere una decision explicita.

Fuentes: [Microsoft Fabric Skills](https://github.com/microsoft/skills-for-fabric)
y [documentacion de productos](docs/referencias-avanzadas.md).
Licencia [MIT](LICENSE). Material educativo independiente.
