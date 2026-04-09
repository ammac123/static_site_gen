import os
import shutil
import sys
from copystatic import copy_directory_src_to_dest
from generatepage import generate_page_recursive

basepath = sys.argv[1] or "/"
dir_path_static = "static"
dir_path_public = "docs"
dir_path_content = "content"
template_path = "template.html"

def main():
    print(basepath)
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_directory_src_to_dest(".", dir_path_static, dir_path_public)
    generate_page_recursive(dir_path_content, template_path, dir_path_public, basepath)

if __name__=="__main__":
    main()