from textnode import TextNode, TextType, BlockType, block_to_block_type
from htmlnode import ParentNode, HTMLNode, LeafNode
from enum import Enum
from node_converters import paragraph_to_html_node, heading_to_html_node, code_to_html_node, unordered_list_to_html_node, ordered_list_to_html_node, quote_to_html_node, text_to_children
import re
from markdown_utils import inline_markdown_to_text_nodes, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, validate_markdown_delimiters

def split_nodes_image(old_nodes):
    """
    Split text nodes containing markdown images into separate nodes for text and images.
    """
    image_result = []

    for old_node in old_nodes:
        if not old_node.text:
            continue
            
        if old_node.text_type != TextType.TEXT:
            image_result.append(old_node)
            continue

        if "\\![" in old_node.text:
            image_result.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images:
            image_result.append(old_node)
            continue
        
        remaining_text = old_node.text
        
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            image_parts = remaining_text.split(image_markdown, 1)

            if image_parts[0]:
                image_result.append(TextNode(image_parts[0], TextType.TEXT))

            image_result.append(TextNode(image_alt, TextType.IMAGE, image_url))

            if len(image_parts) > 1:
                remaining_text = image_parts[1]
            else: 
                remaining_text = ""

        if remaining_text:
            image_result.append(TextNode(remaining_text, TextType.TEXT))

    return image_result

def split_nodes_link(old_nodes):
    """
    Split text nodes containing markdown links into separate nodes for text and links.
    """
    link_result = []

    for old_node in old_nodes:
        if not old_node.text:
            continue
            
        if old_node.text_type != TextType.TEXT:
            link_result.append(old_node)
            continue

        if "\\[" in old_node.text:
            link_result.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links:
            link_result.append(old_node)
            continue
        
        remaining_text = old_node.text
        
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            link_parts = remaining_text.split(link_markdown, 1)

            if link_parts[0]:
                link_result.append(TextNode(link_parts[0], TextType.TEXT))

            link_result.append(TextNode(link_text, TextType.LINK, link_url))

            if len(link_parts) > 1:
                remaining_text = link_parts[1]
            else: 
                remaining_text = ""

        if remaining_text:
            link_result.append(TextNode(remaining_text, TextType.TEXT))

    return link_result

def text_to_textnodes(text):
    """
    Convert a text string to a list of TextNode objects.
    """
    if text == "":
        return [TextNode("", TextType.TEXT)]
    
    if "****" in text:
        placeholder = "EMPTY_BOLD_PLACEHOLDER_12345"
        text = text.replace("****", placeholder)
        
        try:
            nodes = [TextNode(text, TextType.TEXT)]
            nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
            nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
            nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
            nodes = split_nodes_image(nodes)
            nodes = split_nodes_link(nodes)
            
            for node in nodes:
                node.text = node.text.replace(placeholder, "****")
            
            return nodes
        except Exception:
            return [TextNode(text.replace(placeholder, "****"), TextType.TEXT)]
    

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    if nodes and text.strip().endswith("**"):
        nodes.append(TextNode("", TextType.TEXT))

    return nodes

def markdown_to_blocks(markdown):
    # Run validation if needed
    validate_markdown(markdown)
    # Use the new block-splitting logic
    return split_blocks_by_type(markdown)

def markdown_to_html_node(markdown):
    """
    Convert a markdown document to an HTML node.
    """
    if not markdown.strip():
        return ParentNode("div", [])
    # Step 1: Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Step 2: Create a parent div to hold all block nodes
    children = []
    
    # Step 3: Process each block
    for block in blocks:
        block_type = block_type_identifier(block)

        if block_type in ["paragraph", "heading", "unordered_list", "ordered_list", "quote"]:
            validate_markdown_delimiters(block)
        
        # Add validation for malformed markdown
        if block_type not in ["paragraph", "heading", "code", "unordered_list", "ordered_list", "quote"]:
            raise ValueError(f"Invalid block type: {block_type}")
        
        # Create a node based on the block type
        if block_type == "paragraph":
            children.append(paragraph_to_html_node(block))
        elif block_type == "heading":
            children.append(heading_to_html_node(block))
        elif block_type == "code":
            children.append(code_to_html_node(block))
        elif block_type == "unordered_list":
            children.append(unordered_list_to_html_node(block))
        elif block_type == "ordered_list":
            children.append(ordered_list_to_html_node(block))
        elif block_type == "quote":
            children.append(quote_to_html_node(block))

    
    
    return ParentNode("div", children)

