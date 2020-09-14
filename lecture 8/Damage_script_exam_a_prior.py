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
% Date: 22 September 2018
"""
#%%Importing the relevant packages
import os #package to manipulate and connect paths and files.
import glob #package to list folders and files.
import numpy as np #mathematical package for fast operations on arrays.
import pandas as pd #mathematical package for operations on arrays with labelled columns and indexes. Very good for time serie analysis 
import rasterio #package for raster operation

#%% Define folder paths and filenames
data_path = r'E:\surfdrive\Shared\Water_Risks\2019_2020\SESSION_MATERIALS\SESSION_8_Integrating_to_risk\PRACTICALS\Damage\example_exam'

output_folder = 'output'              # A suffix name for your output folder
output_filename = 'output_damage';     # Filename of your output map
output_map_epsg = 3106;                # EPSG code of the coordinate system used

#%% Load data
landuse_map = os.path.join(data_path,'landuse_exam.tif') #Filename of your landuse map
curve_path = os.path.join(data_path,'TABLE_CURVES_exam.csv') #Filename of your depth-damage functions
maxdam_path = os.path.join(data_path,'TABLE_MAXDAM_exam.csv') #Filename of your maximum damage values
inun_map = os.path.join(data_path, 'inun_exam_rp_00100.tif') #Filename of your hazard map

#Read csv data
curves = pd.read_csv(curve_path).dropna(axis = 1).values #Reading csv file of depth-damage curves and storing it in an array 
curves[:,1:] = curves[:,1:]/100 #Converting the depth-damage curve to a ratio (i.e. value between 0 and 1)

maxdam = pd.read_csv(maxdam_path).values #Reading csv file of maximum damage and storing it in an array 

#Read raster data
with rasterio.open(landuse_map) as src: #Reading the landuse map and storing it in an array
    landuse = src.read()[0, :, :]
    transform = src.transform

with rasterio.open(inun_map) as src: #Reading the inundation map and storing it in an array
    inundation = src.read()[0, :, :]
    transform = src.transform
    
#%% Setting no data value and calculating cell size
#Calculate cell size of one cell: be careful with units!
cellsize = src.res[0] * src.res[1] #in the rasterio package '.res' will return the resolution of the cell along the x or y axis (0 or 1)

no_data = 9999  #Setting the no data value

#%% Calculating the damage

# Set the no value data values in the hazard and land use maps to NaN
inundation[inundation == no_data] = np.nan    # Assigns NaN to no data values in hazard map
landuse[landuse == no_data] = np.nan   # Assigns NaN to no data values in landuse map

#Extract data from inundation map only for inundated cells 
inun = inundation * (inundation >= 0) + 0  #Creates a mask of cells to select (TRUE-FALSE raster) and select their values. The '+0' makes sure no values are left with negative signs
inun[inun >= curves[:, 0].max()] = curves[:, 0].max() #Set maximum inundation in the hazard map to the one in the depth-damage curve
area = inun > 0 #Keep inundation map only for inundated cells (in a TRUE-FALSE raster)
waterdepth = inun[inun > 0] #Keep inundation map only for inundated cells (in a VECTOR)
landuse = landuse[inun > 0] #Do the same as the last line, for the landuse map 


# Calculate damage per land-use class 
numberofclasses = len(maxdam)  # Automatically detect the number of land use classes
alldamage = np.zeros(landuse.shape[0]) # Creates a vector of the same size as landuse to store the damage results per cell
damagebin = np.zeros((numberofclasses,2,)) # Creates an array to store the summary of damages per land-use class

#Looping through each land use classes
for i in range(0, numberofclasses):
    n = maxdam[i, 0] #Selecting land class category
    damagebin[i, 0] = n  #Writing the land class category in the summary table
    wd = waterdepth[landuse == n] #Selecting cells with the given land use category
    alpha = np.interp(wd, ((curves[:, 0])), curves[:, i + 1]) #Interpolating the depth-damage curve to obtain damage ratio at the given water depth
    damage = alpha * (maxdam[i, 1] * cellsize) #Calculate damage at each cell by multiplying the ratio by the maximum damage
    damagebin[i, 1] = sum(damage) #Calculate the total damage for this land use category
    alldamage[landuse == n] = damage #Save damage result for the cell with the selected land-use class

#%%Store the damage raster results and export it
    
# create the raster damagemap
damagemap = np.zeros((area.shape[0], area.shape[1]), dtype='int32') #Create a 2D array of zeros to store the damage values with the same shape as your input shape
damagemap[area] = alldamage #Save damage values on the 2D array using the TRUE-FALSE mask of inundated cells

# Save the raster damagemap as a geotiff
#We set the raster options to be used by the rasterio function wrtie(). 
#For a full list of the arguments accepted by the rasterio.open() function, see: https://rasterio.readthedocs.io/en/latest/api/rasterio.html#rasterio.open
rst_opts = {
    'driver': 'GTiff', #Type of raster
    'height': damagemap.shape[0],  #nb of cells of raster - vertical
    'width': damagemap.shape[1],  #nb of cells of raster - horizontal
    'count': 1, #Defines the number of bands to write
    'dtype': damagemap.dtype, #data type - here integers
    'crs': output_map_epsg, #coordinate system 
    'transform': transform, #information normally stored in the .prj file in GIS projects
    'compress': "LZW" #to compress the data and make it less voluminous
}

with rasterio.open(os.path.join(data_path,output_folder,output_filename+'.tif'), 'w', **rst_opts) as dst: #we use the .open() function to write the raster ('w' stands for write)
    dst.write(damagemap, 1) #We write the 2D array damagemap as a tif raster with 1 band
#%%  Export the summary of damages per land-use class to a csv file using the pandas package  
loss_df = pd.DataFrame(damagebin.astype(np.int64), columns=['landuse','losses']).set_index('landuse') #Create a dataframe with appropriate columns names 
loss_df.to_csv(os.path.join(data_path,output_folder,output_filename+'.csv'), index_label = 'landuse') #Export as a csv



        
