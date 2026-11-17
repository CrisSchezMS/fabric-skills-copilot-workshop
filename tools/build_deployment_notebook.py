"""Compose the notebook Copilot deploys and runs after approval, outside the repository."""

import argparse
import json
from pathlib import Path
from uuid import UUID

from src.analytics_sales import analytics_table_names
from tools.build_notebooks import cell, notebook, source_file


def build_deployment_notebook(schema, lakehouse_id):
    analytics_table_names(schema)
    lakehouse_id = str(UUID(lakehouse_id))
    return notebook(
        [
            cell(
                "markdown",
                """\
                # Base analitica desplegada por Copilot

                Ejecutar este notebook PUBLICA las tres tablas derivadas del contrato.
                La aprobacion se obtiene antes de crearlo y arrancarlo, no mediante un flag.
                No modifica las fuentes ni sobrescribe destinos. Un fallo puede dejar
                publicacion parcial: inspecciona el estado antes de reanudar.
                """,
                "intro",
            ),
            cell(
                "code",
                f"SCHEMA = {schema!r}\nEXPECTED_LAKEHOUSE_ID = {lakehouse_id!r}\n",
                "parameters",
                parameters=True,
            ),
            cell("code", source_file("fabric_tables.py"), "fabric-helpers"),
            cell("code", source_file("profile_sales.py"), "profile-helpers"),
            cell("code", source_file("transform_sales.py"), "transform"),
            cell("code", source_file("analytics_sales.py"), "analytics-helpers"),
            cell(
                "code",
                """\
                import notebookutils

                require_default_lakehouse(notebookutils.runtime.context)
                if notebookutils.runtime.context.get("defaultLakehouseId") != EXPECTED_LAKEHOUSE_ID:
                    raise ValueError("El Lakehouse no coincide con el destino aprobado.")
                names = table_names(SCHEMA)
                targets = analytics_table_names(SCHEMA)
                print("Origenes:", names)
                print("Destinos aprobados:", targets)
                source_frames = {key: spark.table(name) for key, name in names.items()}
                expected_frames = create_dataframes(spark, {key: [] for key in names})
                profile = profile_sales(source_frames, expected_frames)
                print("Perfil observado (incidencias raw y sin copias):", profile)
                """,
                "inspect",
            ),
            cell(
                "code",
                """\
                from pyspark.sql import functions as F

                sales_clean = clean_sales(
                    source_frames["sales_raw"], source_frames["products"], source_frames["stores"]
                )
                analytics_frames = build_analytics_frames(sales_clean)
                totals = validate_analytics_frames(analytics_frames)
                print("Totales calculados:", totals)
                display(sales_clean.groupBy("category").agg(
                    F.count("*").alias("sales_count"),
                    F.sum("quantity").alias("units"),
                    F.sum("net_amount").alias("net_revenue"),
                ).orderBy("category"))
                """,
                "validate",
            ),
            cell(
                "code",
                """\
                if notebookutils.runtime.context.get("defaultLakehouseId") != EXPECTED_LAKEHOUSE_ID:
                    raise ValueError("El Lakehouse ha cambiado desde la inspeccion.")
                if analytics_table_names(SCHEMA) != targets:
                    raise ValueError("El destino ha cambiado desde la inspeccion.")
                published = write_analytics_tables(spark, analytics_frames, SCHEMA, approved=True)
                print("Tablas guardadas, releidas y reconciliadas:", published)
                """,
                "publish",
            ),
        ]
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", required=True, help='Esquema descubierto; "" sin esquemas.')
    parser.add_argument("--lakehouse-id", required=True, help="ID descubierto, no un nombre.")
    parser.add_argument("--output", required=True, type=Path, help="Ruta privada fuera del repo.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output.resolve()
    if output.is_relative_to(root):
        parser.error("El notebook contiene contexto del entorno: guardalo fuera del repositorio.")
    artifact = build_deployment_notebook(args.schema, args.lakehouse_id)
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n")
    print("Notebook local creado. Todavia no esta guardado ni ejecutado en Fabric.")


if __name__ == "__main__":
    main()
