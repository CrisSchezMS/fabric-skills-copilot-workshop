# Desarrollo y validacion

Los participantes solo necesitan importar el notebook en Fabric. Estas
instrucciones son para mantener o ampliar el repositorio.

## Fuente y notebooks autonomos

- `src/synthetic_data.py`: datos ficticios reproducibles y calculo de referencia
  con la biblioteca estandar.
- `src/fabric_tables.py`: esquemas Spark, validacion de nombres y escrituras protegidas.
- `src/transform_sales.py`: transformacion PySpark de referencia.
- `tools/build_notebooks.py`: ensambla el codigo en notebooks independientes y
  regenera el JSON de resultados con la configuracion original.

Cambiar solo un `.ipynb` no modifica su fuente. Regenera despues de editar fuentes.
Los notebooks publicados nunca deben contener salidas ni IDs del entorno.

## Comandos (PowerShell, desde la raiz)

Python 3.11 para desarrollo; Java 17 y PySpark para las pruebas de integracion.
No instales estas dependencias dentro de un notebook de Fabric.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m ruff format src tools tests
python -m tools.build_notebooks
python -m ruff check .
python -m tools.build_notebooks --check
python -m unittest discover -s tests -v
```

Para incluir Spark local en el mismo proceso de pruebas:

```powershell
$env:RUN_SPARK_TESTS = "1"
python -m unittest discover -s tests -v
Remove-Item Env:RUN_SPARK_TESTS
```

Los tests Spark usan una sesion local de prueba sin UI y no se conectan a Fabric.
No prueban OneLake, el catalogo Fabric, permisos, importacion en el portal ni el
motor T-SQL. La compatibilidad final debe comprobarse en un Lakehouse de prueba.

Las pruebas unitarias comprueban determinismo, limites, errores inyectados,
recuperacion de nulos, conflictos y proteccion de escrituras antes de modificar
tablas. Las de integracion comparan PySpark con una referencia Python e incluyen
redondeo y notebooks generados. CI ejecuta ambas categorias con Spark 3.5.

No se ejecutan DDL/DML contra ningun recurso remoto desde CI y no se necesitan
secretos de GitHub Actions. El flujo usa permisos de solo lectura del repositorio.

## Comprobacion manual en Fabric antes de impartir

1. Importa el notebook 01 en un workspace de pruebas y adjunta un Lakehouse vacio.
2. Ejecuta con los parametros por defecto; compara el informe con
   `docs/expected-results.json` y comprueba las tres tablas.
3. Repite con ALLOW_OVERWRITE=False: debe detenerse antes de escribir.
4. Ejecuta la solucion 02 y compara recuentos e ingresos exactos.
5. En el SQL analytics endpoint, descubre el esquema y ejecuta por separado los
   scripts de SQL en orden. Los tres resultados de validacion de claves deben
   estar vacios. Los ingresos por categoria deben coincidir con PySpark.
6. Si exportas notebooks desde Fabric, no publiques esa exportacion con salidas o
   bindings: vuelve a generar los archivos distribuibles desde las fuentes.

Este checklist es una tarea de preparacion, no una afirmacion de que ya se ha
ejecutado en el tenant de la persona que descarga el material.