def create_paragraph_node(block):
    # Replace newlines with spaces to collapse them
    text = block.strip().replace("\n", " ")
    
    # Create children nodes from the text
    children = text_to_children(text)
    
    # Create paragraph node
    return ParentNode("p", children, {})

def create_heading_node(block):
    # Determine the heading level
    heading_level = 0
    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break
    
    # Process inline markdown in the heading text
    content = block[heading_level:].strip()
    children = text_to_children(content)
    return ParentNode(f"h{heading_level}", children, {})

def create_quote_node(block):
    # Process inline markdown in the quote text
    lines = block.split("\n")
    quote_content = "\n".join([line.lstrip("> ").strip() for line in lines if line.strip()])
    children = text_to_children(quote_content)
    return ParentNode("blockquote", children, {})

def create_unordered_list_node(items):
    print(f"CREATING UL NODE with items: {items}")
    list_items = []
    
    for item_text, child_lines in items:
        print(f"  Item text: {item_text}")
        print(f"  Child lines: {child_lines}")
        children_nodes = text_to_children(item_text)
        
        # Process any nested list items
        for nested_items, is_ordered in child_lines:
            print(f"    Nested items: {nested_items}")
            print(f"    Is ordered: {is_ordered}")
            if is_ordered:
                nested_list = create_ordered_list_node(nested_items)
            else:
                nested_list = create_unordered_list_node(nested_items)
            children_nodes.append(nested_list)
        
        list_items.append(ParentNode("li", children_nodes, {}))
    
    return ParentNode("ul", list_items, {})

def create_ordered_list_node(items):
    """
    Create an ordered list HTMLNode from a list of items.
    """
    list_items = []
    
    for item_text, child_lines in items:
        children_nodes = text_to_children(item_text)
        
        # Process any nested list items
        for nested_items, is_ordered in child_lines:
            if is_ordered:
                nested_list = create_ordered_list_node(nested_items)
            else:
                nested_list = create_unordered_list_node(nested_items)
            children_nodes.append(nested_list)
        
        list_items.append(ParentNode("li", children_nodes, {}))
    
    return ParentNode("ol", list_items, {})


def create_code_block_node(block):
    # Remove the triple backticks and any language identifier
    lines = block.strip().split("\n")
    # Skip the first and last lines with ``` and join the rest
    code_content = "\n".join(lines[1:-1])
    
    # Create a leaf node for the code content (no parsing of inline markdown)
    code_node = LeafNode(tag="code", value=code_content)
    
    # Wrap in pre tag as a parent node
    return ParentNode(tag="pre", children=[code_node])

def validate_markdown(markdown):
    """
    Validate the markdown text.
    """
    if not isinstance(markdown, str):
        raise ValueError("Markdown must be a string")
    # Allow empty markdown
    if markdown is None:
        raise ValueError("Markdown cannot be None")

