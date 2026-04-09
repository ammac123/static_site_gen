import re
from typing import List
from textnode import TextNode, TextType

def split_nodes_deliminiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        while delimiter in current_text:
            try:
                raw_text, inline_text, current_text = current_text.split(sep=delimiter, maxsplit=2)
            except:
                raise Exception("Invalid Markdown syntax")
            if raw_text:
                new_nodes.append(TextNode(raw_text, TextType.TEXT))
            new_nodes.append(TextNode(inline_text, text_type))
        if current_text:
            new_nodes.extend([TextNode(current_text, TextType.TEXT)])
    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        for image in extract_markdown_images(current_text):
            alt_text, url = image
            try:
                raw_text, current_text = current_text.split(f'![{alt_text}]({url})', maxsplit=1)
            except:
                raise Exception("Invalid inline Markdown image")
            if raw_text:
                new_nodes.append(TextNode(raw_text, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        if current_text:
            new_nodes.extend([TextNode(current_text, TextType.TEXT)])
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        for image in extract_markdown_links(current_text):
            value, url = image
            try:
                raw_text, current_text = current_text.split(f'[{value}]({url})', maxsplit=1)
            except:
                raise Exception("Invalid inline Markdown link")
            if raw_text:
                new_nodes.append(TextNode(raw_text, TextType.TEXT))
            new_nodes.append(TextNode(value, TextType.LINK, url))
        if current_text:
            new_nodes.extend([TextNode(current_text, TextType.TEXT)])
    return new_nodes

def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_deliminiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_deliminiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_deliminiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_markdown_images(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r'(?<!!)\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches