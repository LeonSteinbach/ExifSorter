import os
import sys
import shutil


def merge(folder1, folder2):
    files1 = os.listdir(folder1)
    files2 = [f.lower() for f in os.listdir(folder2)]

    for f1 in files1:
        name = "".join(f1.split(".")[:-1])
        extension = f1.split(".")[-1]

        # Name collision
        file_num = 0
        new_name = f1
        while (f1 != new_name and new_name.lower() in files1) or new_name.lower() in files2:
            file_num += 1
            new_name = name + " (" + str(file_num) + ")." + extension
            print(new_name)
        
        # Rename and move
        os.rename(os.path.join(folder1, f1), os.path.join(folder1, new_name))
        try:
            shutil.move(os.path.join(folder1, new_name), folder2)
        except FileExistsError:
            print("ERROR: " + f1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge.py <folder> <folder>")
        sys.exit(1)

    folder1 = sys.argv[1]
    folder2 = sys.argv[2]

    if not os.path.isdir(folder1) or not os.path.isdir(folder2):
        print("Parameter not a folder!")
        sys.exit(1)

    merge(folder1, folder2)
