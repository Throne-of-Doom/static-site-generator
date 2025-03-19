from textnode import TextNode, TextType

def main():
    """
    Main function to create a TextNode and print it.
    """
    try:
        text_node = TextNode("Hello World", TextType.TEXT)
        print(text_node)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()