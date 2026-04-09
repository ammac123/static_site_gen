import os
import shutil
from copystatic import copy_directory_src_to_dest
from generatepage import generate_page_recursive

dir_path_static = "static"
dir_path_public = "public"
dir_path_content = "content"
template_path = "template.html"

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_directory_src_to_dest(".", dir_path_static, dir_path_public)
    generate_page_recursive(dir_path_content, template_path, dir_path_public)

if __name__=="__main__":
    main()