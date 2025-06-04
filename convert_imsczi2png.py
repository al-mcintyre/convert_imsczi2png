#!/usr/bin/env python3
# a script to convert .czi and .ims files to pngs
# A McIntyre (+AI), 2025

import czifile
import tifffile
import numpy as np
from imaris_ims_file_reader.ims import ims
from PIL import Image
import os

def save_img(img,input_file,output_dir,i,chan,int8=False):
    # Convert to uint8 if needed
    if int8 and img.dtype != np.uint8:
        img = (img / np.max(img) * 255).astype(np.uint8)

    output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_t{i}_c{chan}.png")
    print('saving image')
    Image.fromarray(img).save(output_file)
    return


def convert_ims_czi_to_png(input_file, output_dir, int8=False):
    """
    Converts IMS or CZI files to PNG images.

    Args:
        input_file (str): Path to the input IMS or CZI file.
        output_dir (str): Path to the directory to save the output PNG files.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
      if input_file.lower().endswith('.czi'):
        with czifile.CziFile(input_file) as czi_file:
            image_data = czi_file.asarray()
      elif input_file.lower().endswith('.ims'):
            image_data = ims(input_file)
            #image_data = tifffile.imread(input_file)
      else:
        print("Unsupported file format. Please provide a .czi or .ims file.")
        return

      print(image_data.ndim, 'dimensions in input file')
      if image_data.ndim > 3:
          print(image_data.shape[1],'channels detected')
          if image_data.ndim > 4:
              print(image_data.shape[2],'z slices detected')

      # Handle multi-dimensional images (e.g., time series, channels, zstack)
      if image_data.ndim > 2:
          for i in range(image_data.shape[0]): #for each time point.. 
              if image_data.ndim == 3:
                  img = image_data[i, :, :]
                  save_img(img,image_file,output_dir,i,0,int8)
              elif image_data.ndim > 3: #for each channel
                  for chan in range(image_data.shape[1]):
                      if image_data.ndim == 4:
                          img = image_data[i,chan,:,:]
                      elif image_data.ndim == 5: #take maximum intensity projection (MIP)
                          img_tmp = np.array(image_data[i,chan,:,:,:])
                          img = np.max(img_tmp, axis=0)
                      else:
                          print("Unsupported number of dimensions, please adjust code")
                          return
                      save_img(img,input_file,output_dir,i,chan,int8) 
      else:
          save_img(image_data,input_file,output_dir,0,0,int8)

      print("Conversion successful!")
    except Exception as e:
        print(f"Error during conversion: {e}")

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Convert .czi or .ims file to .png (with maximum intensity projection)')
    parser.add_argument('-i','--input_fi',type=str,required=True,help='provide file path')
    parser.add_argument('-o','--out_dir',type=str,required=False,help='output directory (default = output_pngs)',default="output_pngs")
    parser.add_argument('--int8',action='store_true',required=False,help='convert to int8 0-255 scale (default = False)',default=False)
    parser.add_argument('-v','--version',action='version',version='%(prog)s (v0.1)') 

    args = parser.parse_args()
    assert os.path.isfile(args.input_fi),'no file found at {}'.format([args.input_fi])

    convert_ims_czi_to_png(args.input_fi, args.out_dir, args.int8)

if __name__ == "__main__":
    main()
