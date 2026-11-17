# Desarrollo y validacion

El recorrido del participante es conectado: [despliegue](despliegue.md).
Estas instrucciones son para mantener el repo, no para sustituir esa ejecucion.

## Fuentes y artefactos

| Fuente | Funcion |
|---|---|
| `src/synthetic_data.py`, `src/fabric_tables.py` | Generador y esquemas originales, conservados |
| `src/profile_sales.py` | Esquema primero; contadores raw y sin copias separados |
| `src/transform_sales.py` | Limpieza, conflictos, dimensiones e importe decimal |
| `src/analytics_sales.py` | Agregado, calendario, reconciliacion y escritura protegida |
| `tools/build_notebooks.py` | Unico notebook distribuido: generador; resultados de referencia |
| `tools/build_deployment_notebook.py` | Notebook operativo autonomo que Copilot despliega/ejecuta |

No edites solamente un `.ipynb`. El constructor de despliegue inserta fuentes,
esquema e ID de Lakehouse reales, por lo que su salida se guarda **fuera del repo**
en una ruta privada nueva. Valida el Lakehouse al ejecutarse y publica sin un
flag de escritura desactivado. La autorizacion se obtiene antes de arrancarlo.
Los helpers de escritura mantienen la aprobacion explicita y `errorifexists`.
El generador distribuido no incorpora ese contexto y se conserva sin cambios.

## Comandos locales desde la raiz

Python 3.11 para desarrollo; Java 17 y PySpark para integracion.
Instala dependencias en un entorno dedicado cuando corresponda, nunca dentro
del notebook de ventas para arreglar una edicion:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m ruff format src tools tests
python -m tools.build_notebooks
python -m ruff check .
python -m tools.build_notebooks --check
python -m unittest discover -s tests -v
node --test tests\test_native_app.mjs
```

Spark local opt-in:

```powershell
$env:RUN_SPARK_TESTS = "1"
python -m unittest discover -s tests -v
Remove-Item Env:RUN_SPARK_TESTS
```

CI usa Spark 3.5 y no consulta Fabric. Las pruebas cubren determinismo,
reglas de negocio, conflictos, redondeo, perfiles raw/sin copias, destinos,
reconciliacion y codigo autonomo. El notebook operativo se prueba en memoria,
con lectura de catalogo y escritura remota sustituidas, sin crear tablas reales.
No se necesitan SDK de Data Agent, Rayfin, tokens ni secretos de CI.
El test Node comprueba el adaptador con fixtures; no despliega una App.

## Aceptacion remota antes de impartir

En un workspace de prueba **autorizado**, recorre el laboratorio completo:
descubrimiento por nombre, inventario, aprobacion y despliegues reales.
Comprueba generador, notebook/job analitico, tablas, modelo, informe,
ontologia, Data Agent y App segun los criterios de cada modulo.
Si algun componente no esta disponible, registra su bloqueo y no certifiques
ese tramo como probado. Las pruebas locales no demuestran permisos ni previews.

Para comprobar SQL, descubre esquema y ejecuta cada SELECT por separado;
no uses T-SQL para escribir Delta. Conserva evidencias privadas y no publiques
exportaciones Fabric con outputs, IDs o bindings. No uses `dev/up` de Rayfin
como validacion local inocua. Deten sesiones al terminar; no borres recursos
automaticamente ni desactives protecciones para repetir el taller.
