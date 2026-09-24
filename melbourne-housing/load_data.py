import kagglehub
import os
import shutil

# Download latest version of the dataset
path = kagglehub.dataset_download("dansbecker/melbourne-housing-snapshot")
print("Path to dataset files:", path, "\n")

# Define the source file path
src = os.path.join(path, "melb_data.csv")

# Get the absolute path of the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the destination path inside the script's folder
dst = os.path.join(script_dir, "data.csv")
CSV_DIR = dst

# Copy the file
shutil.copy(src, dst)
print(f"Copied {src} → {dst}\n")