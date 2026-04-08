import unittest
from textnode import TextNode, TextType
from inlinetext import (
    split_nodes_deliminiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link,
    text_to_textnodes,
)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        old_nodes = [TextNode(
            "This is **bold** text", TextType.TEXT
        )]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        actual = split_nodes_deliminiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(actual, expected)
    
    def test_italic(self):
        old_nodes = [TextNode(
            "This is _italic_ text", TextType.TEXT
        )]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        actual = split_nodes_deliminiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(actual, expected)
    
    def test_code(self):
        old_nodes = [TextNode(
            "This is `code` text", TextType.TEXT
        )]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        actual = split_nodes_deliminiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(actual, expected)

    def test_bold_multiword(self):
        old_nodes = [TextNode(
            "This is a line with **bolded words** and more **bolded words**", TextType.TEXT
        )]
        expected = [
            TextNode("This is a line with ", TextType.TEXT),
            TextNode("bolded words", TextType.BOLD),
            TextNode(" and more ", TextType.TEXT),
            TextNode("bolded words", TextType.BOLD),
        ]
        actual = split_nodes_deliminiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(actual, expected)
    
    def test_bold_and_italic(self):
        old_nodes = [TextNode(
            "**bold** text and _italic_", TextType.TEXT
        )]
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        old_nodes = split_nodes_deliminiter(old_nodes, "**", TextType.BOLD)
        actual = split_nodes_deliminiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(actual, expected)

    def test_incorrect_delimiter(self):
        old_nodes = [TextNode(
            "This is **italic** text", TextType.TEXT
        )]
        expected = [TextNode(
            "This is **italic** text", TextType.TEXT
        )]
        actual = split_nodes_deliminiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(actual, expected)

    def test_no_closing_delimiter(self):
        old_nodes = [TextNode(
            "This text is missing `code", TextType.TEXT
        )]
        self.assertRaises(Exception, split_nodes_deliminiter, old_nodes, "`", TextType.CODE)

    def test_nested_cases(self):
        old_nodes = [TextNode("This is **bold** and **more bold** text", TextType.TEXT)]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        actual = split_nodes_deliminiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(actual, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![pic](https://test.com)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"), 
                ("pic", "https://test.com")
            ], matches
        )

    def test_does_not_extract_links(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extracts_multiple_links(self):
        matches = extract_markdown_links(
            "First [link](https://linkone.com) and [two](https://second.coming)"
        )
        self.assertListEqual(
            [
                ("link", "https://linkone.com"),
                ("two", "https://second.coming"),
            ],
            matches
        )

    def test_does_not_extract_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_leave_image(self):
        node = TextNode(
            "This is text with a [link to wikipedia](https://wikipedia.org) and an ![image](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a [link to wikipedia](https://wikipedia.org) and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com"),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode("![image](https://example.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode("text before ![image](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com"),
            ],
            new_nodes,
        )

    def test_no_images_returns_original(self):
        node = TextNode("plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_non_text_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("first ![a](https://a.com) end", TextType.TEXT),
            TextNode("second ![b](https://b.com) end", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("first ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://a.com"),
                TextNode(" end", TextType.TEXT),
                TextNode("second ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "https://b.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link to wikipedia](https://wikipedia.org) and another [special one](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to wikipedia", TextType.LINK, "https://wikipedia.org"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "special one", TextType.LINK, "https://example.com"
                ),
            ],
            new_nodes,
        )

    def test_split_image_leave_link(self):
        node = TextNode(
            "This is text with a [link to wikipedia](https://wikipedia.org) and an ![image](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to wikipedia", TextType.LINK, "https://wikipedia.org"),
                TextNode(" and an ![image](https://example.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_start(self):
        node = TextNode("[click here](https://example.com) for more", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("click here", TextType.LINK, "https://example.com"),
                TextNode(" for more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode("see this [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("see this ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_no_links_returns_original(self):
        node = TextNode("plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_non_text_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("first [a](https://a.com) end", TextType.TEXT),
            TextNode("second [b](https://b.com) end", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("first ", TextType.TEXT),
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode(" end", TextType.TEXT),
                TextNode("second ", TextType.TEXT),
                TextNode("b", TextType.LINK, "https://b.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToNodes(unittest.TestCase):
    def test_multiple_nodes(self):
        text = """This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_plain_text(self):
        actual = text_to_textnodes("just plain text")
        self.assertEqual([TextNode("just plain text", TextType.TEXT)], actual)

    def test_multiline(self):
        text = "First line **bold**\nSecond line _italic_\nThird with [link](https://example.com)"
        actual = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("First line ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("\nSecond line ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode("\nThird with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            actual,
        )

    def test_unclosed_delimiter_raises(self):
        self.assertRaises(Exception, text_to_textnodes, "This has an **unclosed bold")