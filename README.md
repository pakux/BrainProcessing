# BrainProcessing
Preprocessing for Brain sMRI steps included:

## 1. Extracting dcms
- extract_zip.py creates a structured dcm_raw folder after extracting downloaded data contained in zips
## 2. Dcm to niftii conversion 
- dcm2nii.sh converts structured dcms to niftiis  #if you already have a BIDS-structured dcm_raw folder 
## 3. Nifti preprocessing 
- nifti_processing.py 
  - registers raw niftiis and saves into nifti_reg folder 
  - skull-stripps registered niftiis and saves into nifti_deskull folder
## 4. Tensor transformations
- npy_transforms.py includes cropping and normalization and creation of npy tensors

Stucture of the Image Directory in the end: #Feel free to delete intermediate processing folders after checking the correct final product that is the npy images
- cohort 1
  - dcms_cmprs
  - dcms_raw
  - nifti_raw
  - nifti_reg
  - nifti_deskull
  - npy_cohort180 
- cohort 2
- cohort 3
