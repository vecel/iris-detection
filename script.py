import os
import shutil
import re

import kagglehub

# Download latest version
path = kagglehub.dataset_download("naureenmohammad/mmu-iris-dataset")

print("Path to dataset files:", path)

# Base directory where the images are stored
base_dir = path + "/MMU-Iris-Database"
target_dir = "./data"  # Move files here

# Ensure target directory exists
os.makedirs(target_dir, exist_ok=True)

# Loop through each numbered folder
for number in os.listdir(base_dir):
    number_path = os.path.join(base_dir, number)
    if not os.path.isdir(number_path):
        continue  # Skip if it's not a directory

    # Loop through 'left' and 'right' folders
    for side in ["left", "right"]:
        side_path = os.path.join(number_path, side)
        if not os.path.isdir(side_path):
            continue  # Skip if the side folder doesn't exist

        # Rename and move files to the target directory
        for filename in os.listdir(side_path):
            old_path = os.path.join(side_path, filename)
            if os.path.isfile(old_path) and filename.endswith(".bmp"):
                match = re.search(r"(\d+)", filename)  # Extract number from filename
                if match:
                    name_number = match.group(1)
                    new_filename = f"person_{number}_{side}{name_number}.bmp"
                    new_path = os.path.join(target_dir, new_filename)
                    shutil.copy(old_path, new_path)  # Move file
                    # print(f"Moved: {old_path} -> {new_path}")

print("Renaming and moving complete!")
