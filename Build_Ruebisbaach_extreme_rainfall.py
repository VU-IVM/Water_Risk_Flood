'''
Adapted from: Andres Diaz and Philip Ward
Coded into Python by Eric Mortensen and Anaïs Couasnon
Date: August 2020

DESCRIPTION:
This script prepares the precipitation data, aggregating the values in
different rainfall durations.

The homework consists of constructing empirical and analytical IDF curves from the 
Ruebisbaach precipitation data.
'''

#%% Loading packages and functions needed
import os, sys
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import scipy.optimize
from scipy.interpolate import PchipInterpolator

# Define folder paths and filenames
#Make sure to change the working directory to where your scripts are
root_folder = ''
os.chdir(root_folder)

#We import the functions we will use in this practical
from functions_Ruebisbaach import height_to_intensity, Gumbelfit_EM, Gumbel_evfit, empirical_T

#%% Import the data
# Folder where the precipitation data is located
fn_prec = ''
raw_rainfall_data = 'Ruebisbaach_precipitation_RAW_AC.csv'
fn = os.path.join(fn_prec,raw_rainfall_data)

#We import the data using the pandas package
date_format = lambda x: datetime.datetime.strptime(x, "%d-%m-%y %H:%M") #We define the date format to make the datetime are properly recognized
matrixPrec = pd.read_csv(fn, sep=';', date_parser = date_format, names = ['date', '0.5hr'], index_col = ['date'])

# %% Plotting the rainfall with the raw temporal time step
# This is always recommend to first have a look at the data before using it!
plt.figure()
plt.plot(matrixPrec.index, matrixPrec.loc[:,'0.5hr'], '.-b')
plt.ylabel('Rainfall (mm)')
plt.xlabel('Date')
plt.show()

# %% METHOD 1 - USING EXTREME VALUE ANALYSIS FROM OUR DATA

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
i_date_raw = matrixPrec.reset_index().groupby(pd.Grouper(key = 'date', freq = 'AS')).idxmax() #index of annual maxima
date_max_raw =  matrixPrec.iloc[i_date_raw.iloc[:,0].values,:].index  #Date of annual maxima

# This is always recommend to first have a look at the data before using it!
plt.figure()
plt.plot(matrixPrec.index, matrixPrec.loc[:,'0.5hr'], '.-b')
plt.plot(date_max_raw, matrixPrec.loc[date_max_raw,'0.5hr'], '*r')
plt.ylabel('Rainfall (mm)')
plt.xlabel('Date')
plt.show()

extreme1hr = matrixPrec1hr.resample('AS').max() #Annual maxima of 1-hr rainfall

# We combine the results
output = pd.concat([extreme_raw, extreme1hr], axis = 1)
# %% To remove before the class -------------------------------------------------------
# Calculating precipitation for other durations

duration = [0.5, 1, 3, 8, 12, 24]

#.....
#
#
#
#.....

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

return_periods = [5, 50, 100]
figure_plotting = 0 # This argument is passed to the functions below. If 0, then no plots are returned. If 1, then plots are returned.
IDF = pd.DataFrame(index = return_periods, columns = output.columns)
IDF.index.name='return_periods'

for dur in intensity_mmhr.columns:
    print(dur)
    # Fitting Gumbel with parameters based on Euler-Mascheroni constant and Apéry's constant.
    parameters, values , x_T = Gumbelfit_EM(intensity_mmhr.loc[:,dur], return_periods, figure_plotting)
    
    #Fitting Gumbel with parameters based on Maximum Likelihood Estimates 
    parameters2, values2 ,x_T2 = Gumbel_evfit(intensity_mmhr.loc[:,dur], return_periods, figure_plotting)
    
    #We calculate the empirical return period.
    emp_intensity = empirical_T(intensity_mmhr.loc[:,dur], figure_plotting)

    #We select the estimates provided by the first functions
    IDF.loc[:,dur] = x_T.transpose()

