import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is an italic node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode("Sample text", TextType.CODE)
        self.assertIsNone(node.url)

    def test_url_not_none(self):
        url = "www.test.image.png"
        node = TextNode("Alt text for image", TextType.IMAGE, url)
        self.assertIsNotNone(node.url)
        self.assertEqual(node.url, url)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("a cat", TextType.IMAGE, url="https://example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://example.com/cat.png", "alt": "a cat"})

    def test_link_renders_to_html(self):
        node = TextNode("click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">click here</a>')

    def test_image_value_is_none(self):
        # img nodes have no text value — to_html() should raise since LeafNode requires a value
        node = TextNode("a cat", TextType.IMAGE, url="https://example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.value)

if __name__=="__main__":
    unittest.main()