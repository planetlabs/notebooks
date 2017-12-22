# Clip the Crop Data Layer file into a specified area of interest (AOI)

import os
import json
import rasterio
import subprocess
import matplotlib.image as mpimg

CDL_fname = 'CDL_files/CDL_Kings_2016_06031/CDL_2016_06031_clip_01.tif'
aoi_file = 'geojson_ROIs/kings_01_sub.geojson'

cdl_files = [CDL_fname]
clip_names = [os.path.abspath(cdl[:-4]+"_clip"+".tif") for cdl in cdl_files]
full_cdl_files = [os.path.abspath("./"+cdl) for cdl in cdl_files]

for in_file,out_file in zip(cdl_files,clip_names):
    commands = ["gdalwarp", # t
            "-t_srs","EPSG:3857",
            "-cutline",aoi_file,
            "-crop_to_cutline",
            "-tap",
            "-tr", "3", "3"
            "-overwrite"]
    subprocess.call(["rm",out_file])
    commands.append(in_file)
    commands.append(out_file)
    subprocess.call(commands)

