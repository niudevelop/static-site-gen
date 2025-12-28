import shutil
import os

from generator import generate_page, generate_pages_recursive
from copy_dir import copy_dir


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_dir("static", "public")

    # generate_page(
    #     "content/index.md",
    #     "template.html",
    #     "public/index.html",
    # )

    generate_pages_recursive(
        "content",
        "template.html",
        "public",
    )


main()
