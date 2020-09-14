# -*- coding: utf-8 -*-
"""
#Simple script to calculate EAD
#Author: Philip Ward (philip.ward@vu.nl)
#Date: 11th August 2017

"""

import os #package to manipulate and connect paths and files.
import numpy as np #mathematical package for fast operations on arrays.
import matplotlib.pyplot as plt #package used in the vizualisation and plotting of data
import pandas as pd #mathematical package for operations on arrays with labelled columns and indexes. Very good for time serie analysis 
#%% Define root folder, and location of input damages and return periods
root_folder = r'E:\surfdrive\Shared\Water_Risks\2019_2020\SESSION_MATERIALS\SESSION_8_Integrating_to_risk\PRACTICALS\EAD' #r: refers to the root folder you are using, this is a formatting style for python
input_file = 'ead_example_damage_input.csv'

#%% Load input file, extract damages and return periods
fn = os.path.join(root_folder, input_file) #We concatenate the two strings to make one path name
data = pd.read_csv(fn) #loading data from a csv file using the pandas package

#Make a figure to make it is all correct
plt.figure()
plt.plot(data.iloc[:,0], data.iloc[:,1], '-or') #iloc: this is a method to locate data from a dataframe by indexing over the columns, often used to avoid typos in headernames
plt.xlabel('Exc. Prob')
plt.ylabel('Damage (USD)')
plt.show()

#%% Calculate exceedance probability
data.loc[:, 'ep'] = 1/data.loc[:,'RP'] #loc: this is a method to locate data from a dataframe by using the column headers, note: this must without typos

#Calculate EAD...
ead = np.trapz(y = data.iloc[:, 1], x = data.loc[:,'ep']) #Calculate EAD using trapezoidal approximation
