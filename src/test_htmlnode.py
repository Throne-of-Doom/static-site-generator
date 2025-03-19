import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_with_attributes(self):
        """Test props_to_html with multiple attributes."""
        node = HTMLNode(tag="a", props={"href": "https://www.example.com", "target": "_blank"})
        expected = ' href="https://www.example.com" target="_blank"'
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_props_to_html_without_attributes(self):
        """Test props_to_html with no attributes."""
        node = HTMLNode(props={})
        expected = ''  # No attributes, no output
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_props_to_html_with_one_attribute(self):
        """Test props_to_html with a single attribute."""
        node = HTMLNode(props={"id": "main"})
        expected = ' id="main"'
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_props_to_html_with_none(self):
        """Test props_to_html with no props provided."""
        node = HTMLNode()
        expected = ''
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_leaf_to_html_with_tag(self):
        """Test LeafNode to_html with a tag."""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_value_none(self):
        """Test LeafNode initialization with value=None raises ValueError."""
        with self.assertRaises(ValueError, msg="LeafNode must have a value"):
            node = LeafNode(tag="p", value=None, props={"class": "main"})

    def test_leaf_to_html_tag_none(self):
        """Test LeafNode to_html with tag=None."""
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_with_props(self):
        """Test LeafNode to_html with props."""
        node = LeafNode(tag="a", value="Click here", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_leaf_to_html_raw_text(self):
        """Test LeafNode to_html with raw text."""
        node = LeafNode(tag=None, value="Hello!")
        self.assertEqual(node.to_html(), "Hello!")

    def test_leafnode_no_children(self):
        """Test that LeafNode does not allow children."""
        with self.assertRaises(TypeError):
            node = LeafNode(tag="p", value="Hello", children=["child1"])

    def test_props_with_invalid_types(self):
        """Test props_to_html behavior with invalid props types."""
        node = HTMLNode(tag="div", props={42: "number", "class": None})
        result = node.props_to_html()
        self.assertEqual(result, ' 42="')

    def test_leaf_to_html_empty_tag_and_props(self):
        """Test LeafNode to_html with an empty tag and no props."""
        node = LeafNode(tag="", value="Hello!")
        self.assertEqual(node.to_html(), "<>Hello!</>")

    def test_props_to_html_with_special_characters(self):
        """Test props_to_html with keys/values having special characters."""
        node = HTMLNode(tag="div", props={"data-info": 'He said, "Hi!"'})
        expected = ' data-info="He said, "Hi!""'
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_props_to_html_with_many_props(self):
        """Test props_to_html with a large number of props."""
        props = {f"key{i}": f"value{i}" for i in range(100)}
        node = HTMLNode(tag="div", props=props)
        result = node.props_to_html()
        self.assertTrue(all(f'key{i}="value{i}"' in result for i in range(100)))

    def test_leaf_to_html_with_non_string_value(self):
        """Test LeafNode to_html with a non-string value."""
        with self.assertRaises(TypeError):
            node = LeafNode(tag="p", value=123)  # Integers aren't valid for value

    def test_leafnode_rejects_children_argument(self):
        """Test that LeafNode does not accept a 'children' argument."""
        with self.assertRaises(TypeError):
            node = LeafNode(tag="p", value="Invalid", children=["child1"])

    def test_props_with_empty_string_value(self):
        """Test props_to_html with props that have empty string values."""
        node = HTMLNode(tag="input", props={"placeholder": ""})
        expected = ' placeholder=""'  # Should render with an empty attribute tag
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_props_with_none_value(self):
        """Test props_to_html with props that have None values."""
        node = HTMLNode(tag="div", props={"class": "header", "id": None})
        expected = ' class="header"'  # "id" should be excluded
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_leaf_to_html_with_special_characters_in_value(self):
        """Test LeafNode to_html with special characters in the value."""
        node = LeafNode(tag="p", value="3 < 5 & 7 > 2")
        expected = "<p>3 < 5 & 7 > 2</p>"  # Ensure HTML-escaping
        result = node.to_html()
        self.assertEqual(result, expected)

    def test_props_with_special_characters_in_key_or_value(self):
        """Test props_to_html with special characters in keys or values."""
        node = HTMLNode(
            tag="a",
            props={"data-info": 'data "quoted"', "style": "width: 5 > 2"}
        )
        expected = ' data-info="data "quoted"" style="width: 5 > 2"'
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_leaf_to_html_with_self_closing_tag(self):
        """Test LeafNode to_html with self-closing tags."""
        node = LeafNode(tag="img", value="", props={"src": "image.png", "alt": "Sample"})
        expected = '<img src="image.png" alt="Sample" />'  # Self-closing tag formatting
        result = node.to_html()
        self.assertEqual(result, expected)


    def test_props_with_boolean_attribute(self):
        """Test props_to_html with a boolean attribute that has no explicit value."""
        # The `checked` attribute is a good example of this behavior
        node = HTMLNode(tag="input", props={"type": "checkbox", "checked": True})
        expected = ' type="checkbox" checked'  # Proper HTML should include `checked`
        result = node.props_to_html()
        self.assertEqual(result, expected)

        # If `checked` is False, it shouldn't appear in the output at all
        node = HTMLNode(tag="input", props={"type": "checkbox", "checked": False})
        expected = ' type="checkbox"'
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_props_with_nested_values(self):
        """Test props_to_html where props have nested dictionaries."""
        node = HTMLNode(tag="div", props={"data-meta": {"key": "value"}})
        # If unsupported, it should throw an error or warn the user
        with self.assertRaises(TypeError):
            node.props_to_html()

    def test_props_to_html_with_many_attributes(self):
        """Test props_to_html with a very large number of props."""
        large_props = {f"key{i}": f"value{i}" for i in range(1, 10_001)}  # 10,000 props
        node = HTMLNode(tag="div", props=large_props)
        result = node.props_to_html()
        for i in range(1, 10_001):
            self.assertIn(f'key{i}="value{i}"', result)  # Ensure all props are rendered

    def test_leaf_to_html_with_invalid_tag(self):
        """Test LeafNode with an invalid tag name."""
        with self.assertRaises(ValueError, msg="Invalid tag name provided"):
            node = LeafNode(tag="123invalid", value="Bad tag!")
            node.to_html()

    def test_leaf_to_html_illegal_characters_in_value(self):
        """Test LeafNode to_html with a value containing illegal HTML characters."""
        node = LeafNode(tag="p", value="<b>text</b> & <script>alert('Oops')</script>")
        # Expect HTML to be safely escaped
        expected = "<p><b>text</b> & <script>alert('Oops')</script></p>"
        result = node.to_html()
        self.assertEqual(result, expected)

    def test_to_html_with_children(self):
        """Test ParentNode to_html with children."""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """Test ParentNode to_html with grandchildren."""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parentnode_no_children(self):
        """Test that ParentNode does not allow no children."""
        with self.assertRaises(ValueError):
            node = ParentNode(tag="div", children=[])

    def test_parentnode_rejects_value_argument(self):
        """Test that ParentNode does not accept a 'value' argument."""
        with self.assertRaises(TypeError):
            node = ParentNode(tag="div", value="Invalid")
    
    def test_parentnode_has_no_tag(self):
        """Test that ParentNode does not allow no tag."""
        with self.assertRaises(ValueError):
            node = ParentNode(tag=None, children=[LeafNode("p", "Hello")])

    def test_parentnode_has_tag(self):
        """Test that ParentNode allows a tag."""
        node = ParentNode(tag="div", children=[LeafNode("p", "Hello")])
        self.assertEqual(node.tag, "div")

    def test_parentnode_has_children(self):
        """Test that ParentNode requires children."""
        node = ParentNode(tag="div", children=[LeafNode("p", "Hello")])
        self.assertEqual(len(node.children), 1)

    def test_parentnode_to_html_no_tag(self):
        """Test ParentNode to_html with no tag."""
        with self.assertRaises(ValueError):
            node = ParentNode(tag=None, children=[LeafNode("p", "Hello")])
            node.to_html()

    def test_parentnode_to_html_no_children(self):
        """Test ParentNode to_html with no children."""
        with self.assertRaises(ValueError):
            node = ParentNode(tag="div", children=[])
            node.to_html()

    def test_parentnode_to_html_with_props(self):
        """Test ParentNode to_html with props."""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "main"})
        self.assertEqual(parent_node.to_html(), '<div class="main"><span>child</span></div>')

