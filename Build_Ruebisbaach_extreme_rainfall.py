# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 15:45:09 2020

@author: acn980
"""

# Adapted from: Andres Diaz and Philip Ward
# Coded into Python by Eric Mortensen and Anaïs Couasnon
# Date: 2020


# DESCRIPTION:
# This script prepares the precipitation data, aggregating the values in
# different rainfall durations.

# The homework consists of constructing empirical and analytical IDF curves from the 
# Ruebisbaach precipitation data.
#%% importing relevant packages
import os, sys
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

from functions import rainfall_intensity




#%% Define folder paths and filenames
#Folder where your data and scripts are
root_folder = r'E:\surfdrive\Shared\Water_Risks\2019_2020\SESSION_MATERIALS\SESSION_3_Flood_Hazard_I\Practical_Session\UPLOAD' 
raw_rainfall_data = 'Ruebisbaach_precipitation_RAW_AC.csv'
fn = os.path.join(root_folder,raw_rainfall_data)

#We import the data using the pandas package
date_format = lambda x: datetime.datetime.strptime(x, "%d-%m-%y %H:%M") #We define the date format to make the datetime are properly recognized
matrixPrec = pd.read_csv(fn, sep=';', date_parser = date_format, names = ['date', '0.5hr'], index_col = ['date'])

#%% Plotting the rainfall with a time step of 30min
# This is always recommend to first have a look at the data before using it!
plt.figure()
plt.plot(matrixPrec.index, matrixPrec.loc[:,'0.5hr'], '.-b')
plt.ylabel('Rainfall (mm)')
plt.xlabel('Date')
plt.show()

#%% METHOD 1 - USING EXTREME VALUE ANALYSIS FROM OUR DATA

# Extracting extreme values using Annual Maxima method
# We will accumulate over a number of different intervals. 
# Note: if we have half hour data and we accumulate 4 intervals, our output data will be 2 hour interval 
# duration. Below, we give the example for 30-min and 1 hour, you will need to to it for
# other durations
duration = [0.5, 1]

matrixPrec1hr = matrixPrec.resample('H').sum()
matrixPrec1hr.rename(columns={'0.5hr': '1hr'}, inplace = True)

# We extract the extreme values using the Annual Maxima method
extreme_raw = matrixPrec.resample('AS').max() #Annual maxima of 30-min rainfall
#date_max_raw = #####################################################################

extreme1hr = matrixPrec1hr.resample('AS').max() #Annual maxima of 1-hr rainfall

# We combine the results
output = pd.concat([extreme_raw, extreme1hr], axis = 1)
#%% To remove before the class -------------------------------------------------------
# Calculating precipitation for other durations

duration = [0.5, 1, 3, 6, 12, 24]

matrixPrec3hr = matrixPrec.resample('3H').sum()
matrixPrec3hr.rename(columns={'0.5hr': '3hr'}, inplace = True)

matrixPrec6hr = matrixPrec.resample('6H').sum()
matrixPrec6hr.rename(columns={'0.5hr': '6hr'}, inplace = True)

matrixPrec12hr = matrixPrec.resample('12H').sum()
matrixPrec12hr.rename(columns={'0.5hr': '12hr'}, inplace = True)

matrixPrec24hr = matrixPrec.resample('D').sum()
matrixPrec24hr.rename(columns={'0.5hr': '24hr'}, inplace = True)

extreme3hr = matrixPrec3hr.resample('AS').max() #Annual maxima of 3-hr rainfall
extreme6hr = matrixPrec6hr.resample('AS').max() #Annual maxima of 6-hr rainfall
extreme12hr = matrixPrec12hr.resample('AS').max() #Annual maxima of 12-hr rainfall
extreme24hr = matrixPrec24hr.resample('AS').max() #Annual maxima of 24-hr rainfall

# We combine the results
output = pd.concat([extreme_raw, extreme1hr, extreme3hr, extreme6hr, extreme12hr, extreme24hr], axis = 1)
#%% Convert to rainfall intensity
intensity_mmhr = pd.DataFrame(data = None, columns = output.columns)
for i in np.arange(0,len(output.columns), 1):
    intensity_mmhr.iloc[:,i] = height_to_intensity(output.iloc[:,i], duration[i]) 
#%% Fitting an Extreme Value Analysis (EVA) distribution
# We want to extrapolate our data to events we did not observe yet. We will
# use the function "Gumbelfit_EM" and "Gumbel_evfit". Both functions
# estimate the parameters of the distribution using a different method. Both
# functions return three arguments:
#--> The first is a structure with the values of the parameters
#--> The second is a matrix with two columns with in column1 x and in column2 ICDF(x)
#--> The third is an array with the expected values of x at given return periods

return_periods = [10,50,100]
figure_plotting = 1 # This argument is passed to the functions below. If 0, then no plots are returned. If 1, then plots are returned.
IDF = pd.DataFrame(index = return_periods, columns = duration)
IDF.index.name='return_periods'

for dur in intensity_mmhr.columns:
    print(dur)
    # Fitting Gumbel with parameters based on Euler-Mascheroni constant and Apéry's constant.
    parameters, values , x_T = Gumbelfit_EM(intensity_mmhr.loc[:,dur], return_periods, figure_plotting)
    
    #Fitting Gumbel with parameters based on Maximum Likelihood Estimates 
    parameters2, values2 ,x_T2 = Gumbel_evfit(intensity_mmhr.loc[:,dur], return_periods, figure_plotting)
    
    #We calculate the empirical return period.
    emp_intensity = empirical_T(intensity_mmhr.loc[:,dur], figure_plotting);

    #We select the estimates provided by the first functions
    IDF.loc[:,dur] = x_T.transpose
    
    

    
 
#%%
# We save this table to construct our graph
# Tip: first make a variable to hold the output in that you want (the
# columns with the data per year for the different durations
#output = pd.concat(extre3hr(:,2),extre6hr(:,2),extre12hr(:,2),extre24hr(:,2)];

#%%
# Add lines below to save the output in the same format as in the file
# "Manzese_rainfall.txt" (but give it a different name!)
# Then add a line to save this (you can use save: see the Matlab help file
# to find out how save works...

#save(strcat(root_folder,'\Ruebisbaach_rainfall_IDF.txt'), 'output', '-ascii');












