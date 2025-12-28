import unittest

from block_to_block_type import block_to_block_type
from md_types import BlockType


class TestBlockToBlockType(unittest.TestCase):
    # ----- headings -----
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Title"), BlockType.HEADING)

    def test_heading_requires_space_after_hashes(self):
        self.assertEqual(block_to_block_type("##Title"), BlockType.PARAGRAPH)

    def test_heading_more_than_6_hashes_not_heading(self):
        self.assertEqual(block_to_block_type("####### Title"), BlockType.PARAGRAPH)

    def test_heading_multiline_still_heading_if_first_line_heading(self):
        # by your rules, it's a "single block"; heading rule checks start
        self.assertEqual(block_to_block_type("# Title\nmore"), BlockType.HEADING)

    # ----- code blocks -----
    def test_code_block_simple(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)

    def test_code_block_single_line(self):
        self.assertEqual(block_to_block_type("```print('x')```"), BlockType.CODE)

    def test_code_block_empty(self):
        self.assertEqual(block_to_block_type("``````"), BlockType.CODE)

    def test_code_block_missing_end(self):
        self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH)

    def test_code_block_missing_start(self):
        self.assertEqual(block_to_block_type("code\n```"), BlockType.PARAGRAPH)

    # ----- quote blocks -----
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> quote"), BlockType.QUOTE)

    def test_quote_multi_line(self):
        self.assertEqual(
            block_to_block_type("> one\n> two\n> three"),
            BlockType.QUOTE,
        )

    def test_quote_fails_if_any_line_missing_gt(self):
        self.assertEqual(
            block_to_block_type("> one\nnot quoted\n> three"),
            BlockType.PARAGRAPH,
        )

    def test_quote_allows_empty_quoted_line(self):
        self.assertEqual(block_to_block_type(">\n> next"), BlockType.QUOTE)

    # ----- unordered lists -----
    def test_unordered_list_single_line(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multi_line(self):
        self.assertEqual(
            block_to_block_type("- a\n- b\n- c"),
            BlockType.UNORDERED_LIST,
        )

    def test_unordered_list_requires_dash_space(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    def test_unordered_list_fails_if_any_line_not_list_item(self):
        self.assertEqual(
            block_to_block_type("- a\nb\n- c"),
            BlockType.PARAGRAPH,
        )

    # ----- ordered lists -----
    def test_ordered_list_single_line(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multi_line_correct_sequence(self):
        self.assertEqual(
            block_to_block_type("1. a\n2. b\n3. c"),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_must_start_at_1(self):
        self.assertEqual(block_to_block_type("2. a\n3. b"), BlockType.PARAGRAPH)

    def test_ordered_list_must_increment_by_1(self):
        self.assertEqual(
            block_to_block_type("1. a\n3. b"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_requires_dot_space(self):
        self.assertEqual(block_to_block_type("1.a"), BlockType.PARAGRAPH)

    def test_ordered_list_fails_if_any_line_not_ordered(self):
        self.assertEqual(
            block_to_block_type("1. a\n- b\n3. c"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_allows_two_digit_numbers_if_sequence_matches(self):
        self.assertEqual(
            block_to_block_type("1. a\n2. b\n3. c\n4. d\n5. e\n6. f\n7. g\n8. h\n9. i\n10. j"),
            BlockType.ORDERED_LIST,
        )

    # ----- paragraph fallback -----
    def test_paragraph_plain_text(self):
        self.assertEqual(block_to_block_type("just text"), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(
            block_to_block_type("line one\nline two"),
            BlockType.PARAGRAPH,
        )

    def test_paragraph_starts_with_gt_but_not_all_lines(self):
        self.assertEqual(
            block_to_block_type("> q\nnot q"),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
