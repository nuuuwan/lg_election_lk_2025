import os
from utils import Log
import shutil

log = Log("hexmaps")


def run():
    dir_root = os.path.join("workflows", "analysis", "hexmaps")
    for dirpath, dirnames, filenames in os.walk(dir_root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if filename == "__main__.py" and dirpath != dir_root:
                cmd = f"python {file_path}"
                print("-" * 60)
                log.info(f"{cmd}")
                os.system(cmd)
                print("-" * 60)


def clean_and_copy():
    dir_root = os.path.join("workflows", "analysis", "hexmaps")
    for dirpath, dirnames, filenames in os.walk(dir_root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            if filename.endswith(".py"):
                continue
            if filename.startswith("hexbin-") and filename.endswith(".png"):
                shutil.move(file_path, os.path.join("images", filename))
                log.info(f'Moved "{file_path}" to images')
                continue
            os.remove(file_path)
            log.warning(f'Removed "{file_path}"')

        for dirname in dirnames:
            dir_path = os.path.join(dirpath, dirname)
            if dirname == "__pycache__":
                shutil.rmtree(dir_path)
                log.warning(f'Removed "{dir_path}"')


def main():
    run()
    clean_and_copy()


if __name__ == "__main__":
    main()
