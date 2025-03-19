from enum import Enum
from typing import Optional

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        """
        Initialize a TextNode instance.

        :param text: The text content.
        :param text_type: The type of the text.
        :param url: The URL associated with the text, if any.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        """
        Check if two TextNode instances are equal.

        :param other: The other TextNode instance to compare with.
        :return: True if the instances are equal, False otherwise.
        """
        if not isinstance(other, TextNode):
            return False
        return (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url)

    def __repr__(self) -> str:
        """
        Return a string representation of the TextNode instance.

        :return: A string representation of the TextNode instance.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def to_html(self):
        if self.text_type == TextType.BOLD:
            return f"<b>{self.text}</b>"
        elif self.text_type == TextType.ITALIC:
            return f"<i>{self.text}</i>"
        elif self.text_type == TextType.CODE:
            return f"<code>{self.text}</code>"
        elif self.text_type == TextType.LINK:
            return f'<a href="{self.url}">{self.text}</a>'
        elif self.text_type == TextType.IMAGE:
            return f'<img src="{self.url}" alt="{self.text}" />'
        else:
            return self.text

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(markdown: str) -> BlockType:
    """
    Determine the block type of a given markdown string.

    :param markdown: The markdown string to analyze.
    :return: The BlockType corresponding to the markdown string.
    """
    if not markdown:
        return BlockType.paragraph
    
    if is_blockquote(markdown):
        return BlockType.quote
    
    # Check if the markdown is a heading
    if markdown.startswith("#"):
        heading_level = 0
        for char in markdown:
            if char == "#":
                heading_level += 1
            else:
                break
        if 1 <= heading_level <= 6 and markdown[heading_level] == " ":
            return BlockType.heading
    
    # Check if the markdown is a code block
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.code
    
    # Check if the markdown is a quote
    elif markdown.startswith(">"):
        lines = markdown.split("\n")
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.quote
    
    # Check if the markdown is an unordered list
    elif markdown.lstrip().startswith("- "):  # Allow indentation
        lines = markdown.split("\n")
        for line in lines:
            if line.strip() and not line.strip().startswith("- "):
                return BlockType.paragraph
        non_empty_lines = [i for i, line in enumerate(lines) if line.strip()]
        if non_empty_lines:
            for i in range(non_empty_lines[0], non_empty_lines[-1]):
                if i not in non_empty_lines and i < len(lines):
                    return BlockType.paragraph
        return BlockType.unordered_list
    
    # Check if the markdown is an ordered list
    elif markdown[0].isdigit() and "." in markdown:
        lines = markdown.split("\n")
        # Check if first line starts with 1 (more flexible parsing)
        first_line = lines[0].strip()
        if not (first_line.startswith("1.") and len(first_line) > 2 and first_line[2] == " "):
            return BlockType.paragraph
        
        expected_number = 1
        for line in lines:
            if not line.strip():
                continue
            if line.strip() == "...":
                # When we encounter ellipsis, look ahead to find the next number
                next_lines = [l for l in lines[lines.index(line)+1:] if l.strip() and l.strip() != "..."]
                if next_lines:
                    next_line = next_lines[0].strip()
                    if next_line[0].isdigit():
                        try:
                            parts = next_line.split(".", 1)
                            if len(parts) == 2 and parts[1].startswith(" "):
                                expected_number = int(parts[0])
                        except ValueError:
                            pass
                continue

            line_stripped = line.strip()
            if line_stripped and line_stripped[0].isdigit():
                parts = line_stripped.split(".", 1)
                if len(parts) != 2:
                    return BlockType.paragraph
                if not parts[1].startswith(" ") or parts[1].startswith("  "):
                    return BlockType.paragraph
                try:
                    num = int(parts[0])
                    if num != expected_number:
                        return BlockType.paragraph
                    expected_number += 1
                except ValueError:
                    return BlockType.paragraph
    
        return BlockType.ordered_list
    
    return BlockType.paragraph


def is_blockquote(block: str) -> bool:
    """
    Determine if a block is a blockquote.
    A block is considered a blockquote if it starts with '>'
    
    Args:
        block: The markdown block to check
        
    Returns:
        True if the block is a blockquote, False otherwise
    """
    # Trim leading whitespace and check if it starts with '>'
    return block.lstrip().startswith(">")