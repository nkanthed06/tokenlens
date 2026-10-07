import unittest

from tokenlens.estimator import estimate_turn
from tokenlens.models import UnsupportedModelError, resolve_model


class ModelResolutionTests(unittest.TestCase):
    def test_aliases_resolve_to_canonical_model_names(self) -> None:
        self.assertEqual(resolve_model("claude-sonnet-4"), "claude-sonnet")
        self.assertEqual(
            resolve_model("gpt-4.1-mini-2025-04-14"),
            "gpt-4.1-mini",
        )

    def test_resolution_normalizes_case_and_whitespace(self) -> None:
        self.assertEqual(resolve_model("  Claude-Sonnet  "), "claude-sonnet")

    def test_turn_estimates_report_the_canonical_model(self) -> None:
        result = estimate_turn("Summarize this", model="claude-sonnet-4")

        self.assertEqual(result.model, "claude-sonnet")
        self.assertEqual(result.cost.model, "claude-sonnet")

    def test_unknown_models_are_never_silently_priced(self) -> None:
        with self.assertRaisesRegex(
            UnsupportedModelError,
            "Supported models: claude-haiku",
        ):
            resolve_model("future-model")


if __name__ == "__main__":
    unittest.main()
