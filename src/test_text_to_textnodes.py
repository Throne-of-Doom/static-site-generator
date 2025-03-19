import unittest
import re
from textnode import TextNode, TextType
from split_markdown import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_simple_text(self):
        """Test case 1: Simple text with no markdown"""
        text = "Hello, world!"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "Hello, world!"
        assert nodes[0].text_type == TextType.TEXT
        
    def test_bold_text(self):
        """Test case 2: Bold text"""
        text = "Hello, **world**!"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "Hello, "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "world"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == "!"
        assert nodes[2].text_type == TextType.TEXT
        
    def test_combination_of_elements(self):
        """Test case 3: Combination of elements"""
        text = "This is **bold** and _italic_ text with a `code block`"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 6
        assert nodes[0].text == "This is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " and "
        assert nodes[2].text_type == TextType.TEXT
        assert nodes[3].text == "italic"
        assert nodes[3].text_type == TextType.ITALIC
        assert nodes[4].text == " text with a "
        assert nodes[4].text_type == TextType.TEXT
        assert nodes[5].text == "code block"
        assert nodes[5].text_type == TextType.CODE
        
    def test_links_and_images(self):
        """Test case 4: Links and images"""
        text = "Check out this [link](https://boot.dev) and ![image](https://example.com/image.jpg)"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 4
        assert nodes[0].text == "Check out this "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "link"
        assert nodes[1].text_type == TextType.LINK
        assert nodes[1].url == "https://boot.dev"
        assert nodes[2].text == " and "
        assert nodes[2].text_type == TextType.TEXT
        assert nodes[3].text == "image"
        assert nodes[3].text_type == TextType.IMAGE
        assert nodes[3].url == "https://example.com/image.jpg"
        
    def test_complex_combination(self):
        """Test case 5: Complex combination"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 10
        assert nodes[0].text == "This is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "text"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " with an "
        assert nodes[2].text_type == TextType.TEXT
        assert nodes[3].text == "italic"
        assert nodes[3].text_type == TextType.ITALIC
        assert nodes[4].text == " word and a "
        assert nodes[4].text_type == TextType.TEXT
        assert nodes[5].text == "code block"
        assert nodes[5].text_type == TextType.CODE
        assert nodes[6].text == " and an "
        assert nodes[6].text_type == TextType.TEXT
        assert nodes[7].text == "obi wan image"
        assert nodes[7].text_type == TextType.IMAGE
        assert nodes[7].url == "https://i.imgur.com/fJRm4Vk.jpeg"
        assert nodes[8].text == " and a "
        assert nodes[8].text_type == TextType.TEXT
        assert nodes[9].text == "link"
        assert nodes[9].text_type == TextType.LINK
        assert nodes[9].url == "https://boot.dev"
        
    def test_nested_markdown(self):
        """Test case 6: Nested markdown (which should be handled as plain text as per most implementations)"""
        text = "**Bold with _italic_ inside**"
        nodes = text_to_textnodes(text)
        # The exact behavior may depend on your implementation, but this tests that something reasonable happens
        assert len(nodes) >= 1
        
    def test_empty_string(self):
        """Test case 7: Empty string"""
        text = ""
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == ""
        assert nodes[0].text_type == TextType.TEXT

    def test_unmatched_delimiters(self):
        """Edge case 1: Unmatched delimiters"""
        text = "This has an **unmatched bold delimiter"
        try:
            nodes = text_to_textnodes(text)
            assert False, "Expected an exception for unmatched delimiter"
        except Exception as e:
            assert "No closing delimiter" in str(e)
        
    def test_delimiters_with_no_content(self):
        """Edge case 2: Delimiters with no content"""
        text = "This has an **** empty bold section"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "This has an **** empty bold section"
        assert nodes[0].text_type == TextType.TEXT
        
    def test_multiple_consecutive_markdown_elements(self):
        """Edge case 3: Multiple consecutive markdown elements"""
        text = "Multiple **bold** _italic_ `code` sections"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 7
        assert nodes[0].text == "Multiple "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " "
        assert nodes[2].text_type == TextType.TEXT
        assert nodes[3].text == "italic"
        assert nodes[3].text_type == TextType.ITALIC
        assert nodes[4].text == " "
        assert nodes[4].text_type == TextType.TEXT
        assert nodes[5].text == "code"
        assert nodes[5].text_type == TextType.CODE
        assert nodes[6].text == " sections"
        assert nodes[6].text_type == TextType.TEXT

    def test_urls_with_special_characters(self):
        """Edge case 4: URLs with special characters"""
        text = "[Link](https://example.com/path?query=value&more=stuff)"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "Link"
        assert nodes[0].text_type == TextType.LINK
        assert nodes[0].url == "https://example.com/path?query=value&more=stuff"
        
    def test_adjacent_markdown_elements_without_spaces(self):
        """Edge case 5: Adjacent markdown elements without spaces"""
        text = "**Bold**_Italic_`Code`"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "Bold"
        assert nodes[0].text_type == TextType.BOLD
        assert nodes[1].text == "Italic"
        assert nodes[1].text_type == TextType.ITALIC
        assert nodes[2].text == "Code"
        assert nodes[2].text_type == TextType.CODE
        
    def test_mix_of_links_and_images(self):
        """Edge case 6: Mix of links and images"""
        text = "Check this [link](https://boot.dev) and ![image](https://example.com/img.jpg) out"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 5
        assert nodes[0].text == "Check this "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "link"
        assert nodes[1].text_type == TextType.LINK
        assert nodes[1].url == "https://boot.dev"
        assert nodes[2].text == " and "
        assert nodes[2].text_type == TextType.TEXT
        assert nodes[3].text == "image"
        assert nodes[3].text_type == TextType.IMAGE
        assert nodes[3].url == "https://example.com/img.jpg"
        assert nodes[4].text == " out"

    def test_empty_url_in_link(self):
        """Edge case 7: Empty URL in link"""
        text = "[Link with empty URL]()"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "Link with empty URL"
        assert nodes[0].text_type == TextType.LINK
        assert nodes[0].url == ""
        
    def test_multiple_sequential_delimiters_of_same_type(self):
        """Edge case 8: Multiple sequential delimiters of same type"""
        text = "Text with **bold** and then more **bold text**"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 5
        assert nodes[0].text == "Text with "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " and then more "
        assert nodes[2].text_type == TextType.TEXT
        assert nodes[3].text == "bold text"
        assert nodes[3].text_type == TextType.BOLD
        assert nodes[4].text == ""
        assert nodes[4].text_type == TextType.TEXT
        
    def test_unicode_characters(self):
        """Edge case 9: Unicode characters"""
        text = "Unicode: **你好** and _😊_"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 4
        assert nodes[0].text == "Unicode: "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "你好"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " and "
        assert nodes[2].text_type == TextType.TEXT
        assert nodes[3].text == "😊"
        assert nodes[3].text_type == TextType.ITALIC
        
if __name__ == "__main__":
    unittest.main()
