import unittest
from split_markdown import markdown_to_html_node
from htmlnode import HTMLNode

print(markdown_to_html_node)  #debug
print(HTMLNode)  #debug

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

    def test_headers(self):
        md = """
        # header 1
        ## header 2
        ### header 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>header 1</h1><h2>header 2</h2><h3>header 3</h3></div>",
        )

    def test_unordered_lists(self):
        md = """
        - item 1
        - item 2
        - item 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>",
        )

    def test_ordered_lists(self):
        md = """
        1. item 1
        2. item 2
        3. item 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item 1</li><li>item 2</li><li>item 3</li></ol></div>",
        )

    def test_block_quotes(self):
        md = """
        > This is a block quote
        > with multiple lines
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a block quote with multiple lines</blockquote></div>",
        )

    def test_bold_text(self):
        md = """
        This is **bolded** text
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>This is <b>bolded</b> text</div>",
        )
    
    def test_italic_text(self):
        md = """
        This is _italic_
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>This is <i>italic</i></div>",
        )

    def test_code_span(self):
        md = """
        This is `code`
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>This is <code>code</code></div>",
        )
    
    def test_link(self):
        md = """
        [link](https://google.com)
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><a href="https://google.com">link</a></div>',
        )

    def test_mixed_content(self):
        md = """
        # header 1
        - item 1
        - item 2
        - item 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>header 1</h1><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>',
        )

    def test_empty_document(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_malformed_markdown(self):
        # Markdown with unmatched bold delimiter
        md = """
This is a paragraph with **bold text that never closes
        """
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)

    def test_unmatched_code_block(self):
        # Markdown with unmatched code block
        md = """ 
        ```   
Code block that never closes
        """
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)


    def test_extra_whitespace_between_blocks(self):
        md = """
        This is a paragraph
        
        This is another paragraph
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph</p><p>This is another paragraph</p></div>",
        )

    def test_nested_formatting(self):
        md = """
        This is a **bolded _italic_** paragraph
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>This is a <b>bolded <i>italic</i></b> paragraph</div>",
        )
    
    def test_header_with_inline_formatting(self):
        md = """
        # This is a **bolded _italic_** header
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>bolded <i>italic</i></b> header</h1></div>",
        )

    def test_list_with_multiple_levels_or_inline_formatting(self):
        md = """
        - item 1
        - item 2
            - item 2.1
            - item 2.2
        - item 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2<ul><li>item 2.1</li><li>item 2.2</li></ul></li><li>item 3</li></ul></div>",
        )

    def test_list_with_nested_lists(self):
        md = """
        - item 1
        - item 2
            1. item 2.1
            2. item 2.2
        - item 3
        """
        print("Input markdown:")
        print(repr(md))
    
        node = markdown_to_html_node(md)
        html = node.to_html()
    
        print("Your output HTML:")
        print(repr(html))
    
        expected = "<div><ul><li>item 1</li><li>item 2<ol><li>item 2.1</li><li>item 2.2</li></ol></li><li>item 3</li></ul></div>"
        print("Expected HTML:")
        print(repr(expected))
    
        self.assertEqual(html, expected)

    def test_nested_block_quotes(self):
        md = """
        > This is a block quote
        > with multiple lines
        > > and nested block quotes
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a block quote with multiple lines<blockquote>and nested block quotes</blockquote></blockquote></div>",
        )

    def test_list_with_block_quotes(self):
        md = """
        - item 1
        - item 2
            > block quote
        - item 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2<blockquote>block quote</blockquote></li><li>item 3</li></ul></div>",
        )

    def test_list_with_code_blocks(self):
        md = """
        - item 1
        - item 2
            ```
            code block
            ```
        - item 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2<pre><code>code block\n</code></pre></li><li>item 3</li></ul></div>",
        )

    def test_code_block_with_inline_formatting(self):
        md = """
        ```
        this is `code` with **bold**
        ```
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>this is <code>code</code> with <b>bold</b>\n</code></pre></div>",
        )

    def test_code_block_with_nested_code_blocks(self):
        md = """
        ```
        this is `code` with
        ```
        ```
        nested `code`
        ```
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>this is <code>code</code> with\n</code></pre><pre><code>nested <code>code</code>\n</code></pre></div>",
        )

    def test_code_block_with_nested_formatting(self):
        md = """
        ```
        this is `code` with **bold**
        ```
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>this is <code>code</code> with <b>bold</b>\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()