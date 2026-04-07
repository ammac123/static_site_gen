import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_all_fields_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html_single(self):
        node = HTMLNode("a", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), 'href="https://example.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode("a", props={"href": "https://example.com", "target": "_blank"})
        self.assertIn('href="https://example.com"', node.props_to_html())
        self.assertIn('target="_blank"', node.props_to_html())

    def test_props_to_html_none(self):
        node = HTMLNode("p")
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_raises(self):
        node = HTMLNode("p", "hello")
        self.assertRaises(NotImplementedError, node.to_html)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_props(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.example.com", "target": "_blank"})
        self.assertIn('href="https://www.example.com" target="_blank"', node.to_html())

    def test_to_html_raises(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_returns_raw_text(self):
        node = LeafNode(None, value="Foobar Bingo")
        self.assertEqual(node.to_html(), "Foobar Bingo")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        parent_node = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
        ])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold</b> and <i>italic</i></p>")

    def test_to_html_with_props(self):
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], props={"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>text</span></div>')

    def test_deeply_nested(self):
        node = ParentNode("h2", [
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode("b", "deep")
                ])
            ])
        ])
        self.assertEqual(node.to_html(), "<h2><section><p><b>deep</b></p></section></h2>")

    def test_no_tag_raises(self):
        child = LeafNode("span", "text")
        node = ParentNode(None, [child])  # type: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_empty_tag_raises(self):
        child = LeafNode("span", "text")
        node = ParentNode("", [child])
        self.assertRaises(ValueError, node.to_html)

    def test_empty_children_raises(self):
        node = ParentNode("div", [])
        self.assertRaises(ValueError, node.to_html)

    def test_invalid_child_type_raises(self):
        node = ParentNode("div", ["not an HTMLNode"])  # type: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_mixed_valid_invalid_children_raises(self):
        node = ParentNode("div", [LeafNode("span", "ok"), "not a node"])  # type: ignore
        self.assertRaises(ValueError, node.to_html)

if __name__=="__main__":
    unittest.main()