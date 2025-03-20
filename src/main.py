from textnode import TextNode, TextType
import os
import shutil
from page_generator import generate_page
import sys

def copy_static(source, destination):
    """
    Recursively copies files and directories from the source to the destination.

    Args:
        source (str): The source directory path.
        destination (str): The destination directory path.
    """
    items = os.listdir(source)
    for item in items:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            # Copy file from source to destination
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            # Create directory in destination and copy contents recursively
            print(f"Creating directory {destination_path}")
            os.mkdir(destination_path)
            copy_static(source_path, destination_path)

def generate_site_pages(content_dir, template_path, docs_dir, basepath):
    """
    Generates HTML pages for all Markdown files in the content directory.

    Args:
        content_dir (str): The directory containing Markdown files.
        template_path (str): The path to the template file.
        docs_dir (str): The directory to save the generated HTML files.
        basepath (str): The base path for URLs in the generated HTML.
    """
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, content_dir)
                if file == "index.md":
                    html_path = os.path.join(docs_dir, os.path.dirname(relative_path), "index.html")
                else:
                    html_path = os.path.join(docs_dir, relative_path.replace(".md", ".html"))
                generate_page(file_path, template_path, html_path, basepath)



def main():
    """
    Main function to set up the static site generator.
    It clears the docs directory if it exists and copies the static files to the docs directory.
    """
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    static_dir = "static"
    docs_dir = "docs"
    
    # Remove the docs directory if it exists
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    
    # Create a new docs directory
    os.mkdir(docs_dir)

    # Copy static files to the docs directory
    copy_static(static_dir, docs_dir)
    generate_site_pages("content", "template.html", docs_dir, basepath)
    

if __name__ == "__main__":
    # Entry point of the script
    main()


