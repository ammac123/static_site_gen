import unittest
from markdown_blocks import (
    BlockType,
    markdown_to_blocks, 
    block_to_block_type,
    markdown_to_html_node,
    extract_title,
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_block(self):
        md = """


"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [],
        )
    
    def test_excessive_newlines(self):
        md = """# Header is here




- List is here
- And here
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "# Header is here",
                "- List is here\n- And here"
            ]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading one"), BlockType.HEADING)

    def test_heading_max_level(self):
        self.assertEqual(block_to_block_type("###### Heading six"), BlockType.HEADING)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> a quote\n> more quote"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item one\n- item two\n- item three"), BlockType.ULIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.OLIST)

    def test_ordered_list_out_of_order_is_paragraph(self):
        self.assertEqual(block_to_block_type("1. first\n3. skipped\n4. fourth"), BlockType.PARAGRAPH)

    def test_paragraph_fallback(self):
        self.assertEqual(block_to_block_type("just a normal paragraph"), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### too many"), BlockType.PARAGRAPH)


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_levels(self):
        md = """# H1

## H2

### H3

###### H6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3><h6>H6</h6></div>",
        )

    def test_heading_with_inline(self):
        md = "## Hello **world**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>Hello <b>world</b></h2></div>")

    def test_blockquote(self):
        md = """> This is a quote
> with multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines</blockquote></div>",
        )

    def test_blockquote_with_inline(self):
        md = "> A quote with **bold** and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>A quote with <b>bold</b> and <i>italic</i></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """- first item
- second item
- third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second item</li><li>third item</li></ul></div>",
        )

    def test_unordered_list_with_inline(self):
        self.maxDiff = None
        md = """- item with **bold**
- item with _italic_
- item with `code`
- [item with a link](/item/link)
- ![alttext with an image](/item/image.png)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            """<div><ul>""" + 
            """<li>item with <b>bold</b></li>""" +
            """<li>item with <i>italic</i></li>""" + 
            """<li>item with <code>code</code></li>""" + 
            """<li><a href="/item/link">item with a link</a></li>""" + 
            """<li><img src="/item/image.png" alt="alttext with an image"></img></li>""" + 
            """</ul></div>""",
        )

    def test_ordered_list(self):
        md = """1. first
2. second
3. third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_code_preserves_content(self):
        md = "```\n`backtick` content\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>`backtick` content\n</code></pre></div>",
        )

    def test_mixed_blocks(self):
        md = """# Title

A paragraph with **bold**.

- list item one
- list item two

> a quote

1. ordered one
2. ordered two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Title</h1>"
            "<p>A paragraph with <b>bold</b>.</p>"
            "<ul><li>list item one</li><li>list item two</li></ul>"
            "<blockquote>a quote</blockquote>"
            "<ol><li>ordered one</li><li>ordered two</li></ol>"
            "</div>",
        )

class TestExtractMarkdownHeading(unittest.TestCase):
    def test_extract_title(self):
        actual = extract_title("# Hello title ")
        self.assertEqual(
            actual,
            "Hello title"
        )
    
    def test_multiple_headings(self):
        markdown = """
### This is not the heading we want

## Neither is this

# Correct Title

# Incorrect Title
"""
        actual = extract_title(markdown)
        self.assertEqual(
            actual,
            "Correct Title"
        )
    
    def test_no_heading(self):
        markdown = """
### Not title heading

#Misformatted title heading too

## Also incorrect

What is this doing here
"""
        self.assertRaises(ValueError, extract_title, markdown)