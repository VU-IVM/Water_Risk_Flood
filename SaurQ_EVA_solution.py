'''
Adapted from: Andres Diaz and Philip Ward
Coded into Python by Eric Mortensen and Anaïs Couasnon
Date: August 2020

DESCRIPTION:
This script imports the hourly discharge data from the Sauer river and
performs extreme value analysis
'''

#%% Loading packages and functions needed
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

# Define folder paths and filenames
#Make sure to change the working directory to where your scripts are
root_folder = r'C:\Users\acn980\Desktop\WATER RISKS\SESSION_3_Flood_Hazard_I\FINAL\UPLOAD\PYTHON'
os.chdir(root_folder)

from functions_Ruebisbaach import Gumbelfit_EM, Gumbel_evfit, empirical_T
#%% Define folder paths and filenames
fn_Q = r'C:\Users\acn980\Desktop\WATER RISKS\SESSION_3_Flood_Hazard_I\FINAL\UPLOAD' #Folder where your data are located
raw_data = 'DIEKIRCH_Q60_2002-2017.csv'
fn = os.path.join(fn_Q,raw_data)

#We import the data using the pandas package
date_format = lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M:%S") #We define the date format to make the datetime are properly recognized
Discharge = pd.read_csv(fn, date_parser = date_format, usecols = [0,3], names = ['date', 'Q'], index_col = ['date'])

#Plot the raw data - the rainfall with a time step of 30min
#This is always recommend to first have a look at the data before using it!
plt.figure()
plt.plot(Discharge.index, Discharge.loc[:,'Q'], '.-b')
plt.ylabel('Discharge (m3/s)')
plt.xlabel('Date')
plt.show()

#%% We extract the extreme values using the Annual Maxima method
extreme_raw = Discharge.resample('AS').max() #Annual maxima of 30-min rainfall
i_date_raw = Discharge.reset_index().groupby(pd.Grouper(key = 'date', freq = 'AS')).idxmax() #index of annual maxima
date_max_raw =  Discharge.iloc[i_date_raw.iloc[:,0].values,:].index  #Date of annual maxima

# This is always recommend to first have a look at the data before using it!
plt.figure()
plt.plot(Discharge.index, Discharge.loc[:,'Q'], '.-b')
plt.plot(date_max_raw, Discharge.loc[date_max_raw,'Q'], '*r')
plt.ylabel('Rainfall (mm)')
plt.xlabel('Date')
plt.show()

#%% Fitting an Extreme Value Analysis (EVA) distribution
# We want to extrapolate our data to events we did not observe yet. We will
# use the function "Gumbelfit_EM" and "Gumbel_evfit". Both functions
# estimate the parameters of the distribution using a different method. Both
# functions return three arguments:
#--> The first is a structure with the values of the parameters
#--> The second is a matrix with two columns with in column1 x and in column2 ICDF(x)
#--> The third is an array with the expected values of x at given return periods

return_periods = [2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000]
return_periods = [10, 25, 100]
figure_plotting = 1 #This argument is passed to the functions below. If 0, then no plots are returned. If 1, then plots are returned.

#Fitting Gumbel with parameters based on Euler-Mascheroni constant and Apéry's constant.
parameters, values , x_T = Gumbelfit_EM(extreme_raw.loc[:,'Q'], return_periods, figure_plotting)

#Fitting Gumbel with parameters based on Maximum Likelihood Estimates 
parameters2, values2 ,x_T2 = Gumbel_evfit(extreme_raw.loc[:,'Q'], return_periods, figure_plotting)

#We calculate the empirical return period.
emp_intensity = empirical_T(extreme_raw.loc[:,'Q'], figure_plotting)

plt.figure()
plt.title('Return Period - semilog')
plt.semilogx(1./values.loc[:,'Exceedance_prob'], values.loc[:,'Exceedance_prob'].index, '-r')
plt.semilogx(return_periods, x_T, '*r')
plt.semilogx(1./values2.loc[:,'Exceedance_prob'], values2.loc[:,'Exceedance_prob'].index, '-g')
plt.semilogx(return_periods, x_T2, '*g')
plt.semilogx(emp_intensity.iloc[:,-1], emp_intensity.iloc[:,0], 'ok')
plt.grid()
plt.ylabel('Discharge (m³/s)')
plt.xlabel('Return Period (yrs)')

#%% PART 2 - Compare SCS discharge hydrograph with the time series. 

# We focus on the 1/10 discharge event
# Import data
raw_dataSCS = 'unit_hydrograph_Sauer.xlsx'
fn = os.path.join(fn_Q,raw_dataSCS)
Q10 = pd.read_excel(fn, sheet_name = 'Hydrograph_Standarized', usecols="A, I")

Discharge.reset_index(inplace = True)

i_max = Discharge.where(Discharge.Q == 342.5).dropna().index
steps = 28
i_beg = int(i_max.values) - steps
i_end = int(i_max.values) + (steps*5)

sel_Q = Discharge.iloc[i_beg:i_end,:].copy()
sel_Q.reset_index(drop = True, inplace = True)
sel_imax = sel_Q.loc[:,'Q'].idxmax()
sel_Q.loc[:,'t_Tp'] = sel_Q.index/sel_imax

plt.figure()
plt.plot(sel_Q.t_Tp, sel_Q.Q, '-ob')
plt.plot(Q10.iloc[:,0], Q10.iloc[:,1], '-or')
plt.xlabel('Dimensionless time')
plt.ylabel('Discharge (m³/s)')


