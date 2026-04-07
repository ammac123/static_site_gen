import unittest

from textnode import TextNode, TextType

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

if __name__=="__main__":
    unittest.main()