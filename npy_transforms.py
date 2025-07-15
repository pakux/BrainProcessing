import os
import argparse
import torchio as tio
import numpy as np
import torch

#%%
def parse_args():
    parser = argparse.ArgumentParser(description="Preprocess NIfTI to .npy: Resample, Crop, Resize, Normalize")
    parser.add_argument('--img_size', type=int, default=96, help='Final output image size (default: 96)')
    parser.add_argument('--crop_size', type=int, default=180, help='Crop size before resizing (default: 180)')
    parser.add_argument('--cohort', type=str, required=True, help='Cohort name (e.g., ukb, ppmi)')
    parser.add_argument('--input_folder', type=str, default=None, help='Input folder with .nii.gz files')
    parser.add_argument('--output_folder', type=str, default=None, help='Output folder for .npy files')
    return parser.parse_args()

#%%
def transform_and_save_npy(nii_path, output_path, transforms):
    subject = tio.Subject(img=tio.ScalarImage(nii_path))
    subject = transforms(subject)
    data = subject.img.data.squeeze(0).numpy()  # Remove channel dimension
    np.save(output_path, data)

#%%
def process_nifti_files(root_dir, npy_folder, transforms):
    nii_files = [f for f in os.listdir(root_dir) if f.endswith('_deskulled.nii.gz')]
    for nii_file in nii_files:
        nii_path = os.path.join(root_dir, nii_file)
        npy_file = nii_file.replace('_deskulled.nii.gz', '') + '.npy'
        output_path = os.path.join(npy_folder, npy_file)

        if os.path.exists(output_path):
            print(f"Skipping {npy_file}, already exists.")
            continue

        transform_and_save_npy(nii_path, output_path, transforms)
        print(f"Saved: {output_path}")

#%%
if __name__ == "__main__":
    args = parse_args()

    input_folder = args.input_folder or f'../images/{args.cohort}/nifti_deskull/'
    output_folder = args.output_folder or f'../images/{args.cohort}/npy{args.img_size}/'
    os.makedirs(output_folder, exist_ok=True)

    # Full transform pipeline
    transforms = tio.Compose([
        tio.Resample((1, 1, 1)),  # Resample to 1mm isotropic
        tio.CropOrPad((args.crop_size, args.crop_size, args.crop_size)),  # Crop/Pad to 180³
        tio.Resize((args.img_size, args.img_size, args.img_size)),  # Downscale to 96³
        tio.ZNormalization()  # Normalize intensity
    ])

    # Process
    process_nifti_files(input_folder, output_folder, transforms)

    # Report
    npy_count = len([f for f in os.listdir(output_folder) if f.endswith('.npy')])
    print(f"Total .npy files in {output_folder}: {npy_count}")

