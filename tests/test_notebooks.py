import ast
import json
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.analytics_sales import analytics_table_names
from tools.build_deployment_notebook import build_deployment_notebook, main
from tools.build_notebooks import build_artifacts

ROOT = Path(__file__).resolve().parents[1]
LAKEHOUSE_ID = "00000000-0000-0000-0000-000000000001"


class NotebookDistributionTests(unittest.TestCase):
    def test_approved_deployment_publishes_and_rejects_changed_destinations(self):
        artifact = build_deployment_notebook("dbo", LAKEHOUSE_ID)
        publish = next(cell for cell in artifact["cells"] if cell["id"] == "publish")
        code = compile("".join(publish["source"]), "publish", "exec")
        writer = Mock()
        namespace = {
            "SCHEMA": "dbo",
            "EXPECTED_LAKEHOUSE_ID": LAKEHOUSE_ID,
            "targets": analytics_table_names("dbo"),
            "analytics_table_names": analytics_table_names,
            "spark": Mock(),
            "analytics_frames": {},
            "notebookutils": types.SimpleNamespace(
                runtime=types.SimpleNamespace(context={"defaultLakehouseId": LAKEHOUSE_ID})
            ),
            "write_analytics_tables": writer,
            "print": Mock(),
        }
        exec(code, namespace)
        writer.assert_called_once_with(
            namespace["spark"], namespace["analytics_frames"], "dbo", approved=True
        )
        writer.reset_mock()
        namespace["SCHEMA"] = "other"
        with self.assertRaisesRegex(ValueError, "destino ha cambiado"):
            exec(code, namespace)
        namespace["SCHEMA"] = "dbo"
        namespace["notebookutils"].runtime.context["defaultLakehouseId"] = "changed"
        with self.assertRaisesRegex(ValueError, "Lakehouse ha cambiado"):
            exec(code, namespace)
        writer.assert_not_called()

    def test_deployment_cli_rejects_repository_paths_and_existing_private_files(self):
        with (
            patch(
                "sys.argv",
                [
                    "builder",
                    "--schema",
                    "dbo",
                    "--lakehouse-id",
                    LAKEHOUSE_ID,
                    "--output",
                    str(ROOT / "private.ipynb"),
                ],
            ),
            patch("sys.stderr"),
        ):
            with self.assertRaises(SystemExit):
                main()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "deployment.ipynb"
            args = [
                "builder",
                "--schema",
                "dbo",
                "--lakehouse-id",
                LAKEHOUSE_ID,
                "--output",
                str(target),
            ]
            with patch("sys.argv", args), patch("sys.stdout"):
                main()
                original = target.read_bytes()
                self.assertEqual(
                    json.loads(original), build_deployment_notebook("dbo", LAKEHOUSE_ID)
                )
                with self.assertRaises(FileExistsError):
                    main()
                self.assertEqual(target.read_bytes(), original)

    def test_distributed_notebooks_are_self_contained_clean_and_parseable(self):
        artifacts = build_artifacts()
        runtime = build_deployment_notebook("dbo", LAKEHOUSE_ID)
        for relative, expected in {**artifacts, "runtime.ipynb": runtime}.items():
            path = ROOT / relative
            with self.subTest(path=relative):
                actual = (
                    runtime
                    if relative == "runtime.ipynb"
                    else json.loads(path.read_text(encoding="utf-8"))
                )
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
