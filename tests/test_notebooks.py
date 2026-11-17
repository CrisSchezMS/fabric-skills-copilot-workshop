import ast
import json
import unittest
from pathlib import Path

from tools.build_notebooks import build_artifacts

ROOT = Path(__file__).resolve().parents[1]


class NotebookDistributionTests(unittest.TestCase):
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
