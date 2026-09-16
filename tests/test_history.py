import json
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from tokenlens.estimator import estimate_turn
from tokenlens.history import (
    append_record,
    read_records,
    record_from_estimate,
    summarize_history,
)


class HistoryTests(unittest.TestCase):
    def test_history_stores_metrics_without_prompt_text(self) -> None:
        estimate = estimate_turn("private prompt", model="claude-haiku")
        record = record_from_estimate(
            estimate, recorded_at=datetime(2026, 9, 16, tzinfo=UTC)
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.jsonl"
            append_record(path, record)
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(payload["model"], "claude-haiku")
        self.assertNotIn("prompt", payload)

    def test_records_round_trip_and_summarize(self) -> None:
        estimate = estimate_turn("short prompt", model="gpt-4.1-mini")
        record = record_from_estimate(estimate)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.jsonl"
            append_record(path, record)
            append_record(path, record)
            records = read_records(path)

        summary = summarize_history(records)
        self.assertEqual(summary.estimates, 2)
        self.assertAlmostEqual(summary.total_cost, record.total_cost * 2)
        self.assertAlmostEqual(summary.average_cost, record.total_cost)

    def test_missing_history_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            records = read_records(Path(directory) / "missing.jsonl")

        self.assertEqual(records, [])

    def test_malformed_history_identifies_the_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.jsonl"
            path.write_text("{}\nnot-json\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "line 1"):
                read_records(path)


if __name__ == "__main__":
    unittest.main()
