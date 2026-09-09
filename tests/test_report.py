import unittest

from tokenlens.estimator import estimate_turn
from tokenlens.report import RecommendationLevel, recommend, render_summary


class ReportTests(unittest.TestCase):
    def test_summary_shows_context_and_cost_components(self) -> None:
        estimate = estimate_turn(
            "Review this diff.",
            model="claude-haiku",
            context_tokens=1_000,
            cached_context_tokens=800,
        )

        summary = render_summary(estimate)

        self.assertIn("Cached context", summary)
        self.assertIn("800 tokens", summary)
        self.assertIn("Estimated cost", summary)

    def test_budget_overage_is_high_priority(self) -> None:
        estimate = estimate_turn("Explain this.", model="claude-opus")

        recommendation = recommend(estimate, warning_budget_usd=0)

        self.assertEqual(recommendation.level, RecommendationLevel.HIGH)

    def test_context_heavy_turn_requests_review(self) -> None:
        estimate = estimate_turn(
            "Continue.", model="claude-haiku", context_tokens=10_000
        )

        recommendation = recommend(estimate, warning_budget_usd=10)

        self.assertEqual(recommendation.level, RecommendationLevel.REVIEW)
        self.assertIn("context", recommendation.message.lower())

    def test_small_turn_is_within_thresholds(self) -> None:
        estimate = estimate_turn("List three files.", model="gpt-4.1-mini")

        recommendation = recommend(estimate, warning_budget_usd=1)

        self.assertEqual(recommendation.level, RecommendationLevel.OK)


if __name__ == "__main__":
    unittest.main()
