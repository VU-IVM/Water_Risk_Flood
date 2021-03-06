#Simple script to calculate EAD
#Author: Philip Ward (philip.ward@vu.nl)
#Date: 11th August 2017

import numpy as np #mathematical package for fast operations on arrays.
import matplotlib.pyplot as plt #package used in the vizualisation and plotting of data 

#Enter damages and return periods
damage = np.array([13000000,12000000,10000000,5000000,0]) #Array of damages for each return period
rp = np.array([np.inf,500,100,50,10]) #Array of return periods

# Calculate exceedance probability
ep = 1/rp; #Conversion: from return period to exceedance probability

#Make a figure to make it is all correct
plt.figure() #create a new figure
plt.plot(ep, damage, '-or') #plotting the exceedance probability vs. the damage
plt.xlabel('Exc. Prob') #adding a x-label to the graph
plt.ylabel('Damage (USD)') #adding a y-label to the graph
plt.show() #finish the figure

#Calculate EAD...
ead = np.trapz(y = damage, x = ep) #Calculate EAD using trapezoidal approximation
