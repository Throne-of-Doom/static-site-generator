import unittest
from markdown_extractor import extract_markdown_images, extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], matches)
    
    def test_no_markdown_images(self):
        matches = extract_markdown_images("This text has no images")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev)"
    )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_markdown_links(self):
            matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
            self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)
    
    def test_no_markdown_links(self):
        matches = extract_markdown_links("This text has no links")
        self.assertListEqual([], matches)
    
    def test_links_not_images(self):
        # Make sure image links aren't being captured by the link function
        matches = extract_markdown_links(
            "This has an ![image](https://example.com/img.jpg) but not a regular link"
        )
        self.assertListEqual([], matches)
    
    def test_images_not_links(self):
        # Make sure regular links aren't being captured by the image function
        matches = extract_markdown_images(
            "This has a [link](https://example.com) but not an image"
        )
        self.assertListEqual([], matches)
    
    def test_mixed_content(self):
        # Test with both links and images
        text = "Here's a ![cat](https://example.com/cat.jpg) and a [dog site](https://dogs.com)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        self.assertListEqual([("cat", "https://example.com/cat.jpg")], image_matches)
        self.assertListEqual([("dog site", "https://dogs.com")], link_matches)

    def test_urls_with_query_parameters(self):
    # Test URLs with query strings and special characters
        matches = extract_markdown_links(
        "Check out [this search](https://www.google.com/search?q=python+regex&lang=en)"
    )
        self.assertListEqual([
        ("this search", "https://www.google.com/search?q=python+regex&lang=en")
    ], matches)

    def test_empty_text(self):
    # Test links/images with empty text
        img_matches = extract_markdown_images("Look at this: ![](https://example.com/img.jpg)")
        link_matches = extract_markdown_links("Click [](https://example.com)")
    
        self.assertListEqual([("", "https://example.com/img.jpg")], img_matches)
        self.assertListEqual([("", "https://example.com")], link_matches)

    def test_multiple_lines(self):
    # Test markdown spread across multiple lines
        text = """
        Here's a paragraph with a [link](https://example.com).
    
        And another paragraph with an ![image](https://example.com/img.jpg).
            """
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
    
        self.assertListEqual([("image", "https://example.com/img.jpg")], img_matches)
        self.assertListEqual([("link", "https://example.com")], link_matches)

    def test_urls_with_parentheses(self):
    # Test URLs containing parentheses
        matches = extract_markdown_links(
        "Wikipedia [article](https://en.wikipedia.org/wiki/Bracket_(disambiguation))"
    )
    # Note: This might fail depending on how your regex handles nested parentheses
        self.assertListEqual([
        ("article", "https://en.wikipedia.org/wiki/Bracket_(disambiguation)")
    ], matches)

    def test_consecutive_markdown(self):
    # Test markdown elements right next to each other
        text = "Back-to-back [link1](https://example1.com)[link2](https://example2.com) and ![img1](https://img1.com)![img2](https://img2.com)"
    
        link_matches = extract_markdown_links(text)
        img_matches = extract_markdown_images(text)
    
        self.assertListEqual([
        ("link1", "https://example1.com"),
        ("link2", "https://example2.com")
    ],  link_matches)
    
        self.assertListEqual([
        ("img1", "https://img1.com"),
        ("img2", "https://img2.com")
    ], img_matches)

    def test_malformed_markdown(self):
    # Test how the function handles malformed markdown
    # Missing closing brackets or parentheses
        text = "This is [malformed markdown](https://example.com and [this too](https://example2.com"
    
        matches = extract_markdown_links(text)
    # Depending on your regex, this might not find any matches or might find partial matches
    # The important thing is that it doesn't crash
        self.assertIsInstance(matches, list)

    def test_urls_with_markdown_characters(self):
    # Test URLs that contain characters used in markdown syntax
        text = "Check [this out](https://example.com/page[1]?key=value#section)"
    
        matches = extract_markdown_links(text)
    # Again, depending on your regex, this might be challenging
        self.assertListEqual([
        ("this out", "https://example.com/page[1]?key=value#section")
    ], matches)

    def test_unicode_characters(self):
    # Test with non-ASCII characters in link text and URLs
        text = "See [résumé examples](https://example.com/résumé) and ![émoji](https://example.com/😊.png)"
    
        link_matches = extract_markdown_links(text)
        img_matches = extract_markdown_images(text)
    
        self.assertListEqual([
        ("résumé examples", "https://example.com/résumé")
    ], link_matches)
    
        self.assertListEqual([
        ("émoji", "https://example.com/😊.png")
    ], img_matches)

    def test_distinguishing_images_from_links(self):
    # Test that the functions correctly distinguish between images and links
        text = "This is an ![image](https://example.com/img.jpg) and this is a [link](https://example.com)"
    
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
    
        self.assertListEqual([
        ("image", "https://example.com/img.jpg")
    ], img_matches)
    
        self.assertListEqual([
        ("link", "https://example.com")
    ], link_matches)

    def test_empty_input(self):
    # Test with empty string as input
        self.assertListEqual([], extract_markdown_links(""))
        self.assertListEqual([], extract_markdown_images(""))

if __name__ == "__main__":
    unittest.main()