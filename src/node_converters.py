import htmlnode
import textnode
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_utils import inline_markdown_to_text_nodes, split_nodes_delimiter
import re

def check_attribute(text_node, attribute, text_type):
    """
    Check if the given attribute exists in the text_node and is not None.
    
    :param text_node: The TextNode instance to check.
    :param attribute: The attribute to check for.
    :param text_type: The type of the text for error message context.
    :raises ValueError: If the attribute is missing or None.
    """
    if not hasattr(text_node, attribute) or getattr(text_node, attribute) is None:
        raise ValueError(f"TextNode for {text_type} type must have a '{attribute}'")

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, {})
    elif text_node.text_type == TextType.BOLD:
        # Create a bold node
        children = []
        # Process the text inside for any nested formatting
        child_text_nodes = inline_markdown_to_text_nodes(text_node.text)
        # Convert each child to HTML and add it
        for child in child_text_nodes:
            children.append(text_node_to_html_node(child))
        return ParentNode("b", children, {})
    elif text_node.text_type == TextType.ITALIC:
        # Similar handling for italic
        children = []
        child_text_nodes = inline_markdown_to_text_nodes(text_node.text)
        for child in child_text_nodes:
            children.append(text_node_to_html_node(child))
        return ParentNode("i", children, {})
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text, {})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
    
def paragraph_to_html_node(block):
    """
    Convert a paragraph block to an HTMLNode.
    """
    text = block.strip()
    children = text_to_children(text)
    
    # Ensure children is never empty
    if not children:
        children = [TextNode("", TextType.TEXT)]
    
    return ParentNode("p", None, children)

def heading_to_html_node(block):
    """
    Convert a heading block to an HTMLNode.
    """
    text = block.strip()
    level = 0
    
    # Count the number of # at the beginning to determine heading level
    for char in text:
        if char == '#':
            level += 1
        else:
            break
    
    # Cap the level at 6 (h1-h6)
    level = min(level, 6)
    
    # Remove the heading markers and any leading/trailing spaces
    content = text[level:].strip()
    
    # Convert the content to child nodes
    children = text_to_children(content)
    
    # Ensure children is never empty
    if not children:
        children = [TextNode("", TextType.TEXT)]
    
    return ParentNode(f"h{level}", None, children)

def code_to_html_node(block):
    """
    Convert a code block to an HTMLNode.
    """
    # Remove the ``` at the beginning and end
    text = block.strip()
    if text.startswith("```") and text.endswith("```"):
        # Extract content between the first and last ```
        content = text[3:-3].strip()
    else:
        content = text
    
    # Create a text node without parsing markdown
    text_node = TextNode(content, TextType.TEXT)
    code_node = text_node_to_html_node(text_node)
    
    # Wrap in pre tag
    return ParentNode("pre", None, [code_node])

# In unordered_list_to_html_node
def unordered_list_to_html_node(block):
    # First, split the block into lines
    lines = block.strip().split("\n")
    
    # Parse the list items
    list_marker_pattern = r'^[-*]\s'
    list_items = parse_list_items(lines, list_marker_pattern)
    
    # Build the nested structure
    nested_items = build_nested_list(list_items)
    
    # Create list item nodes
    li_nodes = create_list_item_nodes(nested_items)
    
    # Return the ul parent node
    return ParentNode("ul", None, li_nodes)

def ordered_list_to_html_node(block):
    # First, split the block into lines
    lines = block.strip().split("\n")
    
    # Parse the list items with the pattern for ordered lists
    list_marker_pattern = r'^\d+\.\s'
    list_items = parse_list_items(lines, list_marker_pattern)
    
    # Build the nested structure
    nested_items = build_nested_list(list_items)
    
    # Create list item nodes
    li_nodes = create_list_item_nodes(nested_items)
    
    # Return the ol parent node
    return ParentNode("ol", None, li_nodes)

