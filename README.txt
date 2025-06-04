install conda packages:
$ mamba create -n if-env cellpose pillow czifile tifffile

install imaris reader:
$ pip install imaris-ims-file-reader

run script as follows (modify example path to file):
$ ./convert_imsczi2png.py -i /Users/alexam/Downloads/2025_04_29_Exp.2_control_293T_GFp_CAGESsi_siRNA_1.ims

