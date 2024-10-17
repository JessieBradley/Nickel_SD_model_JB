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

#%% Set working directory

os.chdir('C:/Users/jessi/Desktop/Thesis/Python') 

#%% Get world map data

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est>0) & (world.name!="Antarctica")]
world['gdp_per_cap'] = world.gdp_md_est / world.pop_est

#%% Add BAU GHG data to countries

BAU_GHG_data = pd.read_csv("SSP2-base3-GHG2.csv")
merged_BAU_GHG_data = world.merge(BAU_GHG_data, on='iso_a3')
merged_BAU_GHG_data.replace(0, np.nan, inplace=True)

#%% Add ET GHG data to countries

ET_GHG_data = pd.read_csv("SSP5-193-GHG2.csv")
merged_ET_GHG_data = world.merge(ET_GHG_data, on='iso_a3')
merged_ET_GHG_data.replace(0, np.nan, inplace=True)

#%% Test BAU figure for 2015

fig, ax = plt.subplots(1, 1)
merged_BAU_GHG_data.plot(column='2015', ax=ax, legend=True,legend_kwds={'label': "Nickel production emissions (tonne CO2eq/tonne) 2015",'orientation': "horizontal"},vmin=0,vmax=40,zorder=2)
final_plot = world.plot(color='white', edgecolor='black', ax=ax,)
final_plot.set_axis_off()
plt.title('BAU (SSP2-base)\n')
plt.savefig('GHG2BAU_2015.png')

#%% Test ET figure for 2015

fig, ax = plt.subplots(1, 1)
merged_ET_GHG_data.plot(column='2015', ax=ax, legend=True,legend_kwds={'label': "Nickel production emissions (tonne CO2eq/tonne) 2015",'orientation': "horizontal"},vmin=0,vmax=40,zorder=2)
final_plot = world.plot(color='white', edgecolor='black', ax=ax,)
final_plot.set_axis_off()
plt.title('Energy transition (SSP5-19)\n')
plt.savefig('GHG2ET_2015.png')


#%% Combine images test

imgs = ['GHG2BAU_2015.png', 'GHG2ET_2015.png']
concatenated = Image.fromarray(
  np.concatenate(
    [np.array(Image.open(x)) for x in imgs],
    axis=1
  )
)
concatenated.save('GHG2_2015.png')

#%% Make a list of the time steps

timeframe = list(merged_BAU_GHG_data)
timeframe = timeframe[9:]

#%% Create a BAU figure for each time step

def save_figs(time):    
    fig, ax = plt.subplots(1, 1)
    merged_BAU_GHG_data.plot(column=time, ax=ax, legend=True,legend_kwds={'label': "Nickel production emissions (tonne CO2eq/tonne) "+time,'orientation': "horizontal"},vmin=0,vmax=40,zorder=2)
    final_plot = world.plot(color='white', edgecolor='black', ax=ax,)
    final_plot.set_axis_off()
    plt.title('BAU (SSP2-base)\n')
    plt.savefig('GHG2BAU_{}.png'.format(time))

for time in timeframe:
    save_figs(time)
    plt.close()
    
#%% Create an ET figure for each time step

def save_figs(time):    
    fig, ax = plt.subplots(1, 1)
    merged_ET_GHG_data.plot(column=time, ax=ax, legend=True,legend_kwds={'label': "Nickel production emissions (tonne CO2eq/tonne) "+time,'orientation': "horizontal"},vmin=0,vmax=40,zorder=2)
    final_plot = world.plot(color='white', edgecolor='black', ax=ax,)
    final_plot.set_axis_off()
    plt.title('Energy transition (SSP5-19)\n')
    plt.savefig('GHG2ET_{}.png'.format(time))

for time in timeframe:
    save_figs(time)
    plt.close()

#%% Combine images

def combine_imgs(time):
    

    imgs = ['GHG2BAU_{}.png'.format(time), 'GHG2ET_{}.png'.format(time)]
    concatenated = Image.fromarray(
        np.concatenate(
            [np.array(Image.open(x)) for x in imgs],
            axis=1
            )
        )
    concatenated.save('GHG2_{}.png'.format(time))

for time in timeframe:
    combine_imgs(time)
    plt.close()


#%% Make a list of the figures

filenames = []
for time in timeframe:
    filenames.append('GHG2_{}.png'.format(time))
  

#%% Create a video of the figures. Run this separately.   

# Folder which contains all the images from which video is to be generated
os.chdir('C:/Users/jessi/Desktop/Thesis/Python/Geo_figures_GHG2')  
path = 'C:/Users/jessi/Desktop/Thesis/Python/Geo_figures_GHG2'

# Checking to see if the number of images is correct    
num_of_images = len(os.listdir('.'))
print(num_of_images)

# Video Generating function
def generate_video():
    image_folder = '.' 
    video_name = 'Dynamic_GHG2_total2.avi'
    os.chdir('C:/Users/jessi/Desktop/Thesis/Python/Geo_figures_GHG2')
      
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]
    
    # Array images should only consider the image files ignoring others if any
    print(images) 
    
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape 
    
    # The second number is the number of images per second
    video = cv2.VideoWriter(video_name, 0, 8, (width, height)) 
  
    # Appending the images to the video one by one
    for image in images: 
        video.write(cv2.imread(os.path.join(image_folder, image))) 
      
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows() 
    video.release()  # releasing the video generated

# Calling the generate_video function
generate_video()
    