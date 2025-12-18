import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_node_with_value_only(self):
        node = HTMLNode(tag="p", value="Hello")
        expected = "<p>Hello</p>"
        self.assertEqual(repr(node), expected)

    def test_node_with_children(self):
        child1 = HTMLNode(tag="span", value="A")
        child2 = HTMLNode(tag="span", value="B")

        parent = HTMLNode(tag="div", children=[child1, child2])

        expected = "<div>\n" "<span>A</span>\n" "<span>B</span>" "</div>"
        self.assertEqual(repr(parent), expected)

    def test_node_with_props(self):
        node = HTMLNode(
            tag="a", value="Link", props={"href": "www.example.com", "target": "_blank"}
        )

        expected = '<a href="www.example.com" target="_blank">Link</a>'
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
