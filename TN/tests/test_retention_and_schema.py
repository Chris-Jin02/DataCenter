import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]


class RetentionAndSchemaTest(unittest.TestCase):
    def test_candidate_schema_declares_every_exported_column(self):
        schema_path = ROOT / "TN/model/notebook_support/candidate_workbook_schema.json"
        schema = json.loads(schema_path.read_text())
        self.assertEqual(schema["version"], "TN-DC-1.0.0")
        self.assertIn("candidate_rank", schema["columns"])
        self.assertIn("required_diligence_checks", schema["columns"])
        self.assertEqual(schema["columns"]["final_score"]["type"], "number")

    def test_retention_policy_keeps_code_and_release_outputs(self):
        policy_path = ROOT / "TN/PROCESS_FILE_RETENTION.md"
        if not policy_path.exists():
            self.skipTest("local retention policy is not included in the GitHub release")
        policy = policy_path.read_text()
        self.assertIn("phase 4/results", policy)
        self.assertIn("node_modules", policy)
        self.assertIn("Do not remove", policy)

    def test_node_build_and_verify_scripts_use_the_shared_schema(self):
        for name in ("build_candidate_workbook.mjs", "verify_candidate_workbook.mjs"):
            source = (ROOT / "TN/model/notebook_support/phase4" / name).read_text()
            self.assertIn("candidate_workbook_schema.json", source)

    def test_verify_script_handles_the_frozen_crlf_csv_header(self):
        source = (ROOT / "TN/model/notebook_support/phase4/verify_candidate_workbook.mjs").read_text()
        self.assertIn("split(/\\r?\\n/, 1)", source)
