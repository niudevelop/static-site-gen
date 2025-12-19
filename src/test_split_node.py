import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_images, split_nodes_link


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_non_text_nodes_are_unchanged(self):
        old = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        new = split_nodes_delimiter(old, "`", TextType.CODE)
        self.assertEqual(new, old)

    def test_text_without_delimiter_is_unchanged(self):
        old = [TextNode("plain text", TextType.TEXT)]
        new = split_nodes_delimiter(old, "`", TextType.CODE)
        self.assertEqual(new, old)

    def test_single_code_span_middle(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new, expected)

    def test_code_span_at_start(self):
        node = TextNode("`code` then text", TextType.TEXT)
        new = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" then text", TextType.TEXT),
        ]
        self.assertEqual(new, expected)

    def test_code_span_at_end(self):
        node = TextNode("text then `code`", TextType.TEXT)
        new = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("text then ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new, expected)

    def test_two_code_spans(self):
        node = TextNode("a `b` c `d` e", TextType.TEXT)
        new = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.TEXT),
        ]
        self.assertEqual(new, expected)

    def test_mixed_nodes_text_and_non_text(self):
        old = [
            TextNode("a `b` c", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode("d `e` f", TextType.TEXT),
        ]
        new = split_nodes_delimiter(old, "`", TextType.CODE)

        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" c", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode("d ", TextType.TEXT),
            TextNode("e", TextType.CODE),
            TextNode(" f", TextType.TEXT),
        ]
        self.assertEqual(new, expected)

    def test_unmatched_delimiter_raises(self):
        node = TextNode("hello `world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_unmatched_delimiter_raises_three_ticks(self):
        node = TextNode("a `b` c `d", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_other_target_type_italic(self):
        node = TextNode("a *b* c", TextType.TEXT)
        new = split_nodes_delimiter([node], "*", TextType.ITALIC)

        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.ITALIC),
            TextNode(" c", TextType.TEXT),
        ]
        self.assertEqual(new, expected)
        
    def test_split_nodes_link_no_links(self):
        nodes = [TextNode("no links here", TextType.TEXT)]
        out = split_nodes_link(nodes)
        self.assertEqual([TextNode("no links here", TextType.TEXT)], out)

    def test_split_nodes_link_single_link_with_text_around(self):
        nodes = [TextNode("hi [a](u) bye", TextType.TEXT)]
        out = split_nodes_link(nodes)
        self.assertEqual(
            [
                TextNode("hi ", TextType.TEXT),
                TextNode("a", TextType.LINK, "u"),
                TextNode(" bye", TextType.TEXT),
            ],
            out,
        )

    def test_split_nodes_link_link_at_start(self):
        nodes = [TextNode("[a](u) tail", TextType.TEXT)]
        out = split_nodes_link(nodes)
        self.assertEqual(
            [
                TextNode("a", TextType.LINK, "u"),
                TextNode(" tail", TextType.TEXT),
            ],
            out,
        )

    def test_split_nodes_link_link_at_end(self):
        nodes = [TextNode("head [a](u)", TextType.TEXT)]
        out = split_nodes_link(nodes)
        self.assertEqual(
            [
                TextNode("head ", TextType.TEXT),
                TextNode("a", TextType.LINK, "u"),
            ],
            out,
        )

    def test_split_nodes_link_multiple_links(self):
        nodes = [TextNode("x [a](u) y [b](v) z", TextType.TEXT)]
        out = split_nodes_link(nodes)
        self.assertEqual(
            [
                TextNode("x ", TextType.TEXT),
                TextNode("a", TextType.LINK, "u"),
                TextNode(" y ", TextType.TEXT),
                TextNode("b", TextType.LINK, "v"),
                TextNode(" z", TextType.TEXT),
            ],
            out,
        )

    # ---------- images ----------
    def test_split_nodes_images_no_images(self):
        nodes = [TextNode("no images here", TextType.TEXT)]
        out = split_nodes_images(nodes)
        self.assertEqual([TextNode("no images here", TextType.TEXT)], out)

    def test_split_nodes_images_single_image_with_text_around(self):
        nodes = [TextNode("hi ![img](u) bye", TextType.TEXT)]
        out = split_nodes_images(nodes)
        self.assertEqual(
            [
                TextNode("hi ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "u"),
                TextNode(" bye", TextType.TEXT),
            ],
            out,
        )

    def test_split_nodes_images_image_at_start(self):
        nodes = [TextNode("![img](u) tail", TextType.TEXT)]
        out = split_nodes_images(nodes)
        self.assertEqual(
            [
                TextNode("img", TextType.IMAGE, "u"),
                TextNode(" tail", TextType.TEXT),
            ],
            out,
        )

    def test_split_nodes_images_image_at_end(self):
        nodes = [TextNode("head ![img](u)", TextType.TEXT)]
        out = split_nodes_images(nodes)
        self.assertEqual(
            [
                TextNode("head ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "u"),
            ],
            out,
        )

    def test_split_nodes_images_multiple_images(self):
        nodes = [TextNode("x ![a](u) y ![b](v) z", TextType.TEXT)]
        out = split_nodes_images(nodes)
        self.assertEqual(
            [
                TextNode("x ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "u"),
                TextNode(" y ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "v"),
                TextNode(" z", TextType.TEXT),
            ],
            out,
        )
if __name__ == "__main__":
    unittest.main()
