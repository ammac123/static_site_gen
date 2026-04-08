from __future__ import annotations
from typing import List, Dict, Optional

class HTMLNode:
    def __init__(
                self, 
                tag: Optional[str] = None, 
                value: Optional[str] = None, 
                children: Optional[List[HTMLNode]] = None, 
                props: Optional[Dict] = None,
            ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ''
        res = []
        for key, value in self.props.items():
            res.append(f'{key}="{value}"')
        return " ".join(res)
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(
                self, 
                tag: str | None, 
                value: str | None, 
                props: Dict | None = None
            ) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("All leafnodes must have a value")
        if not self.tag:
            return str(self.value)
        if props := self.props_to_html():
            props = ' ' + props
        return (
            '<' + self.tag + props + '>' + 
            self.value + 
            '</' + self.tag + '>'
        )
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(
                self, 
                tag: str, 
                children: List[HTMLNode], 
                props: Dict | None = None
            ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parentnodes must have a tag")
        if not self.children or not all(isinstance(n, HTMLNode) for n in self.children):
            raise ValueError("Children of parentnode are not of type HTMLNode")
        if props := self.props_to_html():
            props = ' ' + props
        return (
            '<' + self.tag + props + '>' +
            ''.join([child.to_html() for child in self.children]) +
            '</' + self.tag + '>'
        )