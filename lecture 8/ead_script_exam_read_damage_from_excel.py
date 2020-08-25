# -*- coding: utf-8 -*-
"""
#Simple script to calculate EAD
#Author: Philip Ward (philip.ward@vu.nl)
#Date: 11th August 2017

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%% Define root folder, and location of input damages and return periods
root_folder = r'E:\surfdrive\Shared\Water_Risks\2019_2020\SESSION_MATERIALS\SESSION_8_Integrating_to_risk\PRACTICALS\EAD'
input_file = 'ead_example_damage_input.csv'

fn = os.path.join(root_folder, input_file)
#%% Load input file, extract damages and return periods
data = pd.read_csv(fn)

#Make a figure to make it is all correct
plt.figure()
plt.plot(data.iloc[:,0], data.iloc[:,1], '-or')
plt.xlabel('Exc. Prob')
plt.ylabel('Damage (USD)')
plt.show()


#%% Calculate exceedance probability
data.loc[:, 'ep'] = 1/data.loc[:,'RP']

#Calculate EAD...
ead = np.trapz(y = data.iloc[:, 1], x = data.loc[:,'ep'])     #Calculate EAD using trapezoidal approximation
