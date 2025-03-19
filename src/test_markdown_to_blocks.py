import unittest
from split_markdown import markdown_to_blocks

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
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_empty_lines(self):
        md = "\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_empty_lines_with_text(self):
        md = "\n\nThis is a paragraph\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph"])

    def test_markdown_to_blocks_single_block(self):
        md = "Just a simple block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a simple block"])

    def test_markdown_to_blocks_multiple_blank_lines(self):
        md = """
This is the first block


This is the second block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is the first block",
            "This is the second block"
        ])

    def test_markdown_to_blocks_mixed_content(self):
        md = """
# Heading 1

Paragraph with *italic* and **bold** text.

- List item one
- List item two

Another paragraph with `code`.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "# Heading 1",
            "Paragraph with *italic* and **bold** text.",
            "- List item one\n- List item two",
            "Another paragraph with `code`."
        ])

    def test_markdown_to_blocks_whitespace(self):
        md = """
     
     First block with spaces   
     
     
         Second block starts with whitespace
     
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "First block with spaces",
            "Second block starts with whitespace"
        ])

    def test_markdown_to_blocks_special_characters(self):
        md = """
This is a divider:

---

This is another block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is a divider:",
            "---",
            "This is another block"
        ])

    def test_markdown_to_blocks_empty_surrounded_by_blank_lines(self):
        md = """

This is the first block


This is the second block


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is the first block",
            "This is the second block"
        ])

    def test_markdown_to_blocks_blocks_of_whitespace(self):
        md = """
This is a valid block

          

This is another valid block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is a valid block",
            "This is another valid block"
        ])

    def test_markdown_to_blocks_newline_characters_only(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_consecutive_single_line_blocks(self):
        md = """
This is line one of the block
This is still part of the same block

This is a new block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is line one of the block\nThis is still part of the same block",
            "This is a new block"
        ])

    def test_markdown_to_blocks_non_text_blocks(self):
        md = """
@@@@@

####

123456
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "@@@@@",
            "####",
            "123456"
        ])

    def test_markdown_to_blocks_long_blocks(self):
        md = "This is a single block\n" * 500
        blocks = markdown_to_blocks(md.strip())  # Strip trailing newline in md
        self.assertEqual(blocks, [md.strip()])  # Single block with all lines combined)

    def test_markdown_to_blocks_international_text(self):
        md = """
这是一个段落

这是另一个段落

😊🔥🚀 <-- This is a paragraph of emojis
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "这是一个段落",
            "这是另一个段落",
            "😊🔥🚀 <-- This is a paragraph of emojis"
        ])

    def test_markdown_to_blocks_delimiters_before_or_after_content(self):
        md = """

\n\n
Content starts immediately after odd delimiters

\n\n
Another block follows
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Content starts immediately after odd delimiters",
            "Another block follows"
        ])

    def test_markdown_to_blocks_unusual_markdown_constructs(self):
        md = """
> This is a blockquote

~~This is strikethrough text~~

***

A horizontal rule above this paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "> This is a blockquote",
            "~~This is strikethrough text~~",
            "***",
            "A horizontal rule above this paragraph"
        ])

    def test_markdown_to_blocks_fenced_code(self):
        md = """
```
This is a code block
It has multiple lines

It even has blank lines
```

This is a new paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "```\nThis is a code block\nIt has multiple lines\n\nIt even has blank lines\n```",
            "This is a new paragraph"
        ])

if __name__ == "__main__":
    unittest.main()