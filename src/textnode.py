from leafnode import LeafNode
from md_types import TextType



class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, TextType.{self.text_type.value.upper()}, {self.url})"


def text_node_to_html_node(text_node):

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a",
                value=text_node.text,
                props={
                    "href": text_node.url,
                },
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value=None,
                props={"alt": text_node.text, "src": text_node.url},
            )
        case _:
            raise Exception("invalid text type")


