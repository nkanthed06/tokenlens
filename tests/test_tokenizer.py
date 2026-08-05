import unittest

from tokenlens.tokenizer import analyze_text, estimate_tokens


class TokenizerTests(unittest.TestCase):
    def test_empty_text_has_no_tokens(self) -> None:
        self.assertEqual(estimate_tokens(""), 0)

    def test_estimate_uses_lexical_and_character_bounds(self) -> None:
        self.assertEqual(estimate_tokens("hello, world!"), 4)
        self.assertEqual(estimate_tokens("x" * 40), 10)

    def test_analysis_reports_text_dimensions(self) -> None:
        result = analyze_text("Ship the patch today.")

        self.assertEqual(result.characters, 21)
        self.assertEqual(result.words, 4)
        self.assertGreaterEqual(result.estimated_tokens, 5)

    def test_non_string_input_is_rejected(self) -> None:
        with self.assertRaisesRegex(TypeError, "text must be a string"):
            estimate_tokens(42)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
