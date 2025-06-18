# BrainProcessing
Preprocessing for Brain sMRI steps included:

1. extract_zip.py (creates a structured dcm_raw folder after extracting downloaded data contained in zips) 
2. dcm2nii.sh (converts structured dcms to niftiis)
3. nifti_processing.py 
  a. registered images go to nifti_reg folder 
  b. skull-stripped registered images go to nifti_deskull folder
7. npy.py  (cropping and normalization and creation of npy tensors)
