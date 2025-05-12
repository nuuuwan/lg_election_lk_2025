import os
from utils import Log, File, Hash, JSONFile
import shutil
import random

log = Log("hexmaps")


def clean_and_copy():
    dir_root = os.path.join("workflows", "analysis", "hexmaps")
    for dirpath, dirnames, filenames in os.walk(dir_root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if filename.endswith(".py"):
                continue
            if filename.endswith(".hash.json"):
                continue
            if filename.startswith("hexbin-") and filename.endswith(".png"):
                image_path = os.path.join("images", filename)
                shutil.move(file_path, image_path)
                log.info(f'Moved "{file_path}" to images')
                os.startfile(image_path)
                continue
            os.remove(file_path)
            log.warning(f'Removed "{file_path}"')

        for dirname in dirnames:
            dir_path = os.path.join(dirpath, dirname)
            if dirname == "__pycache__":
                shutil.rmtree(dir_path)
                log.warning(f'Removed "{dir_path}"')


def run_single(file_path):
    content = File(file_path).read()
    VERSION = "v2"
    md5 = Hash.md5(content + VERSION)

    hash_json_file_path = file_path[:-3] + ".hash.json"
    hash_json_file = JSONFile(hash_json_file_path)
    current_md5 = None
    if os.path.exists(hash_json_file_path):
        data = hash_json_file.read()
        current_md5 = data["md5"]

    if current_md5 == md5:
        log.info(f"Not running {file_path}")
        return

    cmd = f"python {file_path}"
    print("-" * 60)
    log.info(f"{cmd}")
    os.system(cmd)
    print("-" * 60)

    hash_json_file.write(dict(md5=md5))

    clean_and_copy()


def run():
    dir_root = os.path.join("workflows", "analysis", "hexmaps")
    exe_path_list = []
    for dirpath, dirnames, filenames in os.walk(dir_root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if filename == "__main__.py" and dirpath != dir_root:
                exe_path_list.append(file_path)

    log.info(f"Found {len(exe_path_list)} builders.")
    random.shuffle(exe_path_list)

    for file_path in exe_path_list:
        run_single(file_path)


def main():

    run()
    clean_and_copy()


if __name__ == "__main__":
    main()
