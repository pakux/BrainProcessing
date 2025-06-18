# BrainProcessing
Preprocessing for Brain sMRI steps included:

## 1. Extracting dcms
- extract_zip.py creates a structured dcm_raw folder after extracting downloaded data contained in zips
## 2. Dcm to niftii conversion
- dcm2nii.sh converts structured dcms to niftiis)
## 3. Nifti preprocessing 
- nifti_processing.py 
  - registers raw niftiis and saves into nifti_reg folder 
  - skull-stripps registered niftiis and saves into nifti_deskull folder
## 4. Tensor transformations
- npy_transforms.py includes cropping and normalization and creation of npy tensors
