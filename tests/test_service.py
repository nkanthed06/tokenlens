import tempfile
import unittest
from pathlib import Path

from tokenlens.config import Settings
from tokenlens.contracts import parse_estimate_request
from tokenlens.estimator import OutputMode
from tokenlens.history import read_records
from tokenlens.service import analyze_request


class ServiceTests(unittest.TestCase):
    def test_service_returns_estimate_and_recommendation(self) -> None:
        result = analyze_request(
            {"prompt": "Review this patch.", "model": "claude-haiku"},
            settings=Settings(warning_budget_usd=1),
        )

        self.assertEqual(result["estimate"]["model"], "claude-haiku")
        self.assertEqual(result["recommendation"]["level"], "ok")

    def test_service_uses_configured_defaults_and_saves_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            history_path = Path(directory) / "history.jsonl"
            settings = Settings(
                default_model="gpt-4.1-mini",
                output_mode=OutputMode.CONCISE,
                warning_budget_usd=1,
                history_path=history_path,
            )

            analyze_request(
                {"prompt": "Summarize this."},
                settings=settings,
                save_history=True,
            )

            records = read_records(history_path)
        self.assertEqual(records[0].model, "gpt-4.1-mini")

    def test_request_rejects_invalid_integer_types(self) -> None:
        for field in ("context_tokens", "cached_context_tokens"):
            for value in (True, 1.5, "1", -1):
                with self.subTest(field=field, value=value), self.assertRaises(
                    ValueError
                ):
                    parse_estimate_request({"prompt": "valid", field: value})

    def test_invalid_request_does_not_create_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            history_path = Path(directory) / "history.jsonl"
            settings = Settings(history_path=history_path)

            with self.assertRaisesRegex(ValueError, "prompt"):
                analyze_request({}, settings=settings, save_history=True)

            self.assertFalse(history_path.exists())


if __name__ == "__main__":
    unittest.main()
