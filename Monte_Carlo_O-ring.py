# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 15:59:41 2020

@author: WBurke
"""
import numpy as np
import matplotlib.pyplot as plt

n = 1000000 # number of trials

# Component specifications
sigma = 3       # assume 99.7% of components in tolerance spec
dp = 22.5 - 0.05      # piston diameter
tol_dp = 0.03   # piston diameter tolerance
do = 3          # o ring diameter
tol_do = 0.09   # o ring diameter tolerance
dc = 25         # cylinder diameter
tol_dc = 0.1    # cylinder diameter tolerance


def calculateInterference(dp, do, dc):
    """
    in: diameters
    out: o ring interference 
    """
    
    interference = dp + do - dc
    return interference

def checkInterference(interference, lower, upper):
    """
    in: o ring interference
    out: Bool, T for pass, F for fail
    """
    
    if interference < lower or interference > upper:
        return False
    else:
        return True

# set interference limits
lower = 0.3 # smallest permissable interference 
upper = 0.6 # largest permissable interference
      
interference_list = []  # initialize a list to store interference values per trial 
results = []            # initialize a list to store our trial results

# Main simulation loop
for trial in range(n):
    # Sample PDF for each component
    piston_sample = np.random.normal(dp, tol_dp/sigma)
    oring_sample = np.random.normal(do, tol_do/sigma)
    cylinder_sample = np.random.normal(dc, tol_dc/sigma)
    
    # compute and store interference 
    interference = calculateInterference(piston_sample, oring_sample, cylinder_sample)
    interference_list.append(interference)
    
    # Trial check: log results of interference check
    results.append(checkInterference(interference, lower, upper))

# results check
goodAssemblyCount = sum(results)
failurePercentage =  100*((n - goodAssemblyCount) / n)

print('Percentage of failed piston assemblies: ', failurePercentage, "%")

# Plot results

#setup histogram parameters for plotting
n_bins = 500
heights, bins, _ = plt.hist(interference_list, bins=n_bins) # get positions and heights of bars

bin_width = np.diff(bins)[0]
bin_pos = bins[:-1] + bin_width / 2

# mask for coloring failures differently
maskleft = (bin_pos <= lower)
maskright = (bin_pos >= upper)

# plot data in three steps
plt.figure(figsize=(14, 4))
plt.bar(bin_pos, heights, width=bin_width, color='#281E78', label='Good Assemblies')
plt.bar(bin_pos[maskleft], heights[maskleft], width=bin_width, color='#ea4228', label='left tail failures')
plt.bar(bin_pos[maskright], heights[maskright], width=bin_width, color='#49C6E5', label='right tail failures')

# axis labels and vertical markers of left and right tail failures
plt.xlabel("O ring interference (mm)")
plt.ylabel("# samples")
plt.axvline(lower, linestyle='--',linewidth=1, color='grey')
plt.axvline(upper, linestyle='--',linewidth=1, color='grey')

# remove upper and right spines, set ticks
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.legend()
plt.show()

        