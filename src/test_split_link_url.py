import unittest
from textnode import TextNode, TextType
from split_markdown import split_nodes_image, split_nodes_link

class TestMarkdownParser(unittest.TestCase):
    def test_split_images(self):
        """Test splitting text with multiple images."""
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
    
    def test_split_links(self):
        """Test splitting text with multiple links."""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        """Test splitting text with no images."""
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_links_no_links(self):
        """Test splitting text with no links."""
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_images_with_non_text_node(self):
        """Test splitting a non-text node (image)."""
        node = TextNode("image", TextType.IMAGE, "https://example.com/image.png")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_links_with_non_text_node(self):
        """Test splitting a non-text node (link)."""
        node = TextNode("link", TextType.LINK, "https://example.com")
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_images_multiple_nodes(self):
        """Test splitting multiple nodes with images."""
        node1 = TextNode("Text with ![image](https://example.com/image.png)", TextType.TEXT)
        node2 = TextNode("Just text", TextType.TEXT)
        node3 = TextNode("Another ![picture](https://example.com/pic.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode("Just text", TextType.TEXT),
                TextNode("Another ", TextType.TEXT),
                TextNode("picture", TextType.IMAGE, "https://example.com/pic.jpg"),
            ],
            new_nodes,
        )
        
    def test_split_links_multiple_nodes(self):
        """Test splitting multiple nodes with links."""
        node1 = TextNode("Text with [link](https://example.com)", TextType.TEXT)
        node2 = TextNode("Just text", TextType.TEXT)
        node3 = TextNode("Another [reference](https://example.org)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("Just text", TextType.TEXT),
                TextNode("Another ", TextType.TEXT),
                TextNode("reference", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )
        
    def test_split_images_at_beginning(self):
        """Test splitting text with an image at the beginning."""
        node = TextNode("![image](https://example.com/image.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_links_at_beginning(self):
        """Test splitting text with a link at the beginning."""
        node = TextNode("[link](https://example.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_images_at_end(self):
        """Test splitting text with an image at the end."""
        node = TextNode("Text followed by ![image](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            ],
            new_nodes,
        )
        
    def test_split_links_at_end(self):
        """Test splitting text with a link at the end."""
        node = TextNode("Text followed by [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        """Test splitting text with consecutive images."""
        node = TextNode(
            "Text with ![image1](https://example.com/image1.png)![image2](https://example.com/image2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://example.com/image1.png"),
                TextNode("image2", TextType.IMAGE, "https://example.com/image2.png"),
            ],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        """Test splitting text with consecutive links."""
        node = TextNode(
            "Text with [link1](https://example1.com)[link2](https://example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example1.com"),
                TextNode("link2", TextType.LINK, "https://example2.com"),
            ],
            new_nodes,
        )

    def test_split_images_empty_text(self):
        """Test splitting an empty text node."""
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)  # Empty text nodes should not be included

    def test_split_links_malformed(self):
        """Test splitting text with a malformed link."""
        # Missing closing parenthesis
        node = TextNode("Text with [link](https://example.com", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)  # Should remain unchanged if extraction fails

    def test_split_images_empty_alt_text(self):
        """Test splitting text with an image having empty alt text."""
        node = TextNode("Text with ![](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_links_empty_link_text(self):
        """Test splitting text with a link having empty link text."""
        node = TextNode("Text with [](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_images_multiple_in_single_node(self):
        """Test splitting text with multiple images in a single node."""
        node = TextNode(
            "![img1](https://example.com/1.png) text ![img2](https://example.com/2.png) more text ![img3](https://example.com/3.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" text ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://example.com/2.png"),
                TextNode(" more text ", TextType.TEXT),
                TextNode("img3", TextType.IMAGE, "https://example.com/3.png"),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        """Test splitting text with only an image."""
        node = TextNode("![solo image](https://example.com/solo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("solo image", TextType.IMAGE, "https://example.com/solo.png"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        """Test splitting text with only a link."""
        node = TextNode("[solo link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("solo link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_images_escaped_markdown(self):
        """Test splitting text with escaped markdown for images."""
        # Testing escaped markdown (should be ignored)
        node = TextNode("This contains \\![not an image](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_escaped_markdown(self):
        """Test splitting text with escaped markdown for links."""
        # Testing escaped markdown (should be ignored)
        node = TextNode("This contains \\[not a link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

if __name__ == '__main__':
    unittest.main()