import unittest
from textnode import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        """Test a simple paragraph with no special formatting."""
        markdown = "This is a simple paragraph with no special formatting."
        self.assertEqual(block_to_block_type(markdown), BlockType.paragraph)
        
    def test_heading(self):
        """Test various valid and invalid headings."""
        # Test valid headings of different levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.heading)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.heading)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.heading)
        
        # Test invalid headings
        self.assertEqual(block_to_block_type("#Invalid heading without space"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("####### Too many hashtags"), BlockType.paragraph)
    
    def test_code(self):
        """Test various valid and invalid code blocks."""
        # Test a simple code block
        code_block = "```\ndef hello_world():\n    print('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.code)
        
        # Test an invalid code block (missing closing backticks)
        invalid_code = "```\nprint('Hello')"
        self.assertEqual(block_to_block_type(invalid_code), BlockType.paragraph)

    def test_quote(self):
        """Test various valid and invalid quotes."""
        # Test a simple quote
        quote = "> This is a quote"
        self.assertEqual(block_to_block_type(quote), BlockType.quote)
        
        # Test an invalid quote (missing closing angle bracket)
        invalid_quote = "> This is a first line\nThis second line doesn't start with >"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.paragraph)

    def test_unordered_list(self):
        """Test various valid and invalid unordered lists."""
        # Test a simple unordered list
        unordered_list = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(unordered_list), BlockType.unordered_list)
        
        # Test an invalid unordered list (missing hyphen)
        invalid_list = "Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(invalid_list), BlockType.paragraph)

    def test_ordered_list(self):
        """Test various valid and invalid ordered lists."""
        # Test a simple ordered list
        ordered_list = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(ordered_list), BlockType.ordered_list)
    
        # Test an invalid ordered list (missing period)
        invalid_list = "1 Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(invalid_list), BlockType.paragraph)
    
        # Test a non-sequential list (skips number 2)
        non_sequential_list = "1. Item 1\n3. Item 3\n4. Item 4"
        self.assertEqual(block_to_block_type(non_sequential_list), BlockType.paragraph)
    
        # Test a list that doesn't start at 1
        wrong_start_list = "2. Item 2\n3. Item 3\n4. Item 4"
        self.assertEqual(block_to_block_type(wrong_start_list), BlockType.paragraph)

    def test_multi_line_paragraph(self):
        """Test a multi-line paragraph."""
        multi_line = "This is a paragraph\nwith multiple lines\nthat should be treated as one block."
        self.assertEqual(block_to_block_type(multi_line), BlockType.paragraph)

    def test_edge_case_headings(self):
        """Test various edge cases for headings."""
        # Test heading with exactly 6 hashtags (maximum allowed)
        self.assertEqual(block_to_block_type("###### Level 6 heading"), BlockType.heading)
    
        # Test heading with 7 hashtags (should be paragraph)
        self.assertEqual(block_to_block_type("####### Too many hashtags"), BlockType.paragraph)
    
        # Test heading without content
        self.assertEqual(block_to_block_type("# "), BlockType.heading)

    def test_complex_code_blocks(self):
        """Test various complex code blocks."""
        # Test code block with language specification
        code_with_lang = "```python\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(code_with_lang), BlockType.code)
    
        # Test code block with backticks inside (should still work)
        nested_backticks = "```\nThis has a `backtick` inside\n```"
        self.assertEqual(block_to_block_type(nested_backticks), BlockType.code)

    def test_complex_quotes(self):
        """Test various complex quotes."""
        # Test multi-line quote
        multi_line_quote = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(multi_line_quote), BlockType.quote)
    
        # Test quote with blank lines that still have >
        quote_with_blanks = "> Line 1\n>\n> Line 3"
        self.assertEqual(block_to_block_type(quote_with_blanks), BlockType.quote)

    def test_complex_unordered_lists(self):
        """Test various complex unordered lists."""
        # Test unordered list with blank lines (not proper markdown, should fail)
        list_with_blanks = "- Item 1\n\n- Item 2"
        self.assertEqual(block_to_block_type(list_with_blanks), BlockType.paragraph)
    
        # Test unordered list with different indentation (should still work if all lines start with -)
        indented_list = "- Item 1\n- Item 2\n  - Subitem"
        self.assertEqual(block_to_block_type(indented_list), BlockType.unordered_list)

    def test_complex_ordered_lists(self):
        """Test various complex ordered lists."""
        # Test ordered list with many items
        long_list = "1. Item 1\n2. Item 2\n3. Item 3\n4. Item 4\n5. Item 5"
        self.assertEqual(block_to_block_type(long_list), BlockType.ordered_list)
    
        # Test ordered list with double-digit numbers
        double_digit = "1. Item 1\n2. Item 2\n...\n10. Item 10\n11. Item 11"
        self.assertEqual(block_to_block_type(double_digit), BlockType.ordered_list)
    
        # Test with extra spaces after the period (should still work)
        extra_spaces = "1.  Item 1\n2.  Item 2"
        self.assertEqual(block_to_block_type(extra_spaces), BlockType.paragraph)  # Strict checking

    def test_empty_block(self):
        """Test an empty block (should be paragraph)."""
        self.assertEqual(block_to_block_type(""), BlockType.paragraph)

    def test_mixed_content(self):
        """Test content that looks like multiple types but should be paragraph."""
        # Content that looks like multiple types but should be paragraph
        mixed = "This starts like paragraph\n- But has a list item\n> And a quote"
        self.assertEqual(block_to_block_type(mixed), BlockType.paragraph)
    
        # Content that has code markers in the middle (not a code block)
        code_markers = "This has ```code markers``` inside"
        self.assertEqual(block_to_block_type(code_markers), BlockType.paragraph)
    
        # Content that has hashtags in the middle (not a heading)
        hashtags = "This has # hashtags inside"
        self.assertEqual(block_to_block_type(hashtags), BlockType.paragraph)

    def test_tricky_edge_cases(self):
        """Test various tricky edge cases."""
        # Test a block with just three backticks (should be code)
        just_backticks = "```\n```"
        self.assertEqual(block_to_block_type(just_backticks), BlockType.code)
    
        # Test a line that starts with number but isn't a list
        number_start = "1989 was a good year."
        self.assertEqual(block_to_block_type(number_start), BlockType.paragraph)
    
        # Test a line with just a single hashtag (should be heading)
        just_hashtag = "# "
        self.assertEqual(block_to_block_type(just_hashtag), BlockType.heading)
    
        # Test list-like but not quite right
        almost_list = "- Item 1\n -Item 2"  # Missing space after the second hyphen
        self.assertEqual(block_to_block_type(almost_list), BlockType.paragraph)
    
        # Test ordered list with no space after period
        no_space = "1.Item 1\n2.Item 2"
        self.assertEqual(block_to_block_type(no_space), BlockType.paragraph)

if __name__ == "__main__":
    unittest.main()