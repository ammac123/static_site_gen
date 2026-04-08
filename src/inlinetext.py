from typing import List
from textnode import TextNode, TextType

def split_nodes_deliminiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
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
            new_nodes.extend([
                TextNode(raw_text, TextType.TEXT), 
                TextNode(inline_text, text_type)]
                )
        new_nodes.extend([TextNode(current_text, TextType.TEXT)])
    return new_nodes