def create_list_item_nodes(nested_items):
    """Convert nested item dictionaries into HTMLNode objects."""
    li_nodes = []
    
    for item in nested_items:
        # Create children nodes from the content
        content_children = text_to_children(item["content"])
        
        # If this item has children, create a nested list node
        if item["children"]:
            if item["type"] == "ul":
                nested_list = ParentNode("ul", None, create_list_item_nodes(item["children"]))
            else:  # ol
                nested_list = ParentNode("ol", None, create_list_item_nodes(item["children"]))
            content_children.append(nested_list)
        
        # Ensure content_children is never empty
        if not content_children:
            content_children = [TextNode("", TextType.TEXT)]
        
        # Create the li node with its content and any nested list
        li_node = ParentNode("li", None, content_children)
        li_nodes.append(li_node)
    
    return li_nodes

def quote_to_html_node(block):
    """
    Convert a quote block to an HTMLNode.
    """
    lines = block.strip().split("\n")
    quote_content = []
    
    for line in lines:
        # Remove the > and trim
        if line.strip().startswith(">"):
            content = line.strip()[1:].strip()
        else:
            content = line.strip()
        
        quote_content.append(content)
    
    # Join all lines and convert content to HTML nodes
    full_content = " ".join(quote_content)
    children = text_to_children(full_content)
    
    # Ensure children is never empty
    if not children:
        children = [TextNode("", TextType.TEXT)]
    
    # Create the blockquote node
    return ParentNode("blockquote", None, children)

def text_to_children(text):
    """Convert text with inline elements to a list of HTML nodes"""
    # First, find all delimited sections (code, bold, italic)
    nodes = []
    
    # Use regex to identify all the marked up sections
    # This finds all the bold, italic, and code sections
    pattern = r'(\*\*.*?\*\*)|(`.*?`)|(_.*?_)'
    
    # Split text by matches
    segments = []
    last_end = 0
    
    for match in re.finditer(pattern, text):
        start, end = match.span()
        
        # Add text before this match
        if start > last_end:
            segments.append(("text", text[last_end:start]))
        
        # Add the matched text with its type
        match_text = match.group()
        if match_text.startswith("**") and match_text.endswith("**"):
            # Handle nested formatting inside bold
            inner_text = match_text[2:-2]  # Remove ** markers
            inner_nodes = text_to_children(inner_text)  # Process what's inside recursively
            segments.append(("bold", inner_nodes))
        elif match_text.startswith("`") and match_text.endswith("`"):
            segments.append(("code", match_text[1:-1]))  # Remove ` markers
        elif match_text.startswith("_") and match_text.endswith("_"):
            # Handle nested formatting inside italic
            inner_text = match_text[1:-1]  # Remove _ markers
            inner_nodes = text_to_children(inner_text)  # Process what's inside recursively
            segments.append(("italic", inner_nodes))
        
        last_end = end
    
    # Add any remaining text
    if last_end < len(text):
        segments.append(("text", text[last_end:]))
    
    # Convert segments to HTML nodes
    for seg_type, content in segments:
        if seg_type == "text":
            if content.strip():  # Only add non-empty text
                nodes.append(TextNode(content, TextType.TEXT))
        elif seg_type == "bold":
            # If content is already a list of nodes (from recursive processing)
            if isinstance(content, list):
                nodes.append(ParentNode("b", content))
            else:
                nodes.append(ParentNode("b", [TextNode(content, TextType.BOLD)]))
        elif seg_type == "italic":
            # If content is already a list of nodes (from recursive processing)
            if isinstance(content, list):
                nodes.append(ParentNode("i", content))
            else:
                nodes.append(ParentNode("i", [TextNode(content, TextType.ITALIC)]))
        elif seg_type == "code":
            nodes.append(ParentNode("code", [TextNode(content, TextType.CODE)]))
    
    return nodes

