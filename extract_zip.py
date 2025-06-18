import os
import zipfile

# Paths
input_dir = "{your_path}/dcm_cmprs"
output_dir = "{your_path}/dcm_raw"
N = 1 #test for 1

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get list of zip files
zip_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.zip')])[:N]

# Extract each zip file
for zip_file in zip_files:
    zip_path = os.path.join(input_dir, zip_file)
    print(f"Extracting {zip_file}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

print("Done extracting.")
