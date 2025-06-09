A script to convert .ims and .czi files to .pngs, with maximum intensity projection of any z stacks.

#### To use:

- install conda packages:
`$ mamba create -n if-env cellpose pillow czifile tifffile`
- then activate the environment with 
`$ mamba activate if-env`
OR
`$ conda activate if-env`

- install imaris reader within the same environment:
`$ pip install imaris-ims-file-reader`

- download python script from this git page (convert_imsczi2png.py)

- make python script executable:
`$ chmod +x [path to script]/convert_imsczi2png.py`

- run script as follows:
`$ [provide path to script or '.' if you are in the directory with the script]/convert_imsczi2png.py -i [path to image file]/2025_04_29_Exp.2_control_293T_GFp_CAGESsi_siRNA_1.ims`

(check help function for full list of options): `$ ./convert_imsczi2png.py -h`

