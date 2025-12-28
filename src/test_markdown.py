import unittest
from markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "A ![one](https://ex.com/1.png) and ![two](https://ex.com/2.jpg)."
        )
        self.assertListEqual(
            [("one", "https://ex.com/1.png"), ("two", "https://ex.com/2.jpg")],
            matches,
        )

    def test_extract_markdown_images_adjacent(self):
        matches = extract_markdown_images(
            "![a](https://ex.com/a.png)![b](https://ex.com/b.png)"
        )
        self.assertListEqual(
            [("a", "https://ex.com/a.png"), ("b", "https://ex.com/b.png")],
            matches,
        )

    def test_extract_markdown_images_empty(self):
        matches = extract_markdown_images("No images here.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_allows_spaces_in_alt(self):
        matches = extract_markdown_images(
            "Text ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) end"
        )
        self.assertListEqual(
            [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
            matches,
        )

    def test_extract_markdown_images_ignores_links(self):
        matches = extract_markdown_images("A [link](https://example.com) but no image.")
        self.assertListEqual([], matches)

    # ----- links -----
    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "A [one](https://ex.com/1) and [two](https://ex.com/2)."
        )
        self.assertListEqual(
            [("one", "https://ex.com/1"), ("two", "https://ex.com/2")],
            matches,
        )

    def test_extract_markdown_links_adjacent(self):
        matches = extract_markdown_links("[a](https://ex.com/a)[b](https://ex.com/b)")
        self.assertListEqual(
            [("a", "https://ex.com/a"), ("b", "https://ex.com/b")],
            matches,
        )

    def test_extract_markdown_links_empty(self):
        matches = extract_markdown_links("No links here.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_allows_spaces_in_text(self):
        matches = extract_markdown_links("Text [obi wan](https://example.com/obi) end")
        self.assertListEqual(
            [("obi wan", "https://example.com/obi")],
            matches,
        )

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "An ![image](https://i.imgur.com/zjjcJKZ.png) but no link."
        )
        self.assertListEqual([], matches)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()
