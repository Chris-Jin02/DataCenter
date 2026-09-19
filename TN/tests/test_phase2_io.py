import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class Phase2IOTest(unittest.TestCase):
    def test_resolve_phase2_workbook_prefers_the_phase_directory_copy(self):
        from TN.model.notebook_support.phase2_io import resolve_phase2_workbook

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            local = root / "TN/model/phase 2/dataset/phase2_model_dataset.xlsx"
            fallback = root / "outputs/Data center/TN/model/phase 2/dataset/phase2_model_dataset.xlsx"
            local.parent.mkdir(parents=True)
            fallback.parent.mkdir(parents=True)
            local.write_bytes(b"local")
            fallback.write_bytes(b"fallback")
            self.assertEqual(resolve_phase2_workbook(root), local.resolve())

    def test_resolve_phase2_workbook_uses_output_fallback(self):
        from TN.model.notebook_support.phase2_io import resolve_phase2_workbook

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fallback = root / "outputs/Data center/TN/model/phase 2/dataset/phase2_model_dataset.xlsx"
            fallback.parent.mkdir(parents=True)
            fallback.write_bytes(b"fallback")
            self.assertEqual(resolve_phase2_workbook(root), fallback.resolve())

    def test_migrated_notebooks_use_the_maintained_support_directory(self):
        notebooks = [
            ROOT / "TN/model/phase 2/Phase2_candidate_domain_background.ipynb",
            ROOT / "TN/model/phase 2/Phase2_grid_feature_matrix.ipynb",
            ROOT / "TN/model/phase 3/code/phase3_final_model_training.ipynb",
            ROOT / "TN/model/phase 3/code/phase3_model_training_comparison_visualization.ipynb",
            ROOT / "TN/model/phase 4/phase4_release_and_products.ipynb",
        ]
        for notebook in notebooks:
            source = notebook.read_text()
            self.assertIn(
                "_support = ROOT / 'outputs' / 'Data center' / 'TN' / 'model' / 'notebook_support'",
                source,
            )
