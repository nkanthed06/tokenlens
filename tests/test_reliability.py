import re
import unittest

from tokenlens.contracts import parse_estimate_request
from tokenlens.estimator import estimate_output_tokens, estimate_turn
from tokenlens.limits import (
    MAX_CONTEXT_TOKENS,
    MAX_OUTPUT_TOKENS,
    MAX_PROMPT_CHARACTERS,
)
from tokenlens.service import analyze_request


class ReliabilityTests(unittest.TestCase):
    def test_prompt_character_limit_is_enforced(self) -> None:
        payload = {"prompt": "x" * (MAX_PROMPT_CHARACTERS + 1)}

        with self.assertRaisesRegex(ValueError, "prompt cannot exceed"):
            parse_estimate_request(payload)

    def test_direct_estimates_enforce_context_limit(self) -> None:
        with self.assertRaisesRegex(ValueError, "context_tokens cannot exceed"):
            estimate_turn(
                "valid",
                model="claude-sonnet",
                context_tokens=MAX_CONTEXT_TOKENS + 1,
            )

    def test_output_limit_is_enforced(self) -> None:
        with self.assertRaisesRegex(ValueError, "maximum cannot exceed"):
            estimate_output_tokens(100, maximum=MAX_OUTPUT_TOKENS + 1)

    def test_identical_requests_receive_identical_analysis_ids(self) -> None:
        payload = {
            "prompt": "Review this change.",
            "model": "claude-sonnet-4",
        }

        first = analyze_request(payload)["analysis_id"]
        second = analyze_request(payload)["analysis_id"]

        self.assertEqual(first, second)
        self.assertIsNotNone(re.fullmatch(r"tl_[0-9a-f]{24}", first))
        self.assertNotIn(payload["prompt"], first)

    def test_analysis_id_changes_when_the_prompt_changes(self) -> None:
        first = analyze_request({"prompt": "Version one"})["analysis_id"]
        second = analyze_request({"prompt": "Version two"})["analysis_id"]

        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
