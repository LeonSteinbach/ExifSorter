import os
import sys
import glob
import time
import shutil
import filecmp
import hashlib
from collections import defaultdict


extensions = ["png", "jpg", "nef", "gif", "bmp", "mp4", "mov", "wmv", "avi", "m2ts", "mts", "3gp"]


def delete_empty_folders(path, remove_root=True):
    if not os.path.isdir(path):
        return

    files = os.listdir(path)
    if len(files):
        for f in files:
          fullpath = os.path.join(path, f)
          if os.path.isdir(fullpath):
              delete_empty_folders(fullpath)

    files = os.listdir(path)
    if len(files) == 0 and "full_recovery" not in path and remove_root:
        print("Removing empty folder: " + path)
        os.rmdir(path)


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remove_duplicates(path):
    if not os.path.isdir(path):
        print("Specified directory does not exist!")
        return

    os.chdir(path)

    num_files = 0

    md5_dict = defaultdict(list)
    for root, dirs, files in os.walk(path):
        num_files = len(files)
        for i, filename in enumerate(files):
            filepath = os.path.join(root, filename)
            file_md5 = md5(filename)
            md5_dict[file_md5].append(filepath)
            print("\r[" + str(i) + "/" + str(num_files) + "]", end="")
    for key in md5_dict:
        file_list = md5_dict[key]
        while len(file_list) > 1:
            item = file_list.pop()
            print("\rRemove duplicate " + str(item), end="")
            os.remove(item)


def clean():
    base = os.getcwd()
    recovery = base + "\\full_recovery\\"

    # Create recovery folder
    try:
        os.makedirs(recovery)
        print("Created recovery folder!")
        time.sleep(1)
    except:
        pass

    # Move or delete all files
    print("Moving and deleting all files...")
    for root, dirs, files in os.walk("."):
        if "full_recovery" in root:
            continue
        for name in files:
            path = os.path.join(root, name)
            print(path, end="\t")
            if name.split(".")[-1].lower() in extensions and "preview_images" not in root:
                # Move to root folder
                print("move")
                new_path = os.path.join(recovery, name)
                try:
                    shutil.move(path, new_path)
                except:
                    print("Error while moving file " + str(path))
                    input("Press a key to continue...")
            else:
                # Delete
                print("delete")
                try:
                    os.remove(path)
                except:
                    print("Error while removing file " + str(path))
                    input("Press a key to continue...")
        
        # Delete empty root folder
        # delete_empty_folders(root, False)
    print("\nFinished moving and deleting files!\n")

    # Delete duplicates
    print("Deleting duplicates...")
    remove_duplicates(recovery)
    print("\nFinished deleting duplicates!\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean.py <folder>")
        sys.exit(1)

    folder = sys.argv[1]

    os.chdir(folder)

    clean()
