import re
from enum import Enum
from typing import List
from htmlnode import ParentNode, HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
from inlinetext import text_to_textnodes
import logging, os
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "INFO").upper())

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    ULIST = 'unordered_list'
    OLIST = 'ordered_list'


def text_to_children(text: str):
    block_type = block_to_block_type(text)
    match BlockType(block_type):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(text)
        case BlockType.ULIST:
            return lists_to_html_node(text, BlockType.ULIST)
        case BlockType.OLIST:
            return lists_to_html_node(text, BlockType.OLIST)
        case BlockType.QUOTE:
            return quote_block_to_html(text)
        case BlockType.HEADING:
            return heading_to_html_node(text)
        case BlockType.CODE:
            return code_to_html_node(text)
        case _:
            raise ValueError(f"{block_type} is not a supported Markdown block")


def text_to_html_node(text: str) -> List[HTMLNode]:
    item_node = []
    text = " ".join(text.splitlines())
    item_node.extend(text_to_textnodes(text))
    html_node = list(map(text_node_to_html_node, item_node))
    return html_node # type: ignore

def paragraph_to_html_node(text: str) -> ParentNode:
    return ParentNode("p", text_to_html_node(text))

def code_to_html_node(text: str) -> ParentNode:
    code_text = text.removeprefix("```\n").removesuffix("```")
    text_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
    return ParentNode("pre", [text_node])

def heading_to_html_node(text: str) -> ParentNode:
    heading_size, heading_text = text.split(" ", maxsplit=1)
    level = len(heading_size)
    if level + 1 >= len(text):
        raise ValueError(f"invalid heading level: {level}")
    tag = f"h{level}"
    return ParentNode(tag, text_to_html_node(heading_text))

def quote_block_to_html(text: str) -> ParentNode:
    new_text_list = []
    for line in text.splitlines():
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_text_list.append(line.lstrip(">").strip())
    new_text = " ".join(new_text_list)
    return ParentNode("blockquote", text_to_html_node(new_text))

def lists_to_html_node(text: str, block_type: BlockType) -> ParentNode:
    block_map = {
        BlockType.ULIST: {
            "pattern": r'^-\s(.*)',
            "tag": "ul",
            },
        BlockType.OLIST: {
            "pattern": r'^\d+\.\s(.*)',
            "tag": "ol",
            }
    }
    list_nodes = []
    for item_text in re.findall(block_map[block_type]["pattern"], text, re.MULTILINE):
        html_node = text_to_html_node(item_text)
        list_nodes.append(ParentNode("li", html_node)) # type: ignore
    return ParentNode(block_map[block_type]["tag"], list_nodes)
        

def block_to_block_type(block: str):
    if all((
            re.match(r'^#{1,6}\s.+', line) 
            for line in block.splitlines()
            )):
        return BlockType.HEADING
    
    if re.match(r'^`{3}\n((.|\n)*)`{3}$', block):
        return BlockType.CODE
    
    if all((
            re.match(r'^>', line)
            for line in block.splitlines()
            )):
        return BlockType.QUOTE
    
    if all((
            re.match(r'^-\s.+', line) 
            for line in block.splitlines()
            )):
        return BlockType.ULIST
    if all((
            re.match(rf'^{i+1}\.', line)
            for i, line in enumerate(block.splitlines())
            )):
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str):
    block_list = []
    blocks = markdown.split('\n\n')
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        block_list.append(block)
    return block_list


def markdown_to_html_node(markdown: str) -> ParentNode:
    markdown_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in markdown_blocks:
        html_blocks.append(text_to_children(block))
    return ParentNode("div", html_blocks)

def extract_title(markdown: str):
    heading_pattern = r'^#\s(.*$)'
    matches = re.findall(heading_pattern, markdown, re.MULTILINE)
    if not matches:
        raise ValueError("Error: No title heading found in markdown")
    return matches[0].strip()