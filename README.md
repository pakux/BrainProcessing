# BrainProcessing
Preprocessing for Brain sMRI steps included:

1. Extracting zips (creates a dcm_raw folder based on BIDS format) 
2. nifti_raw (converts dcms to niftiis)
3. nifti_reg (registration)
4. nifti_deskull (skull-stripping)
5. npy180 (cropping and normalization and creation of npy tensors)
