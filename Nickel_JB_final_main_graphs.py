# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 11:36:11 2025

@author: Jessie Bradley
adapted from Erika van der Linden (2020)
"""

#%% Imports

from ema_workbench import load_results

import seaborn as sns #; sns.set(style="ticks", color_codes=True)
import numpy as np
import matplotlib.pyplot as plt
import ema_workbench
from ema_workbench.analysis.plotting import lines
from ema_workbench.analysis.plotting import envelopes
from ema_workbench.analysis.plotting_util import prepare_data
from ema_workbench.analysis import clusterer, plotting, Density

#%% Load results

results = load_results(r'C:\Users\jessi\Desktop\Thesis\Python\NickelJBfinal.tar.gz')

#%% Data preparation

#Update number of experiments based on the number done for a certain set of runs
nr_experiments = 1000

exp_b, out_b= results
labels_time = [2015, 2020, 2030, 2040, 2050, 2060]

# Determining high and low values

exp_b['High substitution threshold'] = exp_b['Substitution threshold[Batteries]'] >3.75
exp_b['High substitution threshold'] = exp_b['High substitution threshold'].astype('object')

exp_b['High maximum profit deficit as percentage of investment'] = exp_b['Average maximum profit deficit as percentage of investment'] >0.055
exp_b['High maximum profit deficit as percentage of investment'] = exp_b['High maximum profit deficit as percentage of investment'].astype('object')

exp_b['High short administration time'] = exp_b['Administration postponed demand'] >1
exp_b['High short administration time'] = exp_b['High short administration time'].astype('object')

exp_b['High power for price based exploration'] = exp_b['Power for price based exploration'] >0.7
exp_b['High power for price based exploration'] = exp_b['High power for price based exploration'].astype('object')

exp_b['High power for ore grades'] = exp_b['Power for ore grades'] >0.3
exp_b['High power for ore grades'] = exp_b['High power for ore grades'].astype('object')

exp_b['High maximum mothball time'] = exp_b['Average maximum mothball time'] >20
exp_b['High maximum mothball time'] = exp_b['High maximum mothball time'].astype('object')

exp_b['High average mine operation plan'] = exp_b['Average mine operation plan'] >15
exp_b['High average mine operation plan'] = exp_b['High average mine operation plan'].astype('object')

exp_b['High minimum profit over investment'] = exp_b['Minimum profit over investment'] >1.6
exp_b['High minimum profit over investment'] = exp_b['High minimum profit over investment'].astype('object')

exp_b['High global maximum capacity increase percentage'] = exp_b['Global maximum capacity increase percentage'] >0.10
exp_b['High global maximum capacity increase percentage'] = exp_b['High global maximum capacity increase percentage'].astype('object')

# Have second one on for main code, off for adjusted capacity

exp_b['High global maximum capacity increase percentage'] = exp_b['Global maximum capacity increase percentage'] >0.25
exp_b['High global maximum capacity increase percentage'] = exp_b['High global maximum capacity increase percentage'].astype('object')

# Combined conditions

exp_b['None'] = (
    (exp_b['High power for price based exploration'] == True) &
#    (exp_b['SSP scenario switch'].isin([1,2,3])) &
    (exp_b['SSP scenario switch'].isin([3])) &
    (exp_b['Improved EV battery lifetime switch'] == 1) &
    (exp_b['EoL management of batteries switch'].isin([1,2])) &
    (exp_b['High substitution threshold'] == True) 
#    (exp_b['Radical innovation switch'] == 1) &
#    (exp_b['Forward supply chain loss reduction switch'] == 1)
    ).astype('object')

exp_b['All'] = (
    (exp_b['High power for price based exploration'] == False) &
#    (exp_b['SSP scenario switch'].isin([1,2,3])) &
    (exp_b['SSP scenario switch'].isin([2])) &
    (exp_b['Improved EV battery lifetime switch'] == 2) &
    (exp_b['EoL management of batteries switch'].isin([3,4])) &
    (exp_b['High substitution threshold'] == False) 
#    (exp_b['Radical innovation switch'] == 2) &
#    (exp_b['Forward supply chain loss reduction switch'] == 2)
    ).astype('object')

exp_b['Supply'] = (
    (exp_b['High power for price based exploration'] == False) &
#    (exp_b['SSP scenario switch'].isin([1,2,3])) &
    (exp_b['SSP scenario switch'].isin([3])) &
    (exp_b['Improved EV battery lifetime switch'] == 1) &
    (exp_b['EoL management of batteries switch'].isin([3,4])) &
    (exp_b['High substitution threshold'] == True) 
#    (exp_b['Radical innovation switch'] == 1) &
#    (exp_b['Forward supply chain loss reduction switch'] == 2)
    ).astype('object')

exp_b['Demand'] = (
    (exp_b['High power for price based exploration'] == True) &
#    (exp_b['SSP scenario switch'].isin([1,2,3])) &
    (exp_b['SSP scenario switch'].isin([2])) &
    (exp_b['Improved EV battery lifetime switch'] == 2) &
    (exp_b['EoL management of batteries switch'].isin([1,2])) &
    (exp_b['High substitution threshold'] == False) 
#    (exp_b['Radical innovation switch'] == 2) &
#    (exp_b['Forward supply chain loss reduction switch'] == 1)
    ).astype('object')

exp_b['Mix'] = (
    (exp_b['High power for price based exploration'] == True) &
#    (exp_b['SSP scenario switch'].isin([1,2,3])) &
    (exp_b['SSP scenario switch'].isin([2])) &
    (exp_b['Improved EV battery lifetime switch'] == 2) &
    (exp_b['EoL management of batteries switch'].isin([3,4])) &
    (exp_b['High substitution threshold'] == False) 
#    (exp_b['Radical innovation switch'] == 2) &
#    (exp_b['Forward supply chain loss reduction switch'] == 1)
    ).astype('object')

exp_b['Recycling'] = (
    (exp_b['High power for price based exploration'] == True) &
#    (exp_b['SSP scenario switch'].isin([1,2,3])) &
    (exp_b['SSP scenario switch'].isin([3])) &
    (exp_b['Improved EV battery lifetime switch'] == 1) &
    (exp_b['EoL management of batteries switch'].isin([3,4])) &
    (exp_b['High substitution threshold'] == True) 
#    (exp_b['Radical innovation switch'] == 2) &
#    (exp_b['Forward supply chain loss reduction switch'] == 1)
    ).astype('object')

print(exp_b[['None']].value_counts())
print(exp_b[['All']].value_counts())
print(exp_b[['Supply']].value_counts())
print(exp_b[['Demand']].value_counts())
print(exp_b[['Mix']].value_counts())
print(exp_b[['Recycling']].value_counts())


No = exp_b[exp_b['None'] == True]
print(No.index)

All = exp_b[exp_b['All'] == True]
print(All.index)

Supply = exp_b[exp_b['Supply'] == True]
print(Supply.index)

Demand = exp_b[exp_b['Demand'] == True]
print(Demand.index)

Mix = exp_b[exp_b['Mix'] == True]
print(Mix.index)

Recycling = exp_b[exp_b['Recycling'] == True]
print(Mix.index)


# Selection
exp_b['selection'] = 0
exp_b['selection'][No.index] = 1 
exp_b['selection'][All.index] = 2
exp_b['selection'][Supply.index] = 3
exp_b['selection'][Demand.index] = 4

# Selection 2
exp_b['selection2'] = 0
exp_b['selection2'][No.index] = 1 
exp_b['selection2'][All.index] = 2
exp_b['selection2'][Supply.index] = 3
exp_b['selection2'][Demand.index] = 4
exp_b['selection2'][Mix.index] = 5


# Selection 3
exp_b['selection3'] = 0
exp_b['selection3'][No.index] = 1 
exp_b['selection3'][All.index] = 2
exp_b['selection3'][Supply.index] = 3
exp_b['selection3'][Demand.index] = 4
exp_b['selection3'][Mix.index] = 5
exp_b['selection3'][Recycling.index] = 6


# Colours based on colorbrewer 9-class Set1

Red = (228/255,26/255,28/255) 
Blue = (55/255,126/255,184/255) 
Green = (77/255,175/255,74/255) 
Purple = (152/255,78/255,163/255)
Orange = (255/255,127/255,0/255) 
Yellow = (255/255,255/255,51/255)
Brown = (166/255,86/255,40/255)
Pink = (247/255,129/255,191/255)
Gray = (153/255,153/255,153/255)

#%% Demand SSPs 

#custom_palette = [Purple, Blue, Gray, Red]
custom_palette = [Blue, Orange, Green, Red]

palette = sns.color_palette(custom_palette, n_colors=4)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

out_b['Final nickel demand'] = out_b['Sum final demand']
out_b['Final nickel demand'] = out_b['Final nickel demand']/1000000

lines(exp_b, out_b, 'Final nickel demand',group_by = 'SSP scenario switch',density=Density.VIOLIN, legend = True, titles=None ,
      grouping_specifiers= {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == Blue:
        line.set_alpha(0.125)
    if line.get_color() == Orange:
        line.set_alpha(0.1)
    if line.get_color() == Green:
        line.set_alpha(0.075)
    if line.get_color() == Red:
        line.set_alpha(0.05)
ax[0].set_ylabel('Final nickel demand (Mt/year)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_final_nickel_demand600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


#%% Demand radical innovation

#custom_palette = [Red, Blue]
custom_palette = [Blue, Orange]

palette = sns.color_palette(custom_palette, n_colors=2)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

out_b['Final nickel demand'] = out_b['Sum final demand']
out_b['Final nickel demand'] = out_b['Final nickel demand']/1000000

lines(exp_b, out_b, 'Final nickel demand',group_by = 'Radical innovation switch',density=Density.VIOLIN, legend = True, titles=None ,
      grouping_specifiers= {'No':1,'SSP2-19':2})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == Blue:
        line.set_alpha(0.1)
    if line.get_color() == Orange:
        line.set_alpha(0.05)
ax[0].set_ylabel('Final nickel demand (Mt/year)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_final_nickel_demand_2_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1, transparent=False, facecolor='white')



#%% Price SSPs

#custom_palette = [Purple, Blue, Gray, Red]
custom_palette = [Blue, Orange, Green, Red]

palette = sns.color_palette(custom_palette, n_colors=4)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

lines(exp_b, out_b, 'Average periodic nickel price',group_by = 'SSP scenario switch',density=Density.VIOLIN, legend = True, titles=None ,
      grouping_specifiers= {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == Blue:
        line.set_alpha(0.125)
    if line.get_color() == Orange:
        line.set_alpha(0.1)
    if line.get_color() == Green:
        line.set_alpha(0.075)
    if line.get_color() == Red:
        line.set_alpha(0.05)
ax[0].set_ylabel('Average periodic nickel price (2005$/tonne)')
ax[0].set_ylim(0,250000)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_price_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


#%% Price innovation

custom_palette = [Blue, Orange]

palette = sns.color_palette(custom_palette, n_colors=2)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

lines(exp_b, out_b, 'Average periodic nickel price',group_by = 'Radical innovation switch',density=Density.VIOLIN, legend = True, titles=None ,
      grouping_specifiers= {'No':1,'SSP2-19':2})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == Blue:
        line.set_alpha(0.1)
    if line.get_color() == Orange:
        line.set_alpha(0.05)
ax[0].set_ylabel('Average periodic nickel price (2005$/tonne)')
ax[0].set_ylim(0,250000)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_price_2_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)

    

#%% Recycling

#custom_palette = [Yellow, Orange, Pink, Brown]
custom_palette = [Blue, Orange, Green, Red]

palette = sns.color_palette(custom_palette, n_colors=4)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

lines(exp_b, out_b, 'Total EoL RR',group_by = 'EoL management of batteries switch',density=Density.VIOLIN, legend = True, titles=None ,
      grouping_specifiers= {'Worse':1,'Same':2,'Better':3,'SSP2-19': 4})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == Blue:
        line.set_alpha(0.125)
    if line.get_color() == Orange:
        line.set_alpha(0.1)
    if line.get_color() == Green:
        line.set_alpha(0.075)
    if line.get_color() == Red:
        line.set_alpha(0.05)
ax[0].set_ylabel('EoL recycling rate (Dmnl)')
ax[0].set_ylim(0,1)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_recycling_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


#%% Cobalt

#custom_palette = [Purple, Blue, Gray, Red]
custom_palette = [Blue, Orange, Green, Red]

palette = sns.color_palette(custom_palette, n_colors=4)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

out_b['Cumulative mined cobalt 2'] = out_b['Cumulative mined cobalt']
out_b['Cumulative mined cobalt 2'] = out_b['Cumulative mined cobalt 2']/1000000

logical = out_b['Cumulative mined cobalt 2'][:,-1] > 0
exp_in = exp_b[logical]
out_in = {k:v[logical] for k,v in out_b.items()}

lines(exp_in, out_in, 'Cumulative mined cobalt 2',group_by = 'SSP scenario switch',density=Density.VIOLIN, legend = True, titles=None ,
      grouping_specifiers= {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == Blue:
        line.set_alpha(0.125)
    if line.get_color() == Orange:
        line.set_alpha(0.1)
    if line.get_color() == Green:
        line.set_alpha(0.075)
    if line.get_color() == Red:
        line.set_alpha(0.05)
ax[0].set_ylabel('Cumulative mined cobalt (Mt)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_cobalt_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)



#%% Ore grade

#custom_palette = [Purple, Blue, Gray, Red]
custom_palette = [Blue, Orange, Green, Red]

palette = sns.color_palette(custom_palette, n_colors=4)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

out_b['Average ore grade of existing mines'] = out_b['Overall average nickel ore grade of existing mines']
lines(exp_b, out_b, 'Average ore grade of existing mines',group_by = 'SSP scenario switch', density=Density.VIOLIN , legend = True, titles=None  ,
      grouping_specifiers= {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == Blue:
        line.set_alpha(0.125)
    if line.get_color() == Orange:
        line.set_alpha(0.1)
    if line.get_color() == Green:
        line.set_alpha(0.075)
    if line.get_color() == Red:
        line.set_alpha(0.05)
ax[0].set_ylabel('Average ore grade of existing mines (Dmnl)')
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_og_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


#%% GHG emissions

#custom_palette = [Purple, Blue, Gray, Red]
custom_palette = [Blue, Orange, Green, Red]

palette = sns.color_palette(custom_palette, n_colors=4)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

out_b['Cumulative GHG emissions'] = out_b['Total cumulative GHG emissions']
out_b['Cumulative GHG emissions'] = out_b['Cumulative GHG emissions']/1000000
lines(exp_b, out_b, 'Cumulative GHG emissions',group_by = 'SSP scenario switch', density=Density.VIOLIN , legend = True, titles=None  ,
      grouping_specifiers= {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == Blue:
        line.set_alpha(0.125)
    if line.get_color() == Orange:
        line.set_alpha(0.1)
    if line.get_color() == Green:
        line.set_alpha(0.075)
    if line.get_color() == Red:
        line.set_alpha(0.05)
ax[0].set_ylabel('Cumulative GHG emissions (Mt CO2eq)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_ghg_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


  
#%% Policy combinations

custom_palette = [(1, 1, 1), Green, Blue, Red, Orange]

palette = sns.color_palette(custom_palette, n_colors=5)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

out_b['Final nickel demand'] = out_b['Sum final demand']
out_b['Final nickel demand'] = out_b['Final nickel demand']/1000000
lines(exp_b, out_b, 'Final nickel demand',group_by = 'selection',density=Density.VIOLIN, legend = True, titles=None ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
ax[0].set_ylabel('Final nickel demand (Mt/year)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_final_nickel_demand_policies_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


lines(exp_b, out_b, 'Average periodic nickel price',group_by = 'selection', density=Density.VIOLIN, legend = True, titles=None  ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
ax[0].set_ylabel('Average periodic nickel price (2005$/tonne)')
ax[0].set_ylim(0,250000)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_price_policies_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


out_b['Cumulative GHG emissions'] = out_b['Total cumulative GHG emissions']
out_b['Cumulative GHG emissions'] = out_b['Cumulative GHG emissions']/1000000
lines(exp_b, out_b, 'Cumulative GHG emissions',group_by = 'selection', density=Density.VIOLIN , legend = True, titles=None  ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
ax[0].set_ylabel('Cumulative GHG emissions (Mt CO2eq)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_ghg_policies_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


out_b['Average ore grade of existing mines'] = out_b['Overall average nickel ore grade of existing mines']
lines(exp_b, out_b, 'Average ore grade of existing mines',group_by = 'selection', density=Density.VIOLIN , legend = True, titles=None  ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
ax[0].set_ylabel('Average ore grade of existing mines (Dmnl)')
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_og_policies_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


#%% Policy combinations 2 (check for impact of all - exploration)

custom_palette = [(1, 1, 1), Green, Purple, Blue, Red, Orange]

palette = sns.color_palette(custom_palette, n_colors=6)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

out_b['Final nickel demand'] = out_b['Sum final demand']
out_b['Final nickel demand'] = out_b['Final nickel demand']/1000000
lines(exp_b, out_b, 'Final nickel demand',group_by = 'selection2',density=Density.VIOLIN, legend = True, titles=None ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4, 'Demand + Recycling':5})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
    if line.get_color() == Purple:
        line.set_alpha(0.5)
ax[0].set_ylabel('Final nickel demand (Mt/year)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_final_nickel_demand_policies2_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


lines(exp_b, out_b, 'Average periodic nickel price',group_by = 'selection2', density=Density.VIOLIN, legend = True, titles=None  ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4, 'Demand + Recycling':5} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
    if line.get_color() == Purple:
        line.set_alpha(0.5)
ax[0].set_ylabel('Average periodic nickel price (2005$/tonne)')
ax[0].set_ylim(0,250000)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_price_policies2_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


out_b['Cumulative GHG emissions'] = out_b['Total cumulative GHG emissions']
out_b['Cumulative GHG emissions'] = out_b['Cumulative GHG emissions']/1000000
lines(exp_b, out_b, 'Cumulative GHG emissions',group_by = 'selection2', density=Density.VIOLIN , legend = True, titles=None  ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4, 'Demand + Recycling':5} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
    if line.get_color() == Purple:
        line.set_alpha(0.5)
ax[0].set_ylabel('Cumulative GHG emissions (Mt CO2eq)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_ghg_policies2_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


out_b['Average ore grade of existing mines'] = out_b['Overall average nickel ore grade of existing mines']
lines(exp_b, out_b, 'Average ore grade of existing mines',group_by = 'selection2', density=Density.VIOLIN , legend = True, titles=None  ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4, 'Demand + Recycling':5} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
    if line.get_color() == Purple:
        line.set_alpha(0.5)
ax[0].set_ylabel('Average ore grade of existing mines (Dmnl)')
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_og_policies2_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)

#%% Policy combinations 3 (check for impact of only recycling)

custom_palette = [(1, 1, 1), Green, Purple, Blue, Red, Pink, Orange]

palette = sns.color_palette(custom_palette, n_colors=7)
ema_workbench.analysis.plotting_util.COLOR_LIST = palette
sns.set_palette(palette)

out_b['Final nickel demand'] = out_b['Sum final demand']
out_b['Final nickel demand'] = out_b['Final nickel demand']/1000000
lines(exp_b, out_b, 'Final nickel demand',group_by = 'selection3',density=Density.VIOLIN, legend = True, titles=None ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4, 'Demand + recycling':5, 'Recycling':6})
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
    if line.get_color() == Purple:
        line.set_alpha(0.5)
    if line.get_color() == Pink:
        line.set_alpha(0.5)
ax[0].set_ylabel('Final nickel demand (Mt/year)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_final_nickel_demand_policies3_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


lines(exp_b, out_b, 'Average periodic nickel price',group_by = 'selection3', density=Density.VIOLIN, legend = True, titles=None  ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4, 'Demand + recycling':5, 'Recycling':6} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
    if line.get_color() == Purple:
        line.set_alpha(0.5)
    if line.get_color() == Pink:
        line.set_alpha(0.5)
ax[0].set_ylabel('Average periodic nickel price (2005$/tonne)')
ax[0].set_ylim(0,250000)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_price_policies3_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


out_b['Cumulative GHG emissions'] = out_b['Total cumulative GHG emissions']
out_b['Cumulative GHG emissions'] = out_b['Cumulative GHG emissions']/1000000
lines(exp_b, out_b, 'Cumulative GHG emissions',group_by = 'selection3', density=Density.VIOLIN , legend = True, titles=None  ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4, 'Demand + recycling':5, 'Recycling':6} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
    if line.get_color() == Purple:
        line.set_alpha(0.5)
    if line.get_color() == Pink:
        line.set_alpha(0.5)
ax[0].set_ylabel('Cumulative GHG emissions (Mt CO2eq)')
ax[0].set_ylim(0,)
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_ghg_policies3_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)


out_b['Average ore grade of existing mines'] = out_b['Overall average nickel ore grade of existing mines']
lines(exp_b, out_b, 'Average ore grade of existing mines',group_by = 'selection3', density=Density.VIOLIN , legend = True, titles=None  ,
      grouping_specifiers= {'None': 1, 'All':2, '':0, 'Supply-side': 3, 'Demand-side':4, 'Demand + recycling':5, 'Recycling':6} )
fig = plt.gcf()
ax = fig.get_axes()
fig.set_size_inches(6,3)
#find_colors(ax[0])
for line in ax[0].get_lines():
    if line.get_color() == (1, 1, 1):
        line.set_alpha(0)
    if line.get_color() == Green:
        line.set_alpha(1)
    if line.get_color() == Blue:
        line.set_alpha(0.5)
    if line.get_color() == Red:
        line.set_alpha(0.5)
    if line.get_color() == Orange:
        line.set_alpha(0.5)
    if line.get_color() == Purple:
        line.set_alpha(0.5)
    if line.get_color() == Pink:
        line.set_alpha(0.5)
ax[0].set_ylabel('Average ore grade of existing mines (Dmnl)')
ax[0].set_xlim(2015,2060)
sns.despine()
fig.savefig('0_nickel_og_policies3_600dpi.png', dpi=600, bbox_inches='tight', pad_inches=0.1)