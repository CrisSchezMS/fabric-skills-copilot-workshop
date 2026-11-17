"""Build standalone notebooks from reviewed source; no third-party dependencies."""

import argparse
import json
import textwrap
from dataclasses import asdict
from pathlib import Path

from src.synthetic_data import GeneratorConfig, expected_results, generate_data

ROOT = Path(__file__).resolve().parents[1]


def cell(kind, source, cell_id, parameters=False):
    result = {
        "cell_type": kind,
        "id": cell_id,
        "metadata": {"tags": ["parameters"]} if parameters else {},
        "source": textwrap.dedent(source).strip().splitlines(keepends=True),
    }
    result["source"] = [line.rstrip("\n") + "\n" for line in result["source"]]
    if kind == "code":
        result.update(execution_count=None, outputs=[])
    return result


def source_file(name):
    return (ROOT / "src" / name).read_text(encoding="utf-8")


def notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Synapse PySpark",
                "language": "python",
                "name": "synapse_pyspark",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def build_artifacts():
    intro = """\
        # 01 - Generar datos sinteticos de ventas

        **Todo es ficticio.** No se descargan datos, no se usan secretos y no se instalan paquetes.
        Este notebook es autonomo: no necesita clonar el repositorio ni cargar archivos Python.

        ## Antes de pulsar Ejecutar todo
        1. Importa este `.ipynb` en un workspace de Microsoft Fabric con capacidad activa.
        2. Crea un Lakehouse vacio para el taller y adjuntalo como **predeterminado**.
        3. Usa el kernel PySpark. Si cambias el Lakehouse, reinicia la sesion Spark.
        4. Revisa la siguiente celda. `SCHEMA = "dbo"` corresponde a un Lakehouse con esquemas.
           Para un Lakehouse antiguo sin esquemas, usa `SCHEMA = ""`.
        5. Ejecutar todo crea **solo** `workshop_products`, `workshop_stores` y
           `workshop_sales_raw`. Si cualquiera existe, se detiene antes de escribir.

        **Repeticion:** usa otro Lakehouse o cambia explicitamente `ALLOW_OVERWRITE = True`
        despues de revisar el destino. Esto reemplaza esas tres tablas y su esquema.
        Las tres escrituras no son una transaccion: un fallo intermedio puede dejar tablas parciales.
        No uses un Lakehouse compartido con datos de produccion.
        """
    config = """\
        N_SALES = 10_000
        SEED = 42
        START_DATE = "2026-01-01"
        DAYS = 90
        SCHEMA = "dbo"
        ALLOW_OVERWRITE = False
        """
    generate = """\
        import json

        import notebookutils

        require_default_lakehouse(notebookutils.runtime.context)
        config = GeneratorConfig(seed=SEED, n_sales=N_SALES, start_date=START_DATE, days=DAYS)
        names = table_names(SCHEMA)
        print("Tablas de destino:", names)
        data = generate_data(config)
        report = expected_results(data)
        frames = create_dataframes(spark, data)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        display(frames["sales_raw"].orderBy("sale_id").limit(10))
        """
    persist = """\
        saved_counts = write_tables(spark, frames, SCHEMA, allow_overwrite=ALLOW_OVERWRITE)
        print("Tablas Delta guardadas y recuentos comprobados:", saved_counts)
        """
    generator_cells = [
        cell("markdown", intro, "intro"),
        cell("code", config, "parameters", parameters=True),
        cell(
            "markdown",
            "## Generador reutilizable\nSolo biblioteca estandar; semilla fija y fechas fijas.",
            "generator-heading",
        ),
        cell("code", source_file("synthetic_data.py"), "generator"),
        cell("code", source_file("fabric_tables.py"), "fabric-helpers"),
        cell(
            "markdown",
            "## Generar, inspeccionar y conocer los resultados esperados",
            "generate-heading",
        ),
        cell("code", generate, "generate"),
        cell(
            "markdown",
            "## Guardar las tres tablas Delta en el Lakehouse predeterminado",
            "save-heading",
        ),
        cell("code", persist, "persist"),
        cell(
            "markdown",
            """\
            ## Listo para el taller

            Con los parametros por defecto hay 12 productos, 4 tiendas y 10.200 filas de ventas:
            10.000 ventas distintas y 200 copias exactas. Se introducen nulos, texto con espacios,
            cantidades no validas y productos inexistentes. Las cancelaciones son otro estado de
            negocio, no un error de calidad.

            Los contadores del informe incluyen duplicados cuando el nombre termina en `_rows`.
            No sumes incidencias para calcular ventas rechazadas: pueden solaparse.

            **Reto:** pide a Copilot un perfilado y una propuesta de limpieza antes de ejecutar
            cambios. Recupera categoria y ciudad desde las dimensiones; no elimines esas ventas
            solo porque los campos raw sean nulos. Redondea cada linea a dos decimales ANTES
            de sumar. La solucion de referencia esta separada para no desvelar el ejercicio.

            El SQL analytics endpoint puede tardar en mostrar las tablas. Refresca el explorador
            y confirma el esquema antes de ejecutar los ejemplos T-SQL del repositorio.
            Deten la sesion Spark desde la interfaz de Fabric al terminar.
            """,
            "next",
        ),
    ]
    solution_cells = [
        cell(
            "markdown",
            """\
            # 02 - Solucion de referencia: limpiar y analizar

            **Opcional, para despues del ejercicio.** Ejecuta primero el notebook 01 y adjunta
            aqui el mismo Lakehouse predeterminado. Este notebook lee las tres tablas creadas,
            pero no modifica ni guarda ninguna tabla. Solo muestra resultados en memoria.

            Reglas: quitar copias exactas; detenerse si un sale_id tiene versiones distintas;
            aceptar ventas completed con quantity > 0 y claves existentes en las dimensiones;
            recuperar categoria/ciudad de las dimensiones; calcular net_amount con decimal
            y redondeo por linea. Las cancelaciones no se consideran ingresos.
            """,
            "intro",
        ),
        cell("code", 'SCHEMA = "dbo"\n', "parameters", parameters=True),
        cell("code", source_file("fabric_tables.py"), "fabric-helpers"),
        cell("code", source_file("transform_sales.py"), "transform"),
        cell(
            "code",
            """\
            import notebookutils
            from pyspark.sql import functions as F

            require_default_lakehouse(notebookutils.runtime.context)
            names = table_names(SCHEMA)
            source_frames = {key: spark.table(name) for key, name in names.items()}
            sales_clean = clean_sales(
                source_frames["sales_raw"], source_frames["products"], source_frames["stores"]
            )
            summary = sales_clean.groupBy("category").agg(
                F.count("*").alias("sales_count"),
                F.sum("quantity").alias("units"),
                F.sum("net_amount").alias("net_revenue"),
            )
            display(summary.orderBy(F.desc("net_revenue"), "category"))
            display(sales_clean.agg(
                F.count("*").alias("clean_rows"),
                F.sum("net_amount").alias("net_revenue"),
            ))
            assert sales_clean.count() == sales_clean.select("sale_id").distinct().count()
            assert sales_clean.filter(
                F.col("category").isNull() | F.col("city").isNull()
            ).count() == 0
            """,
            "analyze",
        ),
        cell(
            "markdown",
            """\
            ## Comprobar y explicar

            Compara recuentos e ingresos con el informe del notebook 01. Con su configuracion
            original tambien puedes consultar `docs/expected-results.json` en GitHub.
            Si cambias la semilla o el volumen, los importes de ese archivo ya no aplican.
            El detalle de negocio se explica en `docs/datos.md`.

            Para persistir una tabla limpia, pide a Copilot un plan que indique destino, esquema,
            comprobaciones y modo de escritura. Este notebook no realiza esa escritura.
            """,
            "verify",
        ),
    ]
    config = GeneratorConfig()
    return {
        "notebooks/01_generar_datos_sinteticos.ipynb": notebook(generator_cells),
        "soluciones/02_limpiar_y_analizar.ipynb": notebook(solution_cells),
        "docs/expected-results.json": {
            "configuration": asdict(config),
            "expected": expected_results(generate_data(config)),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale.")
    args = parser.parse_args()
    stale = []
    for relative, content in build_artifacts().items():
        path = ROOT / relative
        rendered = json.dumps(content, ensure_ascii=False, indent=2) + "\n"
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != rendered:
                stale.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rendered, encoding="utf-8", newline="\n")
    if stale:
        raise SystemExit("Regenera con python -m tools.build_notebooks: " + ", ".join(stale))
    print("Artefactos actualizados." if not args.check else "Artefactos sincronizados.")


if __name__ == "__main__":
    main()
