#Simple script to calculate EAD
#Author: Philip Ward (philip.ward@vu.nl)
#Date: 11th August 2017

import numpy as np
import matplotlib.pyplot as plt

#Enter damages and return periods
damage = np.array([13000000,12000000,10000000,5000000,0]) #Array of damages for each return period
rp = np.array([np.inf,500,100,50,10]) #Array of return periods

# Calculate exceedance probability
ep = 1/rp; # Convert from return period to exceedance probability

#Make a figure to make it is all correct
plt.figure()
plt.plot(ep, damage, '-or')
plt.xlabel('Exc. Prob')
plt.ylabel('Damage (USD)')
plt.show()

#Calculate EAD...
ead = np.trapz(y = damage, x = ep)     #Calculate EAD using trapezoidal approximation
