import unittest

from textnode import TextNode, text_node_to_html_node
from md_types import TextType
from split_nodes import text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_plain_text(self):
        out = text_to_textnodes("hello world")
        self.assertEqual([TextNode("hello world", TextType.TEXT)], out)

    def test_bold_only(self):
        out = text_to_textnodes("a **b** c")
        self.assertEqual(
            [TextNode("a ", TextType.TEXT), TextNode("b", TextType.BOLD), TextNode(" c", TextType.TEXT)],
            out,
        )

    def test_italic_only(self):
        out = text_to_textnodes("a __b__ c")
        self.assertEqual(
            [TextNode("a ", TextType.TEXT), TextNode("b", TextType.ITALIC), TextNode(" c", TextType.TEXT)],
            out,
        )

    def test_code_only(self):
        out = text_to_textnodes("a `b` c")
        self.assertEqual(
            [TextNode("a ", TextType.TEXT), TextNode("b", TextType.CODE), TextNode(" c", TextType.TEXT)],
            out,
        )

    def test_link_only(self):
        out = text_to_textnodes("[a](u)")
        self.assertEqual([TextNode("a", TextType.LINK, "u")], out)

    def test_image_only(self):
        out = text_to_textnodes("![alt](u)")
        self.assertEqual([TextNode("alt", TextType.IMAGE, "u")], out)

    def test_mixed_all_types(self):
        s = "x **b** y __i__ z `c` w [l](u) q ![img](v) r"
        out = text_to_textnodes(s)
        self.assertEqual(
            [
                TextNode("x ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" y ", TextType.TEXT),
                TextNode("i", TextType.ITALIC),
                TextNode(" z ", TextType.TEXT),
                TextNode("c", TextType.CODE),
                TextNode(" w ", TextType.TEXT),
                TextNode("l", TextType.LINK, "u"),
                TextNode(" q ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "v"),
                TextNode(" r", TextType.TEXT),
            ],
            out,
        )
    def test_multiple_links_and_images(self):
        s = "start [a](https://a.com) mid ![img1](https://i.com/1.png) more [b](https://b.com) end ![img2](https://i.com/2.png)"
        out = text_to_textnodes(s)
        self.assertEqual(
            [
                TextNode("start ", TextType.TEXT),
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://i.com/1.png"),
                TextNode(" more ", TextType.TEXT),
                TextNode("b", TextType.LINK, "https://b.com"),
                TextNode(" end ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://i.com/2.png"),
            ],
            out,
        )
    # adjusted: invalid delimiter should raise (your split_nodes_delimiter does)
    def test_invalid_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("bad **bold")

    def test_invalid_italic_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("bad __italic")

    def test_invalid_code_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("bad `code")


if __name__ == "__main__":
    unittest.main()
