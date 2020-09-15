# -*- coding: utf-8 -*-
"""
%% Damage_script_Session_10
% Script that replicates the steps of the Damagescanner to calculate
% economic damage based on input maps of hazard (inundation depth),
% exposure (land use map and associated maximum damage), and vulnerability
% (depth-damage functions)
% Input are a hazard map, land use map, table of maximum damage per land
% use class, and table of depth-damage functions per land use class
% Output: damage map per cell (geotiff) and Excel summary table of damage
% per land use category

% Author: Philip Ward (philip.ward@vu.nl)
% Date: 10 August 2017
"""
#%%Importing the relevant packages
import os #package to manipulate and connect paths and files.
import glob #package to list folders and files.
import numpy as np #mathematical package for fast operations on arrays.
import pandas as pd #mathematical package for operations on arrays with labelled columns and indexes. Very good for time serie analysis 
import rasterio #package for raster operation

import damagescanner #Package to do risk damage calculations. See also: https://github.com/ElcoK/DamageScanner
from damagescanner.core import RasterScanner #From the package, we import the function RasterScanner we want to work with
#%% Define folder paths and filenames
data_path = r'E:\surfdrive\Shared\Water_Risks\2019_2020\SESSION_MATERIALS\SESSION_8_Integrating_to_risk\PRACTICALS\Damage\example_exam'  # The root folder from which you are working.

inun_map = 'input_inun_maps' # Folder where hazard maps are stored

output_folder = 'output'              # A suffix name for your output folder
output_filename = 'output_damage'      # Filename of your output summary table file
output_map_epsg = 3106;                # EPSG code of the coordinate system used

#%% Load data 
inun_map = os.path.join(data_path,'inun_exam_rp_00100.tif') #Filename of your hazard map
landuse_map = os.path.join(data_path,'landuse_exam.tif') #Filename of your landuse map
curve_path = os.path.join(data_path,'TABLE_CURVES_exam.csv') #Filename of your depth-damage functions
maxdam_path = os.path.join(data_path,'TABLE_MAXDAM_exam.csv') #Filename of your maximum damage values

#Read csv data
curves = pd.read_csv(curve_path).dropna(axis = 1).values #Reading csv file of depth-damage curves and storing it in an array 
curves[:,1:] = curves[:,1:]/100 #Converting the depth-damage curve to a ratio (i.e. value between 0 and 1)

#%% Calculate the damage and output the raster and damage summary table using the function 
loss_df_rp, _, _, _ = RasterScanner(landuse_map,inun_map,curves,maxdam_path, save=True, scenario_name='rp_00100', output_path=os.path.join(data_path, output_folder), dtype = np.float32, nan_value = 9999)

    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    

