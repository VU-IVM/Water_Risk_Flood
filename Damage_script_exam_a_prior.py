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
# import damagescanner
# from damagescanner.core import RasterScanner
# import damagescanner.plot
# from damagescanner.core import RasterScanner

# loss_df_r = RasterScanner(landuse_map,inun_map,curve_path,maxdam_path, save=True, scenario_name='_HCMC', output_path=data_path)
# damagescanner.plot.inundation_map(inun_map, lu_raster=False, lu_vector=False, save=False)

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

#%% Load data...
curves = pd.read_csv(curve_path).dropna(axis = 1).values
curves[:,1:] = curves[:,1:]/100 #to convert to a value between 0 and 1
maxdam = pd.read_csv(maxdam_path).values

with rasterio.open(landuse_map) as src:
    landuse = src.read()[0, :, :]
    transform = src.transform

with rasterio.open(inun_map) as src:
    inundation = src.read()[0, :, :]
    transform = src.transform

cellsize = src.res[0] * src.res[1]
no_data = -9999

#%% Set the no value data values in the hazard and land use maps to NaN
inundation[inundation == no_data] = np.nan    # Assigns NaN to no data values in hazard map
landuse[landuse == no_data] = np.nan   # Assigns NaN to no data values in landuse map

#inundation[inundation > 10] = 0 ############################################################################ASK ELCO ABOUT THIS
inun = inundation * (inundation >= 0) + 0  #Extract data from inundation map only for inundated cells 
inun[inun >= curves[:, 0].max()] = curves[:, 0].max() #Set maximum inundation in the hazard map to the one in the depth-damage curve
area = inun > 0 #Keep inundation map only for inundated cells (in a TRUE-FALSE raster)
waterdepth = inun[inun > 0] #Keep inundation map only for inundated cells (in a VECTOR)
landuse = landuse[inun > 0] #Do the same as the last line, for the landuse map 


# Calculate damage per land-use class for structures
numberofclasses = len(maxdam)  # Automatically detect the number of land use classes
alldamage = np.zeros(landuse.shape[0]) 
damagebin = np.zeros((numberofclasses,2,))

#Looping through each land use classes
for i in range(0, numberofclasses):
#    print(i)
    n = maxdam[i, 0] #Selecting land class category
    damagebin[i, 0] = n  #Writing the land class category
    wd = waterdepth[landuse == n] #Selecting cells with the given land use category
    alpha = np.interp(wd, ((curves[:, 0])), curves[:, i + 1]) #Interpolating the depth-damage curve to obtain damage percentage at the given water depth
    damage = alpha * (maxdam[i, 1] * cellsize) #Calculate damage at each cell 
    damagebin[i, 1] = sum(damage) #Calculate the total damage for this land use category
    alldamage[landuse == n] = damage #Save damage result
    # print(n, max(alldamage))
    # print(alldamage.shape)
    
# create the damagemap
damagemap = np.zeros((area.shape[0], area.shape[1]), dtype='int32') #Create array
damagemap[area] = alldamage #Save damage values on the array
        
damagebin[:,1] = pd.to_numeric(damagebin[:,1])  
# create pandas dataframe with output
loss_df = pd.DataFrame(damagebin.astype(np.int64), columns=['landuse','losses']).groupby('landuse').sum()

#%% Save the damage as a geotiff
rst_opts = {
    'driver': 'GTiff',
    'height': damagemap.shape[0],
    'width': damagemap.shape[1],
    'count': 1,
    'dtype': damagemap.dtype,
    'crs': output_map_epsg,
    'transform': transform,
    'compress': "LZW"
}

with rasterio.open(os.path.join(data_path,output_folder,output_filename+'.tif'), 'w', **rst_opts) as dst:
    dst.write(damagemap, 1)

#%% % The line below saves the data to Excel
loss_df.to_csv(os.path.join(data_path,output_folder,output_filename+'.csv'))



        
