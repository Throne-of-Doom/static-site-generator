from enum import Enum
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
import re

def create_parent_node(tag, children, props=None):
    # If children list is empty, add a default empty text node
    if not children:
        children = [LeafNode("span", "", None)]
    return ParentNode(tag, children, props)

def inline_markdown_to_text_nodes(text, depth=0):
    validate_markdown_delimiters(text)
    # Guard clause to prevent runaway recursion
    if depth > 10:
        raise RecursionError("Too deep, recursion likely caused by bad input")

    # Start with a single text node
    text_nodes = [TextNode(text, TextType.TEXT)]
    
    # Process each delimiter in sequence
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "__", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)

    all_nodes = []  # Collection for processed nodes

    for node in text_nodes:
        # Keep CODE nodes as is (they should be literal)
        if node.text_type == TextType.CODE:
            all_nodes.append(node)
        # Check all other node types (including TEXT, BOLD, ITALIC) for nested delimiters 
        elif any(delim in node.text for delim in ["**", "__", "*", "_", "`"]):
            # Process nested delimiters, but keep track of the current node's type
            current_type = node.text_type
            nested_nodes = inline_markdown_to_text_nodes(node.text, depth + 1)
            
            # For non-TEXT nodes, we need to preserve the original formatting
            if current_type != TextType.TEXT:
                # Create a new node with the original type but processed content
                formatted_text = "".join(n.text for n in nested_nodes)
                all_nodes.append(TextNode(formatted_text, current_type))
            else:
                # For TEXT nodes, just add all the nested nodes
                all_nodes.extend(nested_nodes)
        else:
            # No more delimiters to process
            all_nodes.append(node)

    return all_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes based on a given delimiter and assign a new text type to the delimited content.
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Don't process nodes that aren't TEXT type - preserve their existing formatting
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        text = old_node.text
        start_index = text.find(delimiter)
        
        if start_index == -1:
            new_nodes.append(old_node)
            continue
            
        end_index = text.find(delimiter, start_index + len(delimiter))
        if end_index == -1:
            new_nodes.append(old_node)  # Keep the node as-is if no closing delimiter
            continue
        
        before_text = text[:start_index]
        content_text = text[start_index + len(delimiter):end_index]
        after_text = text[end_index + len(delimiter):]
        
        if before_text:
            new_nodes.append(TextNode(before_text, TextType.TEXT))
        
        # Create the formatted node with the correct text type
        formatted_node = TextNode(content_text, text_type)
        new_nodes.append(formatted_node)
        
        if after_text:
            # Continue processing the rest of the text for more instances of this delimiter
            after_node = TextNode(after_text, TextType.TEXT)
            result_nodes = split_nodes_delimiter([after_node], delimiter, text_type)
            new_nodes.extend(result_nodes)
    
    return new_nodes



def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    image_matches = re.findall(image_pattern, text)

    image_result = []
    for image_match in image_matches:
        images = (image_match[0], image_match[1])
        image_result.append(images)
    
    return image_result
    
def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(((?:[^\(\)]|\([^\(\)]*\))*)\)"
    link_matches = re.findall(link_pattern, text)

    link_result = []
    for link_match in link_matches:
        links = (link_match[0], link_match[1])
        link_result.append(links)

    return link_result

def validate_markdown_delimiters(text):
    """
    Validates that all markdown delimiters are properly paired.
    Raises ValueError if any delimiter is unmatched.
    """
    if text.count("**") % 2 != 0:
        raise ValueError("Unmatched bold delimiter '**'")
    if text.count("__") % 2 != 0:
        raise ValueError("Unmatched bold delimiter '__'")
    if text.count("*") % 2 != 0:
        raise ValueError("Unmatched italic delimiter '*'")
    if text.count("_") % 2 != 0:
        raise ValueError("Unmatched italic delimiter '_'")
    if text.count("`") % 2 != 0:
        raise ValueError("Unmatched code delimiter '`'")
