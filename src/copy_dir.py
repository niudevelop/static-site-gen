import os
import shutil


def copy_dir(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"copied: {src_path} -> {dst_path}")
        else:
            copy_dir(src_path, dst_path)
