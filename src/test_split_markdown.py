import unittest
from textnode import TextNode, TextType
from split_markdown import split_nodes_delimiter  # assuming that's your file name

class TestSplitNodesDelimiters(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is just plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bolded phrase")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " in the middle")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_no_closing_delimiter(self):
        node = TextNode("This is text with an unclosed `code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_delimiter_pairs(self):
        node = TextNode("**Bold** text and another **bold** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " text and another ")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, " word")
        self.assertEqual(result[3].text_type, TextType.TEXT)

    def test_mixed_node_types(self):
        text_node = TextNode("Text with **bold** and more text", TextType.TEXT)
        bold_node = TextNode("This is bold", TextType.BOLD)
        italic_node = TextNode("This is italic", TextType.ITALIC)
        more_text_node = TextNode("More text with **bold**", TextType.TEXT)
        nodes = [text_node, bold_node, italic_node, more_text_node]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert len(result) == 7
        assert result[0].text == "Text with "
        assert result[0].text_type == TextType.TEXT
        assert result[1].text == "bold"
        assert result[1].text_type == TextType.BOLD
        assert result[2].text == " and more text"
        assert result[2].text_type == TextType.TEXT
        assert result[3].text == "This is bold"
        assert result[3].text_type == TextType.BOLD
        assert result[4].text == "This is italic"
        assert result[4].text_type == TextType.ITALIC
        assert result[5].text == "More text with "
        assert result[5].text_type == TextType.TEXT
        assert result[6].text == "bold"
        assert result[6].text_type == TextType.BOLD

    def test_nested_delimiters(self):
        node = TextNode("This has *italic* and **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(result) == 3
        assert result[0].text == "This has *italic* and "
        assert result[0].text_type == TextType.TEXT
        assert result[1].text == "bold"
        assert result[1].text_type == TextType.BOLD
        assert result[2].text == " text"
        assert result[2].text_type == TextType.TEXT
        result = split_nodes_delimiter(result, "*", TextType.ITALIC)
        assert len(result) == 5
        assert result[0].text == "This has "
        assert result[0].text_type == TextType.TEXT
        assert result[1].text == "italic"
        assert result[1].text_type == TextType.ITALIC
        assert result[2].text == " and "
        assert result[2].text_type == TextType.TEXT
        assert result[3].text == "bold"
        assert result[3].text_type == TextType.BOLD
        assert result[4].text == " text"
        assert result[4].text_type == TextType.TEXT
        

    def test_nested_delimiters_multiple(self):
        """Test text with multiple nested delimiters."""
        text = "**Bold and *italic* and again **bold** text**"
        node = TextNode(text, TextType.TEXT)
    
    # Instead of trying to process everything at once:
    # result = split_nodes_delimiter([node], "**", TextType.BOLD)
    
    # Process bold first
        intermediate_result = split_nodes_delimiter([node], "**", TextType.BOLD)
    
    # Then process italic on the result from bold
        result = split_nodes_delimiter(intermediate_result, "*", TextType.ITALIC)
    
        #print("Result length:", len(result))
        #for i, n in enumerate(result):
            #print(f"Node {i}: {repr(n.text)} (type: {n.text_type})")
        
    # Expected behavior when processing ** then *:
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Bold and ")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " and again ")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "bold")
        self.assertEqual(result[3].text_type, TextType.TEXT)
        self.assertEqual(result[4].text, " text")
        self.assertEqual(result[4].text_type, TextType.BOLD)


    def test_nested_delimiters_mixed(self):
        """Test text with mixed nested delimiters."""
        node = TextNode("**Bold and *italic* and again **bold** text** and again **bold** and *italic*", TextType.TEXT)
    
    # Process ** for BOLD first
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
    # Process * for ITALIC next
        result = split_nodes_delimiter(result, "*", TextType.ITALIC)
    
        #print("\nMixed delimiters input:", repr(node.text))
        #print("Result length:", len(result))
        #for i, n in enumerate(result):
            #print(f"Node {i}: {repr(n.text)} (type: {n.text_type})")
    
    # Expected behavior when processing ** then *:
        self.assertEqual(len(result), 9)
        self.assertEqual(result[0].text, "Bold and ")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " and again ")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "bold")
        self.assertEqual(result[3].text_type, TextType.TEXT)
        self.assertEqual(result[4].text, " text")
        self.assertEqual(result[4].text_type, TextType.BOLD)
        self.assertEqual(result[5].text, " and again ")
        self.assertEqual(result[5].text_type, TextType.TEXT)
        self.assertEqual(result[6].text, "bold")
        self.assertEqual(result[6].text_type, TextType.BOLD)
        self.assertEqual(result[7].text, " and ")
        self.assertEqual(result[7].text_type, TextType.TEXT)
        self.assertEqual(result[8].text, "italic")
        self.assertEqual(result[8].text_type, TextType.ITALIC)

    # Commenting out the problematic tests
    def test_sequential_processing(self):
        """Test sequential processing of different delimiters."""
        node = TextNode("Regular text with **bold** and `code` and *italic*", TextType.TEXT)
    
    #     # First process bold
        result1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result1), 3)
        self.assertEqual(result1[0].text, "Regular text with ")
        self.assertEqual(result1[0].text_type, TextType.TEXT)
        self.assertEqual(result1[1].text, "bold")
        self.assertEqual(result1[1].text_type, TextType.BOLD)
        self.assertEqual(result1[2].text, " and `code` and *italic*")
        self.assertEqual(result1[2].text_type, TextType.TEXT)
    
    #     # Then process code
        result2 = split_nodes_delimiter(result1, "`", TextType.CODE)
        self.assertEqual(len(result2), 5)
        self.assertEqual(result2[0].text, "Regular text with ")
        self.assertEqual(result2[0].text_type, TextType.TEXT)
        self.assertEqual(result2[1].text, "bold")
        self.assertEqual(result2[1].text_type, TextType.BOLD)
        self.assertEqual(result2[2].text, " and ")
        self.assertEqual(result2[2].text_type, TextType.TEXT)
        self.assertEqual(result2[3].text, "code")
        self.assertEqual(result2[3].text_type, TextType.CODE)
        self.assertEqual(result2[4].text, " and *italic*")
        self.assertEqual(result2[4].text_type, TextType.TEXT)
    
    #     # Finally process italic
        result3 = split_nodes_delimiter(result2, "*", TextType.ITALIC)
        #for i, node in enumerate(result3):
            #print(f"Node {i}: '{node.text}' (type: {node.text_type})")
        self.assertEqual(len(result3), 6)
        self.assertEqual(result3[0].text, "Regular text with ")
        self.assertEqual(result3[0].text_type, TextType.TEXT)
        self.assertEqual(result3[1].text, "bold")
        self.assertEqual(result3[1].text_type, TextType.BOLD)
        self.assertEqual(result3[2].text, " and ")
        self.assertEqual(result3[2].text_type, TextType.TEXT)
        self.assertEqual(result3[3].text, "code")
        self.assertEqual(result3[3].text_type, TextType.CODE)
        self.assertEqual(result3[4].text, " and ")
        self.assertEqual(result3[4].text_type, TextType.TEXT)
        self.assertEqual(result3[5].text, "italic")
        self.assertEqual(result3[5].text_type, TextType.ITALIC)


if __name__ == '__main__':
    unittest.main()