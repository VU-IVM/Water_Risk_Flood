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

input_folder_hazard_maps = 'input_inun_maps' # Folder where hazard maps are stored

output_folder = 'output'              # A suffix name for your output folder
output_filename = 'output_damage'      # Filename of your output summary table file
output_map_epsg = 3106;                # EPSG code of the coordinate system used

#%% Create list of all inundation maps in the input hazard maps folder
hazard_filenames = glob.glob(os.path.join(data_path,input_folder_hazard_maps,'*.tif')) #We only list files finishing by .tif

#%% Load data outside the loop
landuse_map = os.path.join(data_path,'landuse_exam.tif') #Filename of your landuse map
curve_path = os.path.join(data_path,'TABLE_CURVES_exam.csv') #Filename of your depth-damage functions
maxdam_path = os.path.join(data_path,'TABLE_MAXDAM_exam.csv') #Filename of your maximum damage values

#Read csv data
curves = pd.read_csv(curve_path).dropna(axis = 1).values #Reading csv file of depth-damage curves and storing it in an array 
curves[:,1:] = curves[:,1:]/100 #Converting the depth-damage curve to a ratio (i.e. value between 0 and 1)
#%% Loop through inundation maps
#We want to save the damages per land-use class for each return period in an overall summary table
damage_per_class_all_rps = pd.DataFrame(data=None)
for inun_map in hazard_filenames:
    print(inun_map)   
    #Extract return period string for this iteration
    str1 = inun_map.split('inun_exam_')[-1]
    name_rp = str1.split('.tif')[0]    
    
    #Calculate the damage and output the raster and damage summary table using the function 
    loss_df_rp, _, _, _ = RasterScanner(landuse_map,inun_map,curves,maxdam_path, save=True, scenario_name=name_rp, output_path=os.path.join(data_path, output_folder), dtype = np.float32, nan_value = 9999)
    loss_df_rp.rename(columns = {'losses':name_rp}, inplace = True) #We change the name of the column with the RP
    
    damage_per_class_all_rps = damage_per_class_all_rps.join(loss_df_rp, how = 'outer') #We append the column to the overall summary table
    
    
#%% Write the total damage per land use class to an Excel file...
damage_per_class_all_rps.to_csv(os.path.join(data_path,output_folder,output_filename+'.csv'), index_label = 'landuse') #Export as a csv

    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    

