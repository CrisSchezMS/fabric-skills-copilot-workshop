import contextlib
import io
import os
import sys
import types
import unittest
from decimal import Decimal
from unittest.mock import patch

from src.fabric_tables import create_dataframes
from src.synthetic_data import GeneratorConfig, expected_results, generate_data
from src.transform_sales import clean_sales
from tools.build_notebooks import build_artifacts


@unittest.skipUnless(os.environ.get("RUN_SPARK_TESTS") == "1", "Spark local es opt-in.")
class SparkIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pyspark.sql import SparkSession

        os.environ["PYSPARK_PYTHON"] = sys.executable
        os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
        cls.spark = (
            SparkSession.builder.master("local[2]")
            .appName("fabric-skills-workshop-tests")
            .config("spark.ui.enabled", "false")
            .config("spark.sql.shuffle.partitions", "2")
            .config("spark.driver.bindAddress", "127.0.0.1")
            .getOrCreate()
        )
        cls.spark.sparkContext.setLogLevel("ERROR")
        cls.data = generate_data(GeneratorConfig(n_sales=1000))
        cls.frames = create_dataframes(cls.spark, cls.data)

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_spark_solution_matches_python_counts_revenue_and_categories(self):
        from pyspark.sql import functions as F

        clean = clean_sales(
            self.frames["sales_raw"], self.frames["products"], self.frames["stores"]
        ).cache()
        try:
            expected = expected_results(self.data)
            totals = clean.agg(F.count("*").alias("rows"), F.sum("net_amount").alias("net")).first()
            self.assertEqual(totals.rows, expected["clean_rows"])
            self.assertEqual(str(totals.net), expected["net_revenue"])
            actual = {
                row.category: str(row.revenue)
                for row in clean.groupBy("category")
                .agg(F.sum("net_amount").alias("revenue"))
                .collect()
            }
            self.assertEqual(actual, expected["revenue_by_category"])
            self.assertEqual(clean.select("sale_id").distinct().count(), expected["clean_rows"])
            self.assertEqual(
                clean.filter(F.col("category").isNull() | F.col("city").isNull()).count(), 0
            )
        finally:
            clean.unpersist()

    def test_spark_preserves_recoverable_nulls_and_rounds_half_up(self):
        row = {
            **self.data["sales_raw"][0],
            "product_id": self.data["products"][0]["product_id"],
            "store_id": self.data["stores"][0]["store_id"],
            "quantity": 1,
            "unit_price": Decimal("0.05"),
            "discount_rate": Decimal("0.10"),
            "status": "completed",
            "category_raw": None,
            "city_raw": None,
        }
        frames = create_dataframes(self.spark, {**self.data, "sales_raw": [row, dict(row)]})
        actual = clean_sales(frames["sales_raw"], frames["products"], frames["stores"]).collect()
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].net_amount, Decimal("0.05"))
        self.assertEqual(actual[0].category, self.data["products"][0]["category"])
        self.assertEqual(actual[0].city, self.data["stores"][0]["city"])

    def test_spark_rejects_conflicting_sales_and_duplicate_dimension_keys(self):
        row = self.data["sales_raw"][0]
        frames = create_dataframes(
            self.spark, {**self.data, "sales_raw": [row, {**row, "quantity": 999}]}
        )
        with self.assertRaisesRegex(ValueError, "contenido diferente"):
            clean_sales(frames["sales_raw"], frames["products"], frames["stores"])
        duplicated_products = self.frames["products"].union(self.frames["products"].limit(1))
        with self.assertRaisesRegex(ValueError, "claves duplicadas"):
            clean_sales(self.frames["sales_raw"], duplicated_products, self.frames["stores"])

    def test_standalone_notebooks_execute_without_repository_imports_or_fabric_access(self):
        notebooks = build_artifacts()
        fake_utils = types.ModuleType("notebookutils")
        fake_utils.runtime = types.SimpleNamespace(context={"defaultLakehouseId": "local-test"})
        namespace = {"__name__": "__main__", "spark": self.spark, "display": lambda frame: None}
        with patch.dict(sys.modules, {"notebookutils": fake_utils}):
            with contextlib.redirect_stdout(io.StringIO()):
                for cell in notebooks["notebooks/01_generar_datos_sinteticos.ipynb"]["cells"]:
                    if cell["cell_type"] == "code" and cell["id"] != "persist":
                        exec(compile("".join(cell["source"]), cell["id"], "exec"), namespace)
            self.assertEqual(namespace["frames"]["sales_raw"].count(), 10_200)
            lookup = {namespace["names"][key]: frame for key, frame in namespace["frames"].items()}
            # Only the catalog read is substituted; all solution transformations use real Spark.
            solution = {
                "__name__": "__main__",
                "spark": types.SimpleNamespace(table=lookup.__getitem__),
                "display": lambda frame: frame.count(),
            }
            for cell in notebooks["soluciones/02_limpiar_y_analizar.ipynb"]["cells"]:
                if cell["cell_type"] == "code":
                    exec(compile("".join(cell["source"]), cell["id"], "exec"), solution)
            self.assertEqual(solution["sales_clean"].count(), namespace["report"]["clean_rows"])


if __name__ == "__main__":
    unittest.main()
