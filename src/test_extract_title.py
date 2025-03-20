import unittest
from markdown_blocks import extract_title  # Replace with your actual module name

class TestExtractTitle(unittest.TestCase):
    
    def test_basic_title(self):
        markdown = "# Hello World\nThis is some content."
        expected = "Hello World"
        self.assertEqual(extract_title(markdown), expected)
    
    def test_title_with_extra_whitespace(self):
        markdown = "#    Extra Spaces    \nMore content."
        expected = "Extra Spaces"
        self.assertEqual(extract_title(markdown), expected)
    
    def test_no_title_raises_exception(self):
        markdown = "This markdown has no title\nJust content."
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_my_title(self):
        markdown = "# I don't need your help\nI can do it myself.\n I'm a big boy now.\n and I am better then this."
        expected = "I don't need your help"
        self.assertEqual(extract_title(markdown), expected)
        
if __name__ == '__main__':
    unittest.main()