import os
import subprocess
import pandas as pd
import ants
import multiprocessing as mp
from functools import partial

# === Config ===
# Add necessary variables here
input_folder = f'{path}/images/{cohort}/nifti_raw/'
reg_folder = f'{path}/images/{cohort}/nifti_reg_nlin/'
deskull_folder = f'{path}/images/{cohort}/nifti_deskull_nlin/'
csv_path = f'{path}/data/{cohort}/{csv_name}.csv'
template_path = "{path}/images/templates/mni_icbm152_nlin_asym_09c/mni_icbm152_pd_tal_nlin_asym_09c.nii"

# === Load template and EIDs ===
fixed = ants.image_read(template_path)
df = pd.read_csv(csv_path, dtype={'eid': str})
eids = df['eid'].tolist()[:1000]

# === Registration ===
def register_single(eid):
    try:
        matched_files = [f for f in os.listdir(input_folder) if f.startswith(eid + '_') and f.endswith('.nii.gz')]
        if not matched_files:
            print(f"[SKIP] No file found for {eid}")
            return
        input_file = matched_files[0]
        input_path = os.path.join(input_folder, input_file)

        output_file = f"{eid}_registered.nii.gz"
        output_path = os.path.join(reg_folder, output_file)

        if os.path.exists(output_path):
            print(f"[SKIP] {eid} already registered.")
            return

        print(f"[INFO] Registering {eid}")
        moving = ants.image_read(input_path)
        reg = ants.registration(fixed=fixed, moving=moving, type_of_transform='SyN')
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
        command = f'hd-bet -i {input_path} -o {output_path} -device cuda:{gpu_id}'
        subprocess.run(command, shell=True, check=True)
        print(f"[DONE] Deskulled {file_name} on GPU {gpu_id}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Deskulling {file_name} on GPU {gpu_id}: {e}")

# === Run ===
if __name__ == "__main__":
    os.makedirs(reg_folder, exist_ok=True)
    os.makedirs(deskull_folder, exist_ok=True)

    print("=== Starting nonlinear registration ===")
    with mp.Pool(processes=4) as pool:  
        pool.map(register_single, eids)

    print("=== Starting deskulling on 2 GPUs ===")
    all_files = [f for f in os.listdir(reg_folder) if f.endswith('_registered.nii.gz')]
    gpu0_files = all_files[::2]
    gpu1_files = all_files[1::2]

    # Run deskulling on both GPUs in parallel
    with mp.Pool(processes=2) as pool:
        pool.starmap(deskull_single, [(f, 0) for f in gpu0_files] + [(f, 1) for f in gpu1_files])
