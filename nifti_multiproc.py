import os
import subprocess
import pandas as pd
import ants
import multiprocessing as mp
from functools import partial

# === Config ===
cohort = 'adni1-sc'
reg_type= 'Affine'
gpu_id = 'cuda:0'
input_folder = f'/images/{cohort}/nifti_raw/'
n4_folder = f'/images/{cohort}/nifti_n4/'
reg_folder = f'/images/{cohort}/nifti_reg_{reg_type}/'
deskull_folder = f'/images/{cohort}/nifti_deskull_{reg_type}/'
csv_path = f'/data/{cohort}/ad-cn.csv'
template_path = "/images/templates/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii"

# === Load template and EIDs ===
fixed = ants.image_read(template_path)
df = pd.read_csv(csv_path, dtype={'eid': str})
eids = df['eid'].tolist()
#eids = sorted(set(f.split('_')[0] for f in os.listdir(input_folder) if f.endswith('.nii') or f.endswith('.nii.gz')))[:10]


def bias_correct_single(eid):
    try:
        matched_files = [f for f in os.listdir(input_folder) if f.startswith(eid + '_') and f.endswith('.nii.gz')]
        if not matched_files:
            print(f"[SKIP] No input for {eid}")
            return
        input_file = matched_files[0]
        input_path = os.path.join(input_folder, input_file)

        output_file = input_file.replace('.nii.gz', '_n4.nii.gz')
        output_path = os.path.join(n4_folder, output_file)

        if os.path.exists(output_path):
            print(f"[SKIP] {eid} already bias corrected.")
            return

        print(f"[INFO] N4 correcting {eid}")
        img = ants.image_read(input_path)
        corrected = ants.n4_bias_field_correction(img)
        ants.image_write(corrected, output_path)
        print(f"[DONE] Bias corrected {eid}")
    except Exception as e:
        print(f"[ERROR] Bias correcting {eid}: {e}")

def register_single(eid):
    try:
        matched_files = [f for f in os.listdir(n4_folder) if f.startswith(eid + '_') and f.endswith('_n4.nii.gz')]
        if not matched_files:
            print(f"[SKIP] No N4 image for {eid}")
            return
        input_path = os.path.join(n4_folder, matched_files[0])

        output_file = f"{eid}_registered.nii.gz"
        output_path = os.path.join(reg_folder, output_file)

        if os.path.exists(output_path):
            print(f"[SKIP] {eid} already registered.")
            return

        print(f"[INFO] Registering {eid}")
        moving = ants.image_read(input_path)
        reg = ants.registration(fixed=fixed, moving=moving, type_of_transform=reg_type)
        ants.image_write(reg['warpedmovout'], output_path)
        print(f"[DONE] {eid}")
    except Exception as e:
        print(f"[ERROR] Registering {eid}: {e}")

# === Deskulling ===
def deskull_single(file_name, gpu_id):
    if not file_name.endswith('_registered.nii.gz'):
        return

    input_path = os.path.join(reg_folder, file_name)
    output_file = file_name.replace('_registered.nii.gz', '_deskulled.nii.gz')
    output_path = os.path.join(deskull_folder, output_file)

    if os.path.exists(output_path):
        print(f"[SKIP] {file_name} already deskulled.")
        return

    try:
        command = f'hd-bet -i {input_path} -o {output_path} -device {gpu_id}'
        subprocess.run(command, shell=True, check=True)
        print(f"[DONE] Deskulled {file_name} on GPU {gpu_id}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Deskulling {file_name} on GPU {gpu_id}: {e}")

# === Run ===
if __name__ == "__main__":
    os.makedirs(n4_folder, exist_ok=True)
    os.makedirs(reg_folder, exist_ok=True)
    os.makedirs(deskull_folder, exist_ok=True)

    print("=== Starting N4 bias correction ===")
    with mp.Pool(processes=4) as pool:
        pool.map(bias_correct_single, eids)

    print("=== Starting registration ===")
    with mp.Pool(processes=4) as pool:  
        pool.map(register_single, eids)

    print("=== Starting deskulling sequentially on GPU 0 ===")
    all_files = [f for f in os.listdir(reg_folder) if f.endswith('_registered.nii.gz')]

    for f in all_files:
        deskull_single(f, gpu_id)

