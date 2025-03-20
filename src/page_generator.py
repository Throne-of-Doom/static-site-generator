from markdown_blocks import markdown_to_html_node
from markdown_blocks import extract_title
import os


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")
    page = read_file(from_path)
    template = read_file(template_path)
    html_node = markdown_to_html_node(page)
    html_content = html_node.to_html()
    title = extract_title(page)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    write_file(dest_path, template)

def read_file(path):
    with open(path, 'r') as file:
        content = file.read()
    return content

def write_file(path, content):
    with open(path, 'w') as file:
        file.write(content)