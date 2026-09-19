import unittest


class Phase3HelpersTest(unittest.TestCase):
    def test_empirical_percentile_uses_average_ties(self):
        from TN.model.notebook_support.phase3_data import empirical_percentile

        self.assertEqual(empirical_percentile([1, 2, 2, 3]), [25.0, 62.5, 62.5, 100.0])

    def test_empty_empirical_percentile_is_empty(self):
        from TN.model.notebook_support.phase3_data import empirical_percentile

        self.assertEqual(empirical_percentile([]), [])

    def test_empirical_percentile_preserves_missing_values(self):
        from TN.model.notebook_support.phase3_data import empirical_percentile

        result = empirical_percentile([1.0, float("nan"), 3.0])
        self.assertAlmostEqual(result[0], 50.0)
        self.assertTrue(result[1] != result[1])
        self.assertAlmostEqual(result[2], 100.0)

    def test_comparison_notebook_uses_shared_metric_implementations(self):
        notebook = (
            __import__("pathlib").Path(__file__).parents[1]
            / "model/phase 3/code/phase3_model_training_comparison_visualization.ipynb"
        ).read_text()
        self.assertNotIn('"def sigmoid(z):\\n"', notebook)
        self.assertNotIn('"def weighted_auc(y, score, weight):\\n"', notebook)
        self.assertIn("from tn_common import apply_plot_theme, finish_figure, sigmoid, weighted_auc", notebook)

    def test_final_training_notebook_uses_shared_percentile_and_table_helpers(self):
        notebook = (
            __import__("pathlib").Path(__file__).parents[1]
            / "model/phase 3/code/phase3_final_model_training.ipynb"
        ).read_text()
        self.assertNotIn('"def empirical_rank(values):\\n"', notebook)
        self.assertIn("from phase3_data import empirical_percentile, make_training_table as _make_training_table", notebook)
