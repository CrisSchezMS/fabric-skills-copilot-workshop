import ast
import json
import types
import unittest
from pathlib import Path
from unittest.mock import Mock

from src.analytics_sales import analytics_table_names
from tools.build_notebooks import build_artifacts

ROOT = Path(__file__).resolve().parents[1]


class NotebookDistributionTests(unittest.TestCase):
    def test_analytics_publication_is_disabled_and_rejects_changed_destinations(self):
        artifact = build_artifacts()["soluciones/03_publicar_analitica.ipynb"]
        publish = next(cell for cell in artifact["cells"] if cell["id"] == "publish")
        code = compile("".join(publish["source"]), "publish", "exec")
        writer = Mock()
        namespace = {
            "WRITE_ANALYTICS": False,
            "SCHEMA": "dbo",
            "targets": analytics_table_names("dbo"),
            "analytics_table_names": analytics_table_names,
            "source_lakehouse_id": "local-test",
            "notebookutils": types.SimpleNamespace(
                runtime=types.SimpleNamespace(context={"defaultLakehouseId": "local-test"})
            ),
            "write_analytics_tables": writer,
            "print": Mock(),
        }
        exec(code, namespace)
        writer.assert_not_called()
        namespace["WRITE_ANALYTICS"] = True
        namespace["SCHEMA"] = "other"
        with self.assertRaisesRegex(ValueError, "destino ha cambiado"):
            exec(code, namespace)
        namespace["SCHEMA"] = "dbo"
        namespace["notebookutils"].runtime.context["defaultLakehouseId"] = "changed"
        with self.assertRaisesRegex(ValueError, "Lakehouse ha cambiado"):
            exec(code, namespace)
        writer.assert_not_called()

    def test_distributed_notebooks_are_self_contained_clean_and_parseable(self):
        for relative, expected in build_artifacts().items():
            path = ROOT / relative
            with self.subTest(path=relative):
                actual = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(actual, expected, "Regenera los artefactos desde su fuente.")
                if path.suffix != ".ipynb":
                    continue
                self.assertEqual(actual["nbformat"], 4)
                self.assertNotIn("dependencies", actual["metadata"])
                ids = [cell["id"] for cell in actual["cells"]]
                self.assertEqual(len(set(ids)), len(ids))
                for cell in actual["cells"]:
                    self.assertTrue(all(line.endswith("\n") for line in cell["source"]))
                    if cell["cell_type"] != "code":
                        continue
                    self.assertEqual(cell["outputs"], [])
                    self.assertIsNone(cell["execution_count"])
                    code = "".join(cell["source"])
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ImportFrom):
                            self.assertNotIn(node.module, ("src", "tools"))
                            self.assertFalse((node.module or "").startswith(("src.", "tools.")))
                        if isinstance(node, ast.Import):
                            self.assertTrue(
                                all(
                                    alias.name.split(".")[0] not in ("src", "tools")
                                    for alias in node.names
                                )
                            )


if __name__ == "__main__":
    unittest.main()
