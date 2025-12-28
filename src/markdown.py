import re
from block_to_block_type import block_to_block_type
from md_types import BlockType, TextType
from parentnode import ParentNode
from textnode import text_node_to_html_node, TextNode


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]+)\]\(([^\)]+)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    out = []
    for b in blocks:
        b = b.strip()
        if b:
            out.append(b)
    return out
