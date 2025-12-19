
from textnode import TextNode
from md_types import TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        # TEXT TYPE
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("invalid delimitter count. You need matching delimiter")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        while True:
            matches_links = extract_markdown_images(text)
            if not matches_links:
                break
            alt, url = matches_links[0]
            before, after = text.split(f"![{alt}]({url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, node.text_type, node.url))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            text = after
        if text != "":
            new_nodes.append(TextNode(text, node.text_type, node.url))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        while True:
            matches_links = extract_markdown_links(text)
            if not matches_links:
                break
            alt, url = matches_links[0]
            before, after = text.split(f"[{alt}]({url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, node.text_type, node.url))
            new_nodes.append(TextNode(alt, TextType.LINK, url))

            text = after
        if text != "":
            new_nodes.append(TextNode(text, node.text_type, node.url))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_images(nodes)
    return nodes
