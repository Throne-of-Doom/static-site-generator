import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_different_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_link_node(self):
        node = TextNode("This is a text node, but with a URL", TextType.LINK, "https://www.google.com")
        self.assertEqual(node.text, "This is a text node, but with a URL")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://www.google.com")

    def test_different_url(self):
        node1 = TextNode("Same text", TextType.LINK, "https://www.google.com")
        node2 = TextNode("Same text", TextType.LINK, "https://www.bing.com")
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()