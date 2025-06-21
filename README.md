# BrainProcessing
Preprocessing for Brain sMRI:
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
## Data Layout  

All datasets live under a top-level `images/` directory outside the preprocessing code in image_processing directory which should preferably be parallel to image directory but not inside. 
Each cohort has its own subdirectory for images at different preprocessing steps.

Data Tree

```text
images/
├── {cohort1}/
│   ├── dcm_cmprs/
│   │   ├── batch1.zip
│   │   ├── batch2.zip
│   │   └── ...
│   ├── dcm_raw/
│   │   ├── {eid1}/
│   │   │   ├── xx1.dcm
│   │   │   ├── xx2.dcm
│   │   │   └── ...
│   │   └── {eid2}/
│   ├── nifti_raw/
│   │   ├── {eid1}.nii.gz
│   │   └── ...
│   ├── nifti_reg/
│   │   ├── {eid1}_registered.nii.gz
│   │   └── ...
│   ├── nifti_deskull/
│   │   ├── {eid1}_deskulled.nii.gz
│   │   └── ...
│   ├── npy_{cohort1}180/
│   │   ├── {eid1}.npy
│   │   └── ...
├── {cohort2}/
├── {cohort3}/...
```



### Tips
- You can create npy_{cohort1}96 directory too, to test run with smaller images first. Give img_size=96 to npy_transforms.py that will downsize the 3D images using torchio.
- Delete the registered niftii folder later if you have verified that all were correctly registered, in case you want to save space.
- Different registering techniques can also be tried, for example, set reg_path as a new nifti_reg_nlin folder to save nonlinear registration and set 'SyN' as the Ants registration parameter.

