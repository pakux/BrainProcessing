#%%
import os
import subprocess
import pandas as pd
import ants
import multiprocessing as mp
import time

# Paths
cohort = xx
path = yy
input_folder = f'{path}/images/{cohort}/nifti_raw/'
reg_folder = f'{path}/images/{cohort}/nifti_reg/'
deskull_folder = f'{path}/images/{cohort}/nifti_deskull/'
csv_path = f'{path}/data/{cohort}/pd-cn.csv'
template_path = f"{path}/images/templates/mni_icbm152_nlin_asym_09c/mni_icbm152_tal_nlin_asym_09c.nii"
type_reg = 'Affine' #type of registration from ants

# Load fixed image
fixed = ants.image_read(template_path)

# Read CSV
df = pd.read_csv(csv_path, dtype={'eid': str})  #have patientID column named as eid 
eids = df['eid'].to_list()   

# Number of samples to process
N = 1000    #Modify to 3 to check first

#%%
# 
def register_images(input_dir, eid_list, output_dir, fixed):
    os.makedirs(output_dir, exist_ok=True)

    for eid in eid_list[:N]:
        # Find any file that starts with the eid and ends with .nii.gz
        matched_files = [f for f in os.listdir(input_dir) if f.startswith(eid + '_') and f.endswith('.nii.gz')]
        if not matched_files:
            print(f"No file found for {eid}")
            continue
        
        input_file = matched_files[0]  # Use first match
        input_path = os.path.join(input_dir, input_file)

        # Clean filename: remove the trailing _X
        clean_name = eid + '.nii.gz'
        output_file = clean_name.replace('.nii.gz', '_registered.nii.gz')
        output_path = os.path.join(output_dir, output_file)

        if os.path.exists(output_path):
            print(f"Skipping {eid}, already registered.")
            continue

        try:
            print(f"Registering {eid}...")
            moving = ants.image_read(input_path)
            moving_resampled = ants.resample_image_to_target(moving, fixed)
            reg = ants.registration(fixed=fixed, moving=moving_resampled, type_of_transform=type_reg)
            ants.image_write(reg['warpedmovout'], output_path)
            print(f"Saved: {output_path}")
        except Exception as e:
            print(f"Error registering {eid}: {e}")

#%%
# 
def deskull_images(input_dir, output_dir):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through NIfTI files in the input folder
    for file_name in os.listdir(input_dir):
        if file_name.endswith('_registered.nii.gz'):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name.replace('_registered.nii.gz', '_deskulled.nii.gz'))

            # Check if the output file already exists, skip if it does
            if os.path.exists(output_path):
                print(f'Skipping deskulling for {file_name} as the output already exists.')
                continue
            
            # Construct the hd-bet command
            command = f'hd-bet -i {input_path} -o {output_path} -device cuda:1'

            # Execute the command using subprocess
            subprocess.run(command, shell=True)

            print(f'Skull stripping completed for {file_name}')

#%%
if __name__ == "__main__":
    #deface_images_parallel(input_folder, deface_folder)
    register_images(input_folder, eids, reg_folder, fixed)
    deskull_images(reg_folder, deskull_folder)

# %%
