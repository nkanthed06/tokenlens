import unittest

from tokenlens.models import available_models, get_model_rates
from tokenlens.pricing import estimate_cost


class PricingTests(unittest.TestCase):
    def test_catalog_is_sorted_and_resolvable(self) -> None:
        models = available_models()

        self.assertEqual(models, tuple(sorted(models)))
        self.assertGreater(get_model_rates("claude-sonnet").output_per_million, 0)

    def test_cost_includes_cached_and_uncached_input(self) -> None:
        result = estimate_cost(
            "claude-sonnet",
            input_tokens=1_000,
            cached_input_tokens=2_000,
            output_tokens=500,
        )

        self.assertAlmostEqual(result.input_cost, 0.0036)
        self.assertAlmostEqual(result.output_cost, 0.0075)
        self.assertAlmostEqual(result.total_cost, 0.0111)

    def test_unknown_model_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported model"):
            estimate_cost("unknown", input_tokens=1, output_tokens=1)

    def test_token_counts_must_be_non_negative_integers(self) -> None:
        for value in (-1, 1.5, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                estimate_cost(
                    "claude-sonnet",
                    input_tokens=value,  # type: ignore[arg-type]
                    output_tokens=1,
                )


if __name__ == "__main__":
    unittest.main()
