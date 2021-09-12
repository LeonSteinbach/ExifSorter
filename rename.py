import os
import re
import sys
import glob
import time
import shutil
import zipfile
import exifread
import subprocess
from time import strftime, localtime
from pymediainfo import MediaInfo


def rename_media_files():
    preview_folder = "preview_images\\"

    files = []
    extensions = ["*.png", "*.jpg", "*.nef", "*.gif", "*.bmp", "*.mp4", "*.mov", "*.wmv", "*.avi", "*.m2ts", "*.mts", "*.3gp"]
    for extension in extensions:
        files.extend(glob.glob(extension))

    if len(files) > 0:
        max_file_length = len(max(files, key=len))
    else:
        max_file_length = 0

    for i, name in enumerate(files):
        extension = "." + name.split(".")[-1]
        dates = []

        preview_size = False
        preview_image = False

        # Media information
        media_info = MediaInfo.parse(name)
        for track in media_info.tracks:
            data = track.to_data()
            if data["track_type"] == "General":
                dates.append(data["file_creation_date"].replace("UTC ", "").replace(" ", "_").replace("-", "").replace(":", "").split(".")[0])
                dates.append(data["file_creation_date__local"].replace("UTC ", "").replace(" ", "_").replace("-", "").replace(":", "").split(".")[0])
                dates.append(data["file_last_modification_date"].replace("UTC ", "").replace(" ", "_").replace("-", "").replace(":", "").split(".")[0])
                dates.append(data["file_last_modification_date__local"].replace("UTC ", "").replace(" ", "_").replace("-", "").replace(":", "").split(".")[0])
            if data["track_type"] == "Video":
                try:
                    dates.append(data["encoded_date"].replace("UTC ", "").replace(" ", "_").replace("-", "").replace(":", "").split(".")[0])
                    dates.append(data["tagged_date"].replace("UTC ", "").replace(" ", "_").replace("-", "").replace(":", "").split(".")[0])
                except:
                    pass

            # Check for preview images
            if data["track_type"] == "Image":
                if (data["width"] + data["height"] < 1000):
                    preview_size = True
        
        # File information
        try:
            ctime = strftime("%Y%m%d_%H%M%S", localtime(os.stat(name).st_ctime))
            atime = strftime("%Y%m%d_%H%M%S", localtime(os.stat(name).st_atime))
            mtime = strftime("%Y%m%d_%H%M%S", localtime(os.stat(name).st_mtime))

            dates.extend([ctime, atime, mtime])
        except:
            pass

        
        # Exifdata
        f = open(name, "rb")
        try:
            tags = exifread.process_file(f)
        except:
            print("\n=======================\n\n\nTAG ERROR\n\n\n=======================\n")
        if len(tags) > 0:
            try:
                date_time = str(tags["Image DateTime"])[:19].replace(":", "").replace(" ", "_")
                date_time_original = str(tags["EXIF DateTimeOriginal"])[:19].replace(":", "").replace(" ", "_")
                date_time_digitized = str(tags["EXIF DateTimeDigitized"])[:19].replace(":", "").replace(" ", "_")
                dates.extend([date_time, date_time_original, date_time_digitized])
            except:
                print("Error: No exifdata for the file " + str(name))
        else:
            if name.split(".")[-1] in ["png", "jpg", "nef"]:
                print("Error: No exifdata for the file " + str(name))
        f.close()
        

        if len(dates) == 0:
            print(name + "\t =>\t No dates found. File ignored!")
            continue

        file_number = 0
        rename = True
        while True:
            try:
                if file_number == 0:
                    new_name = str(min(dates)) + str(extension)
                else:
                    new_name = str(min(dates)) + " (" + str(file_number) + ")" + str(extension)
                #if new_name in name:
                #    rename = False
                #    break
                os.rename(name, new_name)
                break
            except FileExistsError:
                if preview_size or name.startswith("t"):
                    preview_image = True
                file_number += 1
            except KeyboardInterrupt:
                print("Paused!")
                input("Press any key to continue...")

        if preview_image:
            print("Move " + name + " to " + preview_folder + name)
            try:
                os.makedirs(preview_folder)
                print("Created preview_images folder!")
            except:
                pass
            shutil.move(new_name, preview_folder + new_name)

        if rename:
            print(name + " " * (max_file_length - len(name)) + " => " + new_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rename.py <folder>")
        sys.exit(1)
    folder = sys.argv[1]

    os.chdir(folder)

    rename_media_files()
