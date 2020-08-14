# -*- coding: utf-8 -*-
"""
%% Damage_script_Session_10.m
% Script that replicates the steps of the Damagescanner to calculate
% economic damage based on input maps of hazard (inundation depth),
% exposure (land use map and associated maximum damage), and vulnerability
% (depth-damage functions)

% Input are a hazard map, land use map, table of maximum damage per land
% use class, and table of depth-damage functions per land use class

% Output: damage map per cell (geotiff) and Excel summary table of damage
% per land use category

% Author: Philip Ward (philip.ward@vu.nl)
% Date: 22 September 2018
"""
#%%Importing the relevant packages
import os
import numpy as np
import pandas as pd
import glob
import rasterio 
import damagescanner
from damagescanner.core import RasterScanner
import damagescanner.plot


#%% Define folder paths and filenames
    
            #data_path = r'E:\surfdrive\Documents\Master2020\Jip\Jip'

data_path = r'E:\surfdrive\Shared\Water_Risks\2019_2020\SESSION_MATERIALS\SESSION_8_Integrating_to_risk\PRACTICALS\Damage\example_exam'

landuse_map = os.path.join(data_path,'landuse_exam.tif') #Filename of your landuse map
curve_path = os.path.join(data_path,'TABLE_CURVES_exam.csv') #Filename of your depth-damage functions
maxdam_path = os.path.join(data_path,'TABLE_MAXDAM_exam.csv') #Filename of your maximum damage values
inun_map = os.path.join(data_path,'input_inun_maps', 'inun_exam_rp_00010.tif') #Filename of your hazard map

output_folder = 'output'              # A suffix name for your output folder
output_filename = 'output_damage';     # Filename of your output map
output_map_epsg = 3106;                # EPSG code of the coordinate system used

#%%
loss_df, damagemap, landuse_in, inundation = RasterScanner(landuse_map,inun_map,curve_path,maxdam_path, save=True, scenario_name='_try0010', output_path=os.path.join(data_path, output_folder))

#damagescanner.plot.inundation_map(inun_map, lu_raster=False, lu_vector=False, save=False)
