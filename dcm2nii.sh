#!/bin/bash

INPUT_DIR= {your_dcm_dir_path}
OUTPUT_DIR= {your_nifti_dir_path}

# Add dcm2niix path (optional if not in PATH)
DCM2NIIX="{your_workspace}/dcm2niix/console/build/dcm2niix"

mkdir -p "$OUTPUT_DIR"

for subj_dir in "$INPUT_DIR"/*; do
    if [ -d "$subj_dir" ]; then
        subj_id=$(basename "$subj_dir")

        echo "Converting $subj_id..."
        "$DCM2NIIX" -z y -f "${subj_id}_%s" -o "$OUTPUT_DIR" "$subj_dir"
    fi
done
