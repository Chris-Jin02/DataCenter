import unittest
from pathlib import Path


class Phase4ReleaseTest(unittest.TestCase):
    def test_phase4_notebook_uses_one_namespace_registration_helper(self):
        notebook = (
            Path(__file__).parents[1]
            / "model/phase 4/phase4_release_and_products.ipynb"
        ).read_text()
        self.assertIn("from phase4_runtime import register_namespace", notebook)
        self.assertNotIn("types.ModuleType", notebook)

    def test_namespace_registration_helper_has_a_stable_interface(self):
        from TN.model.notebook_support.phase4_runtime import register_namespace

        self.assertTrue(callable(register_namespace))
