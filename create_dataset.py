import kagglehub
import os
import shutil
import requests

# URL of the PDF file
url = "https://ncert.nic.in/textbook/pdf/lekl101.pdf"

# Download latest version
path = kagglehub.dataset_download("kapturovalexander/football-mini")

print("Path to dataset files:", path)

# Create dataset folder if it doesn't exist
dataset_folder = 'dataset'
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)
if not os.path.exists('database'):
    os.makedirs('database')

# Copy files to the dataset folder without subfolders
for item in os.listdir(path):
    s = os.path.join(path, item)
    d = os.path.join(dataset_folder, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)  # Copy directories
    else:
        shutil.copy2(s, d)  # Copy files

# Ensure the directory exists
os.makedirs(dataset_folder, exist_ok=True)

# Full path for the downloaded file
file_path = os.path.join(dataset_folder, "story.pdf")

# Download the PDF
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded PDF to {file_path}")
else:
    print("Failed to download the PDF.")