def process_list_blocks(lines, start_index, current_indent=0):
    """Process a group of list items at the same indentation level"""
    result = []
    
    # Skip empty lines at the beginning
    while start_index < len(lines) and not lines[start_index].strip():
        start_index += 1
        
    if start_index >= len(lines):
        return [], start_index
        
    # Find minimum indentation of all non-empty lines
    non_empty_lines = [line for line in lines[start_index:] if line.strip()]
    if not non_empty_lines:
        return [], start_index
        
    min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
    
    i = start_index
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Calculate normalized indentation
        raw_indent = len(line) - len(line.lstrip())
        effective_indent = raw_indent - min_indent
        
        # If this line is at a lower indentation level than what we're processing, 
        # we've reached the end of this list
        if effective_indent < current_indent:
            break
            
        # If this is a list item at our current indentation level
        if effective_indent == current_indent and (line.lstrip().startswith("- ") or 
                                                  line.lstrip().startswith("* ") or
                                                  line.lstrip().startswith("+ ") or
                                                  re.match(r"\d+\.\s", line.lstrip())):
            # Extract item text (remove marker)
            if line.lstrip().startswith(("- ", "* ", "+ ")):
                item_text = line.lstrip()[2:]
            else:
                # For ordered lists, remove the number and dot
                item_text = re.sub(r"^\d+\.\s+", "", line.lstrip())
            
            # Check for nested lists
            j = i + 1
            nested_items = []
            
            # If next lines are more indented or empty, they might be part of this item
            if j < len(lines) and (not lines[j].strip() or 
                                  len(lines[j]) - len(lines[j].lstrip()) > raw_indent):
                # Process nested list items
                nested_items, j = process_list_blocks(lines, j, effective_indent + 1)
                i = j - 1  # Adjust i since we processed multiple lines
            
            # Create node for this item
            if item_text.strip():
                text_node = text_to_children(item_text.strip())
            else:
                text_node = []
                
            # Add nested list as a child if exists
            item_children = text_node
            if nested_items:
                item_children.extend(nested_items)
                
            # Create list item node
            list_item = ParentNode("li", item_children)
            result.append(list_item)
            
        else:
            # If this line is more indented, it's content for the previous item
            # This is handled in the nested list processing
            break
            
        i += 1
            
    return result, i

def process_quote_block(block):
    """
    Process a blockquote block by removing the outer '>' markers and handling nested content.
    """
    lines = block.split("\n")
    # Remove the leading '>' from each line in the block
    content = []
    for line in lines:
        if line.startswith("> "):
            content.append(line[2:])
        elif line.startswith(">"):
            content.append(line[1:])
        else:
            content.append(line)
    
    # Process the content into HTML nodes
    children = extract_quote_content("\n".join(content))
    return ParentNode("blockquote", children)

def create_blockquote_node(block):
    """
    Create a blockquote HTMLNode from a block.
    """
    lines = block.split("\n")
    nodes = []
    current_text = []
    
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(">>"):  # Nested blockquote
            if current_text:
                nodes.append(text_to_children(" ".join(current_text))[0])
                current_text = []
            
            nested_content = stripped[2:].lstrip()
            nested_node = ParentNode("blockquote", text_to_children(nested_content))
            nodes.append(nested_node)
        elif stripped.startswith(">"):  # Regular blockquote line
            content = stripped[1:].lstrip()
            current_text.append(content)
    
    if current_text:
        nodes.extend(text_to_children(" ".join(current_text)))
    
    return ParentNode("blockquote", nodes)

def extract_quote_content(content):
    """
    Extract nested blockquotes and process other content in a blockquote.
    Returns a list of HTML nodes.
    """
    if ">" not in content:
        # No nested quotes, just process as text
        return text_to_children(content)
    
    result = []
    lines = content.split("\n")
    regular_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith(">"):
            # Process any accumulated regular lines
            if regular_lines:
                result.extend(text_to_children("\n".join(regular_lines)))
                regular_lines = []
            
            # Collect all lines for this nested blockquote
            nested_lines = [line]
            i += 1
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                nested_lines.append(lines[i])
                i += 1
            
            # Process this nested blockquote
            nested_block = "\n".join(nested_lines)
            nested_node = process_quote_block(nested_block)
            result.append(nested_node)
        else:
            regular_lines.append(line)
            i += 1
    
    # Process any remaining regular lines
    if regular_lines:
        result.extend(text_to_children("\n".join(regular_lines)))
    
    return result


