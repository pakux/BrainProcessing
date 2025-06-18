# BrainProcessing
Preprocessing for Brain sMRI steps included:
## Steps
### 1. Extracting dcms
- extract_zip.py creates a structured dcm_raw folder after extracting downloaded data contained in zips
### 2. Dcm to niftii conversion 
- dcm2nii.sh converts structured dcms to niftiis  #if you already have a BIDS-structured dcm_raw folder 
### 3. Nifti preprocessing 
- nifti_processing.py 
  - registers raw niftiis and saves into nifti_reg folder 
  - skull-stripps registered niftiis and saves into nifti_deskull folder
### 4. Tensor transformations
- npy_transforms.py includes cropping and normalization and creation of npy tensors
- python npy_transforms.py --cohort ixi --img_size 180 --input_folder /data/input --output_folder /data/output
## Expected Directory Structure
Stucture of the Image Directory in the end          
- cohort 1
  - dcm_cmprs
  - dcm_raw
  - nifti_raw
  - nifti_reg
  - nifti_deskull
  - npy_cohort180 
- cohort 2
- cohort 3

#Intermediate processing folders can be deleted after checking the correct final product that is the npy images
