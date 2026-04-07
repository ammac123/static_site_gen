import unittest
from htmlnode import HTMLNode, LeafNode

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
        

if __name__=="__main__":
    unittest.main()