import io
import json
import unittest

from tokenlens.cli import main


class CliTests(unittest.TestCase):
    def test_estimate_command_renders_human_summary(self) -> None:
        output = io.StringIO()

        exit_code = main(
            ["estimate", "Summarize this change.", "--model", "claude-haiku"],
            stdout=output,
        )

        self.assertEqual(exit_code, 0)
        self.assertIn("Model: claude-haiku", output.getvalue())
        self.assertIn("Estimated cost: $", output.getvalue())

    def test_estimate_command_renders_stable_json(self) -> None:
        output = io.StringIO()

        main(
            [
                "estimate",
                "Explain the patch.",
                "--context-tokens",
                "100",
                "--cached-context-tokens",
                "80",
                "--json",
            ],
            stdout=output,
        )
        payload = json.loads(output.getvalue())

        self.assertEqual(payload["context_tokens"], 100)
        self.assertEqual(payload["cached_context_tokens"], 80)
        self.assertIn("total_cost", payload["cost"])


if __name__ == "__main__":
    unittest.main()
