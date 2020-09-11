# -*- coding: utf-8 -*-
"""
#Simple script to calculate EAD
#Author: Philip Ward (philip.ward@vu.nl)
#Date: 11th August 2017

"""

import os #package to manipulate and connect paths and files.
import numpy as np #mathematical package for fast operations on arrays.
import matplotlib.pyplot as plt #package used in the vizualisation and plotting of data
import pandas as pd #mathematical package for time serie analysis based on data frames
#%% Define root folder, and location of input damages and return periods
root_folder = r'C:\Users\Moedj\OneDrive\Overig\Documenten\GitHub\Water_Risk_Flood' #r: refers to the root folder you are using, this is a formatting style for python
input_file = 'ead_example_damage_input.csv'

fn = os.path.join(root_folder, input_file)
#%% Load input file, extract damages and return periods
data = pd.read_csv(fn) 
data.rename(columns = {data.columns[-1]:'Damage_usd'}, inplace = True) #renaming a column header based on indexing
data.sort_values(by='RP', ascending=True, inplace=True) #sorting values based on there return periods

#Make a figure to make it is all correct
plt.figure()
plt.semilogx(data.loc[:,'RP'], data.loc[:,'Damage_usd'], '-or') #loc: this is a method to locate data from a dataframe by using the column headers, note: this must without typos
plt.xlabel('Return Period')
plt.ylabel('Damage (USD)')
plt.show()

#%% Define protection level
prot = 75 #Protection standard below which zero damage and above which dike fails     

#Can you work out what is happening here?
dam_prot = np.interp(prot, data.loc[:,'RP'], data.loc[:,'Damage_usd']) #loc: this is a method to locate data from a dataframe by using the column headers, note: this must without typos

data_insert = pd.DataFrame(data = np.array([[prot, dam_prot], [prot-0.0001, 0]]), columns = data.columns)
data = pd.concat([data, data_insert], axis = 0).sort_values(by='RP', ascending=True).reset_index(drop=True) #first we merge the data using concat from the pandas libary, then we sort the data based on return period and finaly re-index our dataframe 
data.loc[data.loc[:,'RP']<prot, 'Damage_usd'] = 0

#%% Calculate exceedance probability
data.loc[:, 'ep'] = 1/data.loc[:,'RP'] #loc: this is a method to locate data from a dataframe by using the column headers
data.sort_values(by='ep', ascending=True, inplace = True)

#Calculate EAD...
ead = np.trapz(y = data.loc[:, 'Damage_usd'], x = data.loc[:,'ep'])     #Calculate EAD using trapezoidal approximation