def is_new_block_type(line):
    """
    Determine if a line indicates the start of a new block type.
    """
    line = line.lstrip()
    return (
        line.startswith("#") or  # Heading
        line.startswith("- ") or line.startswith("* ") or  # Unordered list
        line.startswith(">") or  # Quote
        # Ordered list: starts with a digit followed by a period and a space
        (line and line[0].isdigit() and ". " in line[:4])
    )


def split_blocks_by_type(markdown):
    """
    Split markdown into blocks based on block types and empty lines.
    """
    lines = markdown.split("\n")
    blocks = []
    current_block = []
    in_code_block = False
    
    for line in lines:
        blocks, current_block, in_code_block = process_line_for_blocks(
            line, blocks, current_block, in_code_block
        )
    
    # Don't forget to add the last block if there is one
    if current_block:
        blocks.append("\n".join(current_block))
    
    return blocks
def process_line_for_blocks(line, blocks, current_block, in_code_block):
    """
    Process a single line and update blocks accordingly.
    Returns updated blocks, current_block, and in_code_block status.
    """
    # Handle code blocks as special case
    if line.strip().startswith("```"):
        if not in_code_block:  # Start of code block
            if current_block:  # Save any accumulated content
                blocks.append("\n".join(current_block))
                current_block = []
            current_block.append(line)
            in_code_block = True
        else:  # End of code block
            current_block.append(line)
            blocks.append("\n".join(current_block))
            current_block = []
            in_code_block = False
        return blocks, current_block, in_code_block

    # Inside a code block, just add the line to the current block
    if in_code_block:
        current_block.append(line)
        return blocks, current_block, in_code_block

    # Empty line indicates end of a block
    if not line.strip():
        if current_block:
            blocks.append("\n".join(current_block))
            current_block = []
        return blocks, current_block, in_code_block

    # Check if line starts a new block type when we already have content
    if current_block and is_new_block_type(line) and not current_block[-1].endswith("\\"):
        # Special case: if the previous line in current_block is empty, ignore this check
        # This prevents creating a new block for indented content following an empty line
        if len(current_block) > 0 and current_block[-1].strip():
            # Get current block type
            current_type = None
            first_line = current_block[0].lstrip()
            
            # Determine the type of the current block
            if first_line.startswith("#"):
                current_type = "heading"
            elif first_line.startswith("- ") or first_line.startswith("* "):
                current_type = "unordered_list"
            elif first_line.startswith(">"):
                current_type = "quote"
            elif first_line and first_line[0].isdigit() and ". " in first_line[:4]:
                current_type = "ordered_list"
            
            # Determine the type of the new line
            new_type = None
            if line.lstrip().startswith("#"):
                new_type = "heading"
            elif line.lstrip().startswith("- ") or line.lstrip().startswith("* "):
                new_type = "unordered_list"
            elif line.lstrip().startswith(">"):
                new_type = "quote"
            elif line.lstrip() and line.lstrip()[0].isdigit() and ". " in line.lstrip()[:4]:
                new_type = "ordered_list"
            
            # If the types are different, create a new block
            if new_type != current_type:
                blocks.append("\n".join(current_block))
                current_block = [line]
                return blocks, current_block, in_code_block
            # Add line to current block
    current_block.append(line)
    return blocks, current_block, in_code_block

def block_type_identifier(block):
    """
    Identify the type of a markdown block.
    """
    # Remove leading/trailing whitespace for better detection
    trimmed = block.strip()
    
    if not trimmed:
        return "empty"
    
    # Code blocks start and end with ```
    if trimmed.startswith("```") and "```" in trimmed[3:]:
        return "code"
    
    # Headings start with # (1-6 of them)
    if trimmed.startswith("#"):
        return "heading"
    
    # Unordered lists start with - or *
    if trimmed.startswith("- ") or trimmed.startswith("* "):
        return "unordered_list"
    
    # Ordered lists start with a number followed by a period
    if trimmed and trimmed[0].isdigit() and ". " in trimmed[:4]:
        return "ordered_list"
    
    # Quote blocks start with >
    if trimmed.startswith(">"):
        return "quote"
    
    # If none of the above, it's a paragraph
    return "paragraph"