def create_list_node(block):
    """
    Create a list node from either a markdown string or a list of already parsed items
    """
    # If block is already a list of items, process it directly
    if isinstance(block, list):
        # Determine list type from the first item (assuming all items are of same type)
        if block and isinstance(block[0], dict) and "ordered" in block[0]:
            list_type = "ol" if block[0]["ordered"] else "ul"
        else:
            # Default to unordered list if can't determine
            list_type = "ul"
        
        # Since items are already parsed and nested, create list item nodes directly
        list_items = create_list_item_nodes(block)
        return ParentNode(list_type, None, list_items)
    
    # Original code for handling string blocks:
    # Determine list type from the first item
    list_type = None
    if "- " in block or "* " in block:  # Unordered list
        list_type = "ul"
        pattern = r'[-*]\s'
    else:  # Ordered list
        list_type = "ol"
        pattern = r'\d+\.\s'
    
    # Split into lines and parse items
    lines = block.split("\n")
    parsed_items = parse_list_items(lines, pattern)
    
    # Build the nested structure
    nested_items = build_nested_list(parsed_items)
    
    # Create and return the list node
    list_items = create_list_item_nodes(nested_items)
    return ParentNode(list_type, list_items)
    
    # Commented out for now
    # def create_html_nodes(items, parent_type):
    #     if not items:
    #         return None
        
    #     list_node = HTMLNode(parent_type)
        
    #     for item in items:
    #         # Create a new list item node
    #         li_node = HTMLNode("li")
            
    #         # Add text content to the list item
    #         if item["content"]:
    #             # Convert the text content to child nodes (for inline markdown)
    #             text_children = text_to_children(item["content"])
    #             li_node.children.extend(text_children)
            
    #         # Process any nested lists
    #         if item["children"]:
    #             # Determine the type of the nested list
    #             nested_type = item["children"][0]["type"]
    #             nested_list = create_html_nodes(item["children"], nested_type)
                
    #             if nested_list:
    #                 li_node.children.append(nested_list)
            
    #         list_node.children.append(li_node)
        
    #     return list_node
    
    # The root level list type is determined at the beginning
    # return create_html_nodes(nested_items, list_type)

def parse_list_items(lines, list_marker_pattern):
    parsed_items = []
    
    # Find the base indentation level (of the first list item)
    base_indent = None
    for line in lines:
        if not line.strip():
            continue
        match = re.match(r'^\s*' + list_marker_pattern, line)
        if match:
            base_indent = len(line) - len(line.lstrip())
            break
    
    if base_indent is None:
        return []
    
    # Process all lines using the base indentation as reference
    for line in lines:
        if not line.strip():
            continue
            
        # Get absolute indentation
        abs_indent = len(line) - len(line.lstrip())
        stripped_line = line.lstrip()
        
        match = re.match(list_marker_pattern, stripped_line)
        if match:
            # Calculate relative indentation level - multiples of 4 spaces typically
            rel_indent = (abs_indent - base_indent) // 4
            
            # Extract the content after the list marker
            content = stripped_line[match.end():].strip()
            
            # Determine list type
            list_type = "ul" if re.match(r'^[-*]\s', stripped_line) else "ol"
            
            parsed_items.append({
                "indent": rel_indent,
                "content": content,
                "children": [],
                "type": list_type
            })
    
    print(f"Parsed list items: {parsed_items}")  # Debugging information
    return parsed_items

def build_nested_list(items):
    if not items:
        return []
        
    root = []
    stack = [(None, root)]  # (indent_level, children_list)
    
    for item in items:
        # Pop from stack until we find the parent level
        while len(stack) > 1 and stack[-1][0] >= item["indent"]:
            stack.pop()
            
        parent_list = stack[-1][1]
        
        # Create a copy of the item without modifying the original
        current_item = item.copy()
        
        # Add the current item to its parent's children
        parent_list.append(current_item)
        
        # If this item might have children, add it to the stack
        stack.append((item["indent"], current_item["children"]))
    
    print(f"Built nested list: {root}")  # Debugging information
    return root