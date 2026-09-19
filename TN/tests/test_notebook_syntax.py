import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
PHASE_ROOT = ROOT / "TN/model"


class NotebookSyntaxTest(unittest.TestCase):
    def test_phase_notebook_code_cells_compile(self):
        notebooks = sorted(PHASE_ROOT.glob("phase */**/*.ipynb"))
        self.assertTrue(notebooks, "No phase notebooks were found")

        for notebook_path in notebooks:
            notebook = json.loads(notebook_path.read_text())
            for index, cell in enumerate(notebook["cells"]):
                if cell["cell_type"] == "code":
                    source = "".join(cell["source"])
                    compile(source, f"{notebook_path}:cell-{index}", "exec")

    def test_markdown_cells_do_not_store_code_outputs(self):
        for notebook_path in PHASE_ROOT.glob("phase */**/*.ipynb"):
            notebook = json.loads(notebook_path.read_text())
            for index, cell in enumerate(notebook["cells"]):
                if cell["cell_type"] == "markdown":
                    self.assertNotIn(
                        "outputs",
                        cell,
                        f"{notebook_path}:cell-{index} is a Markdown cell with outputs",
                    )

    def test_notebook_cells_have_stable_ids(self):
        for notebook_path in PHASE_ROOT.glob("phase */**/*.ipynb"):
            notebook = json.loads(notebook_path.read_text())
            for index, cell in enumerate(notebook["cells"]):
                self.assertTrue(
                    cell.get("id"),
                    f"{notebook_path}:cell-{index} has no stable cell id",
                )

    def test_notebooks_resolve_shared_support_from_the_local_project_layout(self):
        obsolete_support_path = "ROOT / 'TN' / 'model' / 'notebook_support'"
        for notebook_path in PHASE_ROOT.glob("phase */**/*.ipynb"):
            notebook = json.loads(notebook_path.read_text())
            source = "".join(
                "".join(cell["source"])
                for cell in notebook["cells"]
                if cell["cell_type"] == "code"
            )
            self.assertNotIn(obsolete_support_path, source, notebook_path)

    def test_phase4_uses_the_shared_node_support_directory(self):
        path = PHASE_ROOT / "phase 4/phase4_release_and_products.ipynb"
        notebook = json.loads(path.read_text())
        source = "".join(
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )
        self.assertNotIn('PHASE4 / "notebook_support"', source)
        self.assertIn('ROOT / "outputs/Data center/TN/model/notebook_support/phase4"', source)
        self.assertNotIn("/Users/steve/", source)
