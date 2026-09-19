import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
WEIGHTS = ROOT / "TN/model/phase 3/results/phase3_final_model_weights.json"
SCORING = ROOT / "TN/model/phase 3/results/phase3_final_multilocation_scoring.xlsx"


class ReleaseFactsTest(unittest.TestCase):

  def test_release_weight_package_is_the_published_model_contract(self):
    package = json.loads(WEIGHTS.read_text())
    self.assertEqual(package["winner"], "pls_logistic")
    self.assertEqual(len(package["features"]), 21)
    self.assertEqual(len(package["candidate_primary_draw_models"]["pls_logistic"]), 20)
    self.assertTrue(package["score_reference_raw"])
    self.assertEqual(package["phase2_sha256"], "112d6db67d7f4f9e74fa8edde3406937e1f8eb7145e9bc04a64e7030cf1d3e03")


  def test_phase4_readme_records_the_workbook_consumed_by_release_code(self):
    digest = hashlib.sha256(SCORING.read_bytes()).hexdigest()
    readme = (ROOT / "TN/model/phase 4/README.md").read_text()
    self.assertIn(f"Phase 3 scoring workbook SHA-256: `{digest}`", readme)


  def test_current_facing_docs_do_not_describe_release_as_pending(self):
    paths = [
        ROOT / "TN/README.md",
        ROOT / "TN/Proposal/Tennessee_spatial_analysis.md",
        ROOT / "TN/model/phase 3/README.md",
        ROOT / "TN/model/phase 4/README.md",
    ]
    text = "\n".join(path.read_text() for path in paths)
    self.assertNotIn("Phase 3H is next", text)
    self.assertNotIn("Phase 4 | Planned", text)
    self.assertNotIn("screened_logistic` is fixed as the transparent supervised specification", text)