# We plot the differences between empirical and fitted Gumbel
plt.figure()
plt.title('IDF curves from data')
j = 0
for dur in IDF.columns:
    plt.plot(np.repeat(duration[j], len(IDF)), IDF.loc[:,dur].values, 'o')
    j += 1
plt.xlim(0,30)
plt.xlabel('Duration (hrs)')
plt.ylabel('Rainfall Intensity (mm/hr)')

#%% Make the IDF graph and fit an interpolation
# Smooth Original IDF Curves using splines: 
IDF_interp = pd.DataFrame(index = np.linspace(min(duration), max(duration), 100), columns = return_periods)
for r in IDF.index:
    z = PchipInterpolator(duration, IDF.loc[r,:].values) #Interpolation using Piecewise Cubic Hermite Interpolating Polynomial 
    ynew = z(IDF_interp.index.values)
    IDF_interp.loc[:,r] = ynew

#Plot the results
plt.figure()
j = 0
for dur in IDF.columns:
    plt.plot(np.repeat(duration[j], len(IDF)), IDF.loc[:,dur].values, '.k')
    j += 1

for ret_period in IDF_interp.columns:
    print(ret_period)
    plt.plot(IDF_interp.index, IDF_interp.loc[:, ret_period], '-', label = str(ret_period))
plt.legend()
plt.xlim(0,30)
plt.xlabel('Duration (hrs)')
plt.ylabel('Rainfall Intensity (mm/hr)')

#%% METHOD 2 - USING AN EMPIRICAL FUNCTION
# Fit the empirical function to obtain the IDF. Here we use a power law.

#We use the IDF values to create the variables needed to solve the equation:
# log(I) = log(k) + m log(T) + n log(D)

regression = pd.DataFrame(index = np.arange(0,len(return_periods)*len(duration),1), columns = ['log(I)','x_0','log(T)','log(D)'])
i=0
for r in return_periods:
    for dur in duration:
        regression.loc[i,'log(I)'] = np.log10(IDF.loc[r,str(dur)+'hr'])
        regression.loc[i, 'x_0'] = 1
        regression.loc[i, 'log(T)'] = np.log10(r)
        regression.loc[i, 'log(D)'] = np.log10(dur)
        i += 1

# Creating the matrices
Y = np.array(regression.loc[:,'log(I)'])
X_matrix = np.array(regression.loc[:,['x_0','log(T)','log(D)']])

#Solving the general linear model. For more information, see:
# https://en.wikipedia.org/wiki/Regression_analysis

X_matrix_transpose = X_matrix.transpose()
part_a = np.dot(X_matrix_transpose,Y) 
part_b0 = np.dot(X_matrix_transpose,X_matrix)
part_b = np.linalg.inv(np.matrix(part_b0, dtype='float'))
betas = np.dot(part_b,part_a)
beta_values = [10**betas[0,0], betas[0,1], -betas[0,2]]

# Calculate the empirical IDF based on the coefficients found.
IDF_emp = pd.DataFrame(index=np.linspace(0.5,24,1000), columns = return_periods)
for ret_per in IDF_emp.columns:
    print(ret_per)
    IDF_emp.loc[:,ret_per] = beta_values[0]*(ret_per**(beta_values[1])/(IDF_emp.index**(beta_values[2])))
    
# Plot the results
plt.figure()
j = 0
for dur in IDF.columns:
    plt.plot(np.repeat(duration[j], len(IDF)), IDF.loc[:,dur].values, '.k')
    j += 1

for ret_period in IDF_emp.columns:
    print(ret_period)
    plt.plot(IDF_emp.index, IDF_emp.loc[:, ret_period], '-', label = str(ret_period))
plt.legend()
plt.xlim(0,30)
plt.xlabel('Duration (hrs)')
plt.ylabel('Rainfall Intensity (mm/hr)')
#Add a legend to your figure!












