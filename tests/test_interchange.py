import csv
import json
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path

from tokenlens.history import EstimateRecord
from tokenlens.interchange import export_csv, export_json, import_json


def record() -> EstimateRecord:
    return EstimateRecord(
        recorded_at="2026-09-30T12:00:00+00:00",
        model="claude-haiku",
        prompt_tokens=10,
        context_tokens=20,
        output_tokens=30,
        total_cost=0.001,
    )


class InterchangeTests(unittest.TestCase):
    def test_csv_export_has_stable_columns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.csv"
            export_csv([record()], path)
            with path.open(encoding="utf-8") as export_file:
                rows = list(csv.DictReader(export_file))

        self.assertEqual(rows[0]["model"], "claude-haiku")
        self.assertEqual(rows[0]["total_cost"], "0.001")

    def test_json_history_round_trips(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.json"
            export_json([record()], path)
            imported = import_json(path)

        self.assertEqual(imported, [record()])

    def test_json_import_rejects_unknown_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.json"
            payload = asdict(record())
            payload["raw_prompt"] = "must not be imported"
            path.write_text(json.dumps([payload]), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid fields"):
                import_json(path)


if __name__ == "__main__":
    unittest.main()
