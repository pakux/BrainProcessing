#%%
import os
import argparse
import torchio as tio
import numpy as np
import nibabel as nib
import torch 
import matplotlib.pyplot as plt

#%%
def parse_args():
    parser = argparse.ArgumentParser(description="Convert NIfTI to .npy with TorchIO preprocessing")
    parser.add_argument('--img_size', type=int, default=180, help='Image size for cropping/padding (default: 180)')
    parser.add_argument('--cohort', type=str, required=True, help='Cohort name (e.g., ukb, ppmi)')
    parser.add_argument('--input_folder', type=str, default=None, help='Path to input .nii.gz files')
    parser.add_argument('--output_folder', type=str, default=None, help='Path to save .npy files')
    return parser.parse_args()

#%%
def transform_and_save_npy(nii_path, output_path, crop, norm):
    img = nib.load(nii_path)
    data = img.get_fdata()
    tensor_data = torch.tensor(data).unsqueeze(0)
    crop_data = crop(tensor_data)
    norm_data = norm(crop_data).squeeze(0)
    np.save(output_path, norm_data)

#%%
def process_nifti_files(root_dir, npy_folder, crop, norm):
    file_names = []
    nii_files = [file for file in os.listdir(root_dir) if file.endswith('_deskulled.nii.gz')]

    for nii_file in nii_files:
        nii_path = os.path.join(root_dir, nii_file)
        npy_file = nii_file.replace("_deskulled.nii.gz", "") + '.npy'
        output_path = os.path.join(npy_folder, npy_file)

        if os.path.exists(output_path):
            print(f'Skipping {npy_file} as it exists')
            file_names.append(os.path.splitext(npy_file)[0])
            continue

        transform_and_save_npy(nii_path, output_path, crop, norm)
        print(output_path)
        file_names.append(os.path.splitext(npy_file)[0])

#%%
if __name__ == "__main__":
    args = parse_args()

    # Auto-define input/output folders if not explicitly passed
    input_folder = args.input_folder or f'{your_path}/images/nifti_deskull/'
    output_folder = args.output_folder or f'{your_path}/images/{args.cohort}/npy_{args.cohort}{args.img_size}/'
    
    os.makedirs(output_folder, exist_ok=True)

    # Define transforms
    crop = tio.CropOrPad((args.img_size, args.img_size, args.img_size))
    norm = tio.transforms.ZNormalization()

    # Process and save files
    process_nifti_files(input_folder, output_folder, crop, norm)

    # Count .npy files
    npy_count = len([f for f in os.listdir(output_folder) if f.endswith('.npy')])
    print(f"Total number of .npy files in {output_folder}: {npy_count}")
