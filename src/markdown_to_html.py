import re
from block_to_block_type import block_to_block_type
from markdown import markdown_to_blocks
from md_types import BlockType, TextType
from parentnode import ParentNode
from split_nodes import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        t = block_to_block_type(block)
        if t == BlockType.HEADING:
            children.append(_heading_to_node(block))
        elif t == BlockType.CODE:
            children.append(_code_to_node(block))
        elif t == BlockType.QUOTE:
            children.append(_quote_to_node(block))
        elif t == BlockType.UNORDERED_LIST:
            children.append(_ul_to_node(block))
        elif t == BlockType.ORDERED_LIST:
            children.append(_ol_to_node(block))
        elif t == BlockType.PARAGRAPH:
            children.append(_paragraph_to_node(block))
        else:
            raise ValueError("invalid block type")
    return ParentNode("div", children)


def _text_to_children(text):
    children = []
    for tn in text_to_textnodes(text):
        children.append(text_node_to_html_node(tn))
    return children


def _paragraph_to_node(block):
    text = " ".join([ln.strip() for ln in block.split("\n") if ln.strip() != ""])
    return ParentNode("p", _text_to_children(text))


def _heading_to_node(block):
    m = re.match(r"^(#{1,6}) (.*)$", block)
    if not m:
        raise ValueError("invalid heading")
    level = len(m.group(1))
    return ParentNode(f"h{level}", _text_to_children(m.group(2)))


def _code_to_node(block):
    if not (block.startswith("```") and block.endswith("```")):
        raise ValueError("invalid code block")

    inner = block[3:-3]
    if inner.startswith("\n"):
        inner = inner[1:]

    lines = inner.split("\n")

    while lines and lines[-1].strip() == "":
        lines.pop()

    min_indent = None
    for ln in lines:
        if ln.strip() == "":
            continue
        indent = len(ln) - len(ln.lstrip(" "))
        min_indent = indent if min_indent is None else min(min_indent, indent)

    if min_indent is None:
        dedented = "\n"
    else:
        out = []
        for ln in lines:
            if ln.strip() == "":
                out.append("")
            else:
                out.append(ln[min_indent:])
        dedented = "\n".join(out) + "\n"

    code_leaf = text_node_to_html_node(TextNode(dedented, TextType.CODE))
    return ParentNode("pre", [code_leaf])


def _quote_to_node(block):
    lines = block.split("\n")
    stripped = []
    for ln in lines:
        if not ln.startswith(">"):
            raise ValueError("invalid quote")
        ln = ln[1:]
        if ln.startswith(" "):
            ln = ln[1:]
        stripped.append(ln)
    return ParentNode("blockquote", _text_to_children("\n".join(stripped)))


def _ul_to_node(block):
    items = []
    for ln in block.split("\n"):
        if not ln.startswith("- "):
            raise ValueError("invalid unordered list")
        items.append(ParentNode("li", _text_to_children(ln[2:])))
    return ParentNode("ul", items)


def _ol_to_node(block):
    items = []
    for ln in block.split("\n"):
        m = re.match(r"^\d+\. (.*)$", ln)
        if not m:
            raise ValueError("invalid ordered list")
        items.append(ParentNode("li", _text_to_children(m.group(1))))
    return ParentNode("ol", items)


