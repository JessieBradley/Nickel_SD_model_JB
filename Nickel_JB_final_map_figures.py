# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 16:24:56 2022

@author: Jessie Bradley

"""

#%% Imports

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os
import cv2
import numpy as np
from PIL import Image

import sys
print(sys.version)

#%% Set working directory

os.chdir('C:/Users/jessi/Desktop/Thesis/Python') 

#%% Get world map data

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est>0) & (world.name!="Antarctica")]
world['gdp_per_cap'] = world.gdp_md_est / world.pop_est


#%% Change ; to , in csv if this is a problem

with open("SSP2-base_GHG.csv", "r") as f:
    data = f.read().replace(";", ",")  # Replace ; with ,

with open("SSP2-base_GHG_comma.csv", "w") as f:
    f.write(data)  # Save the fixed file
    
with open("SSP5-19_GHG.csv", "r") as f:
    data = f.read().replace(";", ",")  # Replace ; with ,

with open("SSP5-19_GHG_comma.csv", "w") as f:
    f.write(data)  # Save the fixed file

#%% Add BAU GHG data to countries

BAU_GHG_data = pd.read_csv("SSP2-base_GHG_comma.csv")
merged_BAU_GHG_data = world.merge(BAU_GHG_data, on='iso_a3')
merged_BAU_GHG_data.replace(0, np.nan, inplace=True)

#%% Add ET GHG data to countries

ET_GHG_data = pd.read_csv("SSP5-19_GHG_comma.csv")
merged_ET_GHG_data = world.merge(ET_GHG_data, on='iso_a3')
merged_ET_GHG_data.replace(0, np.nan, inplace=True)

#%% BAU figures for 2015 and 2060

fig, ax = plt.subplots(1, 1)
merged_BAU_GHG_data.plot(column='2015', ax=ax, legend=True,legend_kwds={'label': "Nickel production emissions (tonne CO2eq/tonne) 2015",'orientation': "horizontal"},vmin=0,vmax=40,zorder=2)
final_plot = world.plot(color='white', edgecolor='black', ax=ax,)
final_plot.set_axis_off()
plt.title('BAU (SSP2-base)\n')
plt.savefig('GHG_BAU_2015.png', dpi=600)

fig, ax = plt.subplots(1, 1)
merged_BAU_GHG_data.plot(column='2060', ax=ax, legend=True,legend_kwds={'label': "Nickel production emissions (tonne CO2eq/tonne) 2060",'orientation': "horizontal"},vmin=0,vmax=40,zorder=2)
final_plot = world.plot(color='white', edgecolor='black', ax=ax,)
final_plot.set_axis_off()
plt.title('BAU (SSP2-base)\n')
plt.savefig('GHG_BAU_2060.png', dpi=600)

#%% ET figures for 2015 and 2060

fig, ax = plt.subplots(1, 1)
merged_ET_GHG_data.plot(column='2015', ax=ax, legend=True,legend_kwds={'label': "Nickel production emissions (tonne CO2eq/tonne) 2015",'orientation': "horizontal"},vmin=0,vmax=40,zorder=2)
final_plot = world.plot(color='white', edgecolor='black', ax=ax,)
final_plot.set_axis_off()
plt.title('Energy transition (SSP5-19)\n')
plt.savefig('GHG_ET_2015.png', dpi=600)

fig, ax = plt.subplots(1, 1)
merged_ET_GHG_data.plot(column='2060', ax=ax, legend=True,legend_kwds={'label': "Nickel production emissions (tonne CO2eq/tonne) 2060",'orientation': "horizontal"},vmin=0,vmax=40,zorder=2)
final_plot = world.plot(color='white', edgecolor='black', ax=ax,)
final_plot.set_axis_off()
plt.title('Energy transition (SSP5-19)\n')
plt.savefig('GHG_ET_2060.png', dpi=600)
