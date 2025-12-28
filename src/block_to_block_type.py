import re
from md_types import BlockType


def block_to_block_type(block):

    if is_heading(block):
        return BlockType.HEADING
    if is_code_block(block):
        return BlockType.CODE
    if is_block_quote(block):
        return BlockType.QUOTE
    if is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def is_heading(block):
    return bool(re.match("^#{1,6}(?!#) ", block))


def is_code_block(block):
    return block.startswith("```") and block.endswith("```")


def is_block_quote(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            return False
    return True


def is_unordered_list(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("- "):
            return False
    return True


def is_ordered_list(block):
    lines = block.split("\n")
    expected = 1
    for line in lines:
        prefix = str(expected) + ". "
        if not line.startswith(prefix):
            return False
        expected += 1
    return True
