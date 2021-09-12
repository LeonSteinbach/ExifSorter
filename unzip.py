import os
import re
import sys
import glob
import shutil
import zipfile
import subprocess


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
    if len(files) == 0 and remove_root:
        print("Removing empty folder: " + path)
        os.rmdir(path)


def extract_zip(zipfile, new_folder, unzipped_folder):
    cmd = [r"C:\Program Files\7-Zip\7z.exe", "e", zipfile, "-o" + new_folder, "-r", "-aos"]
    try:
        sp = subprocess.Popen(cmd)#, stdout=subprocess.PIPE)
        sp.wait(timeout=60)
    except:
        print("Error extracting the file " + zipfile)
        return
    
    os.remove(zipfile)
    for root, dirs, files in os.walk(new_folder):
        for filename in files:
            if re.search(r'\.zip$', filename):
                shutil.move(root + "\\" + filename, unzipped_folder + filename)

                new_full_path = unzipped_folder + filename.split(".zip")[0]
                extract_zip(unzipped_folder + filename, new_full_path, unzipped_folder)


def unzip_files(folder):
    unzipped_folder = os.getcwd() + "\\unzipped\\"
    
    files = []
    extensions = ["*.zip"]
    for extension in extensions:
        files.extend(glob.glob(extension))
    if len(files) == 0:
        return
    else:
        try:
            os.makedirs(unzipped_folder)
            print("Created unzipped folder!")
        except:
            pass

    for i, name in enumerate(files):
        full_path = os.getcwd() + "\\" + name
        new_full_path = unzipped_folder + name.split(".")[0]
        
        extract_zip(full_path, new_full_path, unzipped_folder)

    delete_empty_folders(unzipped_folder, False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unzip.py <folder>")
        sys.exit(1)
    folder = sys.argv[1]

    os.chdir(folder)
    
    unzip_files(folder)
