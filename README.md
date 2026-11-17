# GitHub Copilot + Microsoft Fabric Skills: tu primera demo

Workshop de **60 minutos**, en espanol, para personas que estan empezando con
Microsoft Fabric y no han utilizado GitHub Copilot.

**Caso:** preparar las ventas de una tienda ficticia, detectar errores de calidad
y calcular ingresos por categoria usando Copilot y las Fabric Skills.
Todos los datos se generan desde cero; no se usan datos de personas ni empresas.

## Empieza por aqui: genera tus datos

No necesitas instalar Python, Git ni Copilot para este primer paso.

1. Descarga [01_generar_datos_sinteticos.ipynb](https://raw.githubusercontent.com/CrisSchezMS/fabric-skills-copilot-workshop/main/notebooks/01_generar_datos_sinteticos.ipynb)
   (en GitHub tambien puedes abrir el archivo y elegir **Download raw file**).
2. En un workspace de Fabric con capacidad activa, crea un **Lakehouse vacio
   dedicado al taller**, por ejemplo `lh_workshop_ventas`. Necesitas permisos
   para crear notebooks y escribir tablas; no necesitas ser administrador.
3. Importa el `.ipynb` en Fabric como notebook y adjunta ese Lakehouse como
   **predeterminado**. Usa el kernel **PySpark**.
4. Revisa la celda de parametros. Para Lakehouses con esquemas deja
   `SCHEMA = "dbo"`; para uno antiguo sin esquemas usa `SCHEMA = ""`.
5. Pulsa **Ejecutar todo**. No hacen falta paquetes adicionales ni conexion a
   origenes externos. Comprueba el informe final y las tres tablas en **Tables**.

| Tabla | Contenido por defecto |
|---|---|
| `workshop_products` | 12 productos en 4 categorias |
| `workshop_stores` | 4 tiendas ficticias |
| `workshop_sales_raw` | 10.200 filas: 10.000 ventas y 200 copias exactas |

El notebook incorpora sus funciones: se puede compartir y ejecutar por separado,
sin descargar el resto del repositorio. La semilla y las fechas fijas permiten
reproducir la misma demo. Introduce errores controlados para practicar su deteccion.

**Proteccion:** si alguna tabla ya existe, se detiene antes de escribir ninguna.
Para repetir, usa otro Lakehouse o revisa y cambia `ALLOW_OVERWRITE = True`.
La sobrescritura reemplaza solo esas tres tablas, incluidos sus esquemas.
Las tres escrituras no son atomicas: un fallo puede dejar una carga parcial.
La demo consume capacidad Fabric; deten la sesion Spark desde la interfaz al acabar.

## Prepara Copilot y las Fabric Skills

Abre este repositorio como carpeta en VS Code, no solo el notebook suelto:

```powershell
git clone https://github.com/CrisSchezMS/fabric-skills-copilot-workshop.git
Set-Location fabric-skills-copilot-workshop
code .
```

Consulta [la preparacion paso a paso](docs/preparacion.md). Hay dos rutas:

- **Copilot CLI en la terminal de VS Code:** instalacion oficial mediante plugin.
- **Chat de VS Code:** instalacion de las skills con APM; el modo basico solo
  genera codigo y no requiere conectar MCP ni dar acceso al workspace.

No confundas las **instrucciones del repo**, las **skills especializadas** y las
**herramientas/autenticacion**. Clonar este repo no instala las Fabric Skills,
no concede permisos y no conecta con tu tenant. Nada se autoejecuta al abrirlo.

## Material incluido

| Archivo o carpeta | Para que sirve |
|---|---|
| [Notebook 01](notebooks/01_generar_datos_sinteticos.ipynb) | Generar datos y guardar las tres tablas Delta |
| [Preparacion](docs/preparacion.md) | Requisitos, instalacion y comprobaciones previas |
| [Laboratorio](docs/laboratorio.md) | Prompts copiables para explorar, planificar y limpiar |
| [Guion de 60 minutos](docs/guion-facilitacion.md) | Orden de la demo, tiempos y plan alternativo |
| [Contrato de datos](docs/datos.md) | Columnas, incidencias y reglas de negocio |
| [Resultados esperados](docs/expected-results.json) | Recuentos e ingresos con la configuracion original |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Contexto general que se comparte con Copilot |
| [.github/instructions/](.github/instructions) | Reglas especificas para SQL, PySpark y notebooks |
| [Skill local del taller](.github/skills/workshop-ventas/SKILL.md) | Ejemplo original de una skill que guia el ejercicio |
| [SQL](sql/) | Descubrimiento, perfilado, validacion de claves y resumen T-SQL |
| [Solucion opcional](soluciones/02_limpiar_y_analizar.ipynb) | Referencia PySpark; lee datos, no guarda tablas |
| [Desarrollo](docs/desarrollo.md) | Fuentes, regeneracion y pruebas locales/CI |

La skill local **no es una Microsoft Fabric Skill oficial** y no sustituye su
instalacion. No se incluyen copias de las skills oficiales ni configuraciones
con credenciales. Las recomendaciones de extensiones de VS Code son opcionales.

## Primer prompt

```text
Soy principiante en Fabric y GitHub Copilot. Lee las instrucciones de este
repositorio y el contrato de datos. Dime que skills tienes disponibles.
Usa spark-cli, si esta instalada, para proponer como perfilar las tres tablas
del taller. No inventes columnas ni resultados. No ejecutes ni modifiques
nada todavia. Si no tienes conexion con Fabric, trabaja solo con los archivos
locales y explicame como ejecutar la propuesta en mi notebook.
```

**Importante:** generar codigo no significa haberlo ejecutado. Las instrucciones
son orientaciones al modelo, no una barrera de seguridad. Revisa destinos,
permisos y cambios antes de autorizarlos.

## Fuentes y limites

- [Microsoft Fabric Skills oficiales](https://github.com/microsoft/skills-for-fabric)
- [Instrucciones personalizadas en VS Code](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [Notebooks en Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)
- [SQL analytics endpoint](https://learn.microsoft.com/en-us/fabric/data-warehouse/sql-analytics-endpoint-performance)

Los notebooks se distribuyen sin ejecutar y sin bindings a un workspace.
Las pruebas locales no equivalen a una ejecucion en tu capacidad Fabric.
Consulta las notas de [desarrollo](docs/desarrollo.md).

Licencia [MIT](LICENSE). Material educativo independiente; no es un producto
oficial ni implica garantias de Microsoft o GitHub.
