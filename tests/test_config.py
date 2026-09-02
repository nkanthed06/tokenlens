import unittest
from pathlib import Path

from tokenlens.config import load_settings
from tokenlens.estimator import OutputMode


class ConfigTests(unittest.TestCase):
    def test_defaults_are_stable(self) -> None:
        settings = load_settings({})

        self.assertEqual(settings.default_model, "claude-sonnet")
        self.assertEqual(settings.output_mode, OutputMode.BALANCED)
        self.assertEqual(settings.warning_budget_usd, 0.05)

    def test_environment_overrides_settings(self) -> None:
        settings = load_settings(
            {
                "TOKENLENS_MODEL": "gpt-4.1-mini",
                "TOKENLENS_OUTPUT_MODE": "concise",
                "TOKENLENS_WARNING_BUDGET_USD": "0.25",
                "TOKENLENS_HISTORY_PATH": "var/tokenlens.jsonl",
            }
        )

        self.assertEqual(settings.default_model, "gpt-4.1-mini")
        self.assertEqual(settings.output_mode, OutputMode.CONCISE)
        self.assertEqual(settings.warning_budget_usd, 0.25)
        self.assertEqual(settings.history_path, Path("var/tokenlens.jsonl"))

    def test_nonfinite_and_negative_budgets_are_rejected(self) -> None:
        for value in ("nan", "inf", "-1"):
            with self.subTest(value=value), self.assertRaisesRegex(
                ValueError, "finite and non-negative"
            ):
                load_settings({"TOKENLENS_WARNING_BUDGET_USD": value})

    def test_blank_paths_and_unknown_modes_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "HISTORY_PATH"):
            load_settings({"TOKENLENS_HISTORY_PATH": " "})
        with self.assertRaisesRegex(ValueError, "OUTPUT_MODE"):
            load_settings({"TOKENLENS_OUTPUT_MODE": "verbose"})


if __name__ == "__main__":
    unittest.main()
