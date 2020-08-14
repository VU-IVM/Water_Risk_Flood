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
data.rename(columns = {data.columns[-1]:'Damage_usd'}, inplace = True)
data.sort_values(by='RP', ascending=True, inplace=True)

#Make a figure to make it is all correct
plt.figure()
plt.semilogx(data.loc[:,'RP'], data.loc[:,'Damage_usd'], '-or')
plt.xlabel('Return Period')
plt.ylabel('Damage (USD)')
plt.show()

#%% Define protection level
prot = 75 #Protection standard below which zero damage and above which dike fails     

#Can you work out what is happening here?
dam_prot = np.interp(prot, data.loc[:,'RP'], data.loc[:,'Damage_usd'])

data_insert = pd.DataFrame(data = np.array([[prot, dam_prot], [prot-0.0001, 0]]), columns = data.columns)
data = pd.concat([data, data_insert], axis = 0).sort_values(by='RP', ascending=True).reset_index(drop=True)
data.loc[data.loc[:,'RP']<prot, 'Damage_usd'] = 0

#%% Calculate exceedance probability
data.loc[:, 'ep'] = 1/data.loc[:,'RP']
data.sort_values(by='ep', ascending=True, inplace = True)

#Calculate EAD...
ead = np.trapz(y = data.loc[:, 'Damage_usd'], x = data.loc[:,'ep'])     #Calculate EAD using trapezoidal approximation

