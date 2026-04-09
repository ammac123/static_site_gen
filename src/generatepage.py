import os
import shutil
from markdown_blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from "{from_path}" to "{dest_path}" using "{template_path}')
    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html_page = template.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", content)
    html_page = html_page.replace('href="/', f'href="{basepath}')
    html_page = html_page.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(html_page)

def generate_page_recursive(dir_path_content, template_path, dir_dest_path, basepath):
    os.makedirs(dir_dest_path, exist_ok=True)
    for item in os.listdir(dir_path_content):
        content_path: str = os.path.join(dir_path_content, item)
        dest_path: str = os.path.join(dir_dest_path, item)
        if os.path.isdir(content_path):
            generate_page_recursive(content_path, template_path, dest_path, basepath)
            continue
        if os.path.isfile(content_path) and content_path.endswith(".md"):
            dest_fp = dest_path.removesuffix(".md") + '.html'
            generate_page(content_path, template_path, dest_fp, basepath) # type: ignore
    return