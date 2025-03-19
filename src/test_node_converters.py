import unittest
from textnode import TextNode, TextType
from node_converters import text_node_to_html_node

class TestNodeConverters(unittest.TestCase):

    def setUp(self):
        self.example_url = "https://www.example.com"
        self.example_image_url = "https://www.example.com/image.jpg"

        # Commonly used nodes
        self.text_node = TextNode("This is a text node", TextType.TEXT)
        self.bold_node = TextNode("Bold text example", TextType.BOLD)
        self.italic_node = TextNode("Italic text example", TextType.ITALIC)
        self.link_node = TextNode("Link text example", TextType.LINK, self.example_url)
        self.image_node = TextNode("Image example", TextType.IMAGE, self.example_image_url)

    # Tests for different TextTypes
    def test_text(self):
        """Test conversion of a TEXT TextNode to an HTMLNode."""
        html_node = text_node_to_html_node(self.text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        """Test conversion of a BOLD TextNode to an HTMLNode."""
        html_node = text_node_to_html_node(self.bold_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text example")

    def test_italic(self):
        """Test conversion of an ITALIC TextNode to an HTMLNode."""
        html_node = text_node_to_html_node(self.italic_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text example")

    def test_link(self):
        """Test conversion of a LINK TextNode to an HTMLNode."""
        html_node = text_node_to_html_node(self.link_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text example")
        self.assertEqual(html_node.props["href"], self.example_url)

    def test_image(self):
        """Test conversion of an IMAGE TextNode to an HTMLNode."""
        html_node = text_node_to_html_node(self.image_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], self.example_image_url)
        self.assertEqual(html_node.props["alt"], "Image example")

    # Tests for missing attributes
    def test_link_missing_url(self):
        """Test that a LINK TextNode without a URL raises a ValueError."""
        node = TextNode("Link text example", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_missing_url(self):
        """Test that an IMAGE TextNode without a URL raises a ValueError."""
        node = TextNode("Image example", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    # Tests for invalid types
    def test_invalid_type(self):
        """Test that an invalid TextType raises a ValueError."""
        node = TextNode("Invalid text example", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_missing_text_type(self):
        """Test that a missing TextType raises a ValueError."""
        node = TextNode("Missing type", None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    # Tests for empty values
    def test_empty_text(self):
        """Test conversion of an empty TEXT TextNode to an HTMLNode."""
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

    def test_empty_link(self):
        """Test conversion of an empty LINK TextNode to an HTMLNode."""
        node = TextNode("", TextType.LINK, self.example_url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["href"], self.example_url)

    def test_empty_image(self):
        """Test conversion of an empty IMAGE TextNode to an HTMLNode."""
        node = TextNode("", TextType.IMAGE, self.example_image_url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], self.example_image_url)
        self.assertEqual(html_node.props["alt"], "")

    def test_empty_link_url(self):
        """Test that a LINK TextNode with an empty URL raises a ValueError."""
        node = TextNode("Empty link url", TextType.LINK, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_empty_image_url(self):
        """Test that an IMAGE TextNode with an empty URL raises a ValueError."""
        node = TextNode("Empty image url", TextType.IMAGE, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_valid_text_types(self):
        """Test conversion of valid TextNode types to HTMLNode."""
        test_cases = [
            (self.text_node, None, "This is a text node"),  # Plain text, no tag
            (self.bold_node, "b", "Bold text example"),    # Bold text with <b>
            (self.italic_node, "i", "Italic text example"),  # Italic text with <i>
            (self.link_node, "a", "Link text example"),    # Link with <a>
            (self.image_node, "img", ""),                 # Image with <img>, empty value
        ]

        for node, expected_tag, expected_value in test_cases:
            with self.subTest(node=node):
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, expected_tag)
                self.assertEqual(html_node.value, expected_value)

                if expected_tag == "a":  # LINK type expects an href property
                    self.assertEqual(html_node.props["href"], self.example_url)
                elif expected_tag == "img":  # IMAGE type expects src and alt properties
                    self.assertEqual(html_node.props["src"], self.example_image_url)
                    self.assertEqual(html_node.props["alt"], "Image example")

if __name__ == "__main__":
    unittest.main()

