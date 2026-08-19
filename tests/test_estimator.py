import unittest

from tokenlens.estimator import OutputMode, estimate_output_tokens, estimate_turn


class EstimatorTests(unittest.TestCase):
    def test_output_modes_scale_in_order(self) -> None:
        estimates = [
            estimate_output_tokens(1_000, mode=mode)
            for mode in (
                OutputMode.CONCISE,
                OutputMode.BALANCED,
                OutputMode.DETAILED,
            )
        ]

        self.assertEqual(estimates, sorted(estimates))

    def test_maximum_caps_output_estimate(self) -> None:
        self.assertEqual(
            estimate_output_tokens(1_000, mode="detailed", maximum=400),
            400,
        )

    def test_turn_estimate_separates_cached_context(self) -> None:
        result = estimate_turn(
            "Summarize these logs.",
            model="claude-sonnet",
            context_tokens=10_000,
            cached_context_tokens=8_000,
        )

        self.assertEqual(result.context_tokens, 10_000)
        self.assertEqual(result.cached_context_tokens, 8_000)
        self.assertEqual(result.cost.cached_input_tokens, 8_000)
        self.assertGreater(result.cost.total_cost, 0)

    def test_cached_context_cannot_exceed_total_context(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot exceed"):
            estimate_turn(
                "prompt",
                model="claude-sonnet",
                context_tokens=10,
                cached_context_tokens=11,
            )


if __name__ == "__main__":
    unittest.main()