def test_parentnode_with_multiple_children(self):
    """Test ParentNode with multiple children."""
    parent_node = ParentNode("div", [
        LeafNode("p", "Paragraph 1"),
        LeafNode("p", "Paragraph 2"),
        LeafNode("span", "Span text")
    ])
    self.assertEqual(
        parent_node.to_html(),
        "<div><p>Paragraph 1</p><p>Paragraph 2</p><span>Span text</span></div>"
    )

def test_parentnode_with_mixed_children(self):
    """Test ParentNode with a mix of LeafNode and ParentNode children."""
    parent_node = ParentNode("div", [
        LeafNode("p", "Paragraph"),
        ParentNode("section", [LeafNode("h1", "Heading")])
    ])
    self.assertEqual(
        parent_node.to_html(),
        "<div><p>Paragraph</p><section><h1>Heading</h1></section></div>"
    )

def test_parentnode_with_tagless_child(self):
    """Test ParentNode with a child that has no tag."""
    parent_node = ParentNode("div", [
        LeafNode(None, "Plain text")
    ])
    self.assertEqual(parent_node.to_html(), "<div>Plain text</div>")

def test_deeply_nested_structure(self):
    """Test with a deeply nested structure."""
    deepest = LeafNode("span", "Deep text")
    middle = ParentNode("article", [deepest])
    inner = ParentNode("section", [middle])
    outer = ParentNode("div", [inner])
    self.assertEqual(
        outer.to_html(),
        "<div><section><article><span>Deep text</span></article></section></div>"
    )

def test_parentnode_with_empty_string_props(self):
    """Test ParentNode with empty string property values."""
    node = ParentNode("div", [LeafNode("p", "Hello")], props={"data-test": ""})
    self.assertEqual(node.to_html(), '<div data-test=""><p>Hello</p></div>')

def test_parentnode_with_non_list_children(self):
    """Test ParentNode rejects non-list children."""
    with self.assertRaises(TypeError):
        ParentNode("div", "not a list")

def test_parentnode_with_prop_children(self):
    """Test ParentNode with children that have props."""
    parent_node = ParentNode("div", [
        LeafNode("p", "Normal paragraph"),
        LeafNode("p", "Styled paragraph", props={"class": "highlight"})
    ])
    self.assertEqual(
        parent_node.to_html(),
        '<div><p>Normal paragraph</p><p class="highlight">Styled paragraph</p></div>'
    )

def test_parentnode_with_boolean_props(self):
    """Test ParentNode with boolean properties (no value)."""
    node = ParentNode("div", [LeafNode("p", "Hello")], props={"hidden": True})
    self.assertEqual(node.to_html(), '<div hidden><p>Hello</p></div>')

def test_parentnode_with_numeric_props(self):
    """Test ParentNode with numeric property values."""
    node = ParentNode("div", [LeafNode("p", "Hello")], props={"data-index": 5})
    self.assertEqual(node.to_html(), '<div data-index="5"><p>Hello</p></div>')

def test_parentnode_children_modification(self):
    """Test that modifying children after creation affects to_html output."""
    child1 = LeafNode("p", "Original")
    parent = ParentNode("div", [child1])
    self.assertEqual(parent.to_html(), "<div><p>Original</p></div>")
    
    # Modify the children list
    parent.children.append(LeafNode("span", "Added"))
    self.assertEqual(parent.to_html(), "<div><p>Original</p><span>Added</span></div>")
    
if __name__ == "__main__":
    unittest.main()