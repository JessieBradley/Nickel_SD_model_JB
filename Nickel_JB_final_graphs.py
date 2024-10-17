# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 23:12:47 2020

@author: Jessie Bradley
adapted from Erika van der Linden (2020)
"""

#%% Imports

from ema_workbench import load_results

import seaborn as sns #; sns.set(style="ticks", color_codes=True)

import matplotlib.pyplot as plt
from ema_workbench.analysis.plotting import lines
from ema_workbench.analysis.plotting_util import prepare_data
from ema_workbench.analysis import clusterer, plotting, Density

#%% Load results

results = load_results(r'C:\Users\jessi\Desktop\Thesis\Python\NickelJBfinal.tar.gz')

#%% Data preparation

#Update number of experiments based on the number done for a certain set of runs
nr_experiments = 1000

exp_b, out_b= results
 
exp_b['Paradigm switch'] = None

exp_b['Paradigm switch'][exp_b['Paradigm switch'] == 1] ='Fixed stock'
exp_b['Paradigm switch'][exp_b['Paradigm switch'] == 2] ='Opportunity cost'

exp_fs = None
exp_oc = None
out_fs = {}
out_oc = {}
for i in out_b:
    out_fs[i] = out_b[i][:nr_experiments]
    out_oc[i] = out_b[i][nr_experiments:]
exp_fs = exp_b[:nr_experiments]
exp_oc = exp_b[nr_experiments:]
results_fs = exp_fs, out_fs
results_oc = exp_oc, out_oc

#labels_time = [2000, 2010, 2020, 2030, 2040, 2050]
labels_time = [2015, 2020, 2030, 2040, 2050, 2060]
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.rcParams['legend.frameon'] = False

#Added stuff
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



#%% Defining functions

def clustering (paradigm, column, nr_of_clusters):
    if paradigm == 'fs':
        dataset=out_fs
        expdata=exp_fs
    elif paradigm == 'oc':
        dataset=out_oc
        expdata=exp_oc
    else:
        dataset = out_b
        expdata = exp_b
    data = dataset[column]
    distances = clusterer.calculate_cid(data)

# calcuate distances
    distances = clusterer.calculate_cid(data)
# do agglomerative clustering on the distances
    clusters = clusterer.apply_agglomerative_clustering(distances,n_clusters=nr_of_clusters)
# show the clusters in the output space
    x = expdata.copy()
    x['clusters'] = clusters.astype('object')
    return (x)

def plot_clusters (paradigm,column,x, zero = False,ylabel = False):
    if paradigm == 'fs':
        dataset=out_fs
        expdata=exp_fs
    elif paradigm == 'oc':
        dataset=out_oc
        expdata=exp_oc
    else:
        dataset = out_b#smaller_out_b
        expdata = exp_b#smaller_exp_b
#plot the clusters
    lines(x, dataset,group_by = 'Clusters',outcomes_to_show = column,density=Density.KDE)
    fig = plt.gcf()
    ax = fig.get_axes()
    ax[0].set_xticklabels(labels_time)
    fig.set_size_inches(7,5)
# plt.yscale('log')
#layout
    plt.margins(0)
    sns.despine()
    if zero == True:
        ax[0].set_ylim([0,None])
        ax[0].set_xticklabels(labels_time)
    if ylabel:
        ax[0].set(ylabel=ylabel)
    change_fontsize(fig)
    sns.despine()
# save_fig(fig,wd,'clustering'+paradigm+column)
    return fig,ax

def plot_one_cluster(paradigm, column, clusternr, x, zero=False):
    if paradigm == 'fs':
        dataset=out_fs
        expdata=exp_fs
    elif paradigm == 'oc':
        dataset=out_oc
        expdata=exp_oc
    else:
        dataset = out_b
        expdata = exp_b
    data2 = prepare_data(x,out_oc, outcomes_to_show = column,group_by ='clusters')
#plot the clusters
    lines(x, data2[0][clusternr], outcomes_to_show = column,density=Density.KDE)
    fig = plt.gcf()
    ax = fig.get_axes()
    ax[0].set_xticklabels(labels_time)
    fig.set_size_inches(13,7)
    if zero == True:
        ax[0].set_ylim([0,None])
    plt.show()

def change_fontsize(fig, fs=11.5):
    '''Change fontsize of figure items to specified size'''
    for ax in fig.axes:
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(fs)
        try:
            parasites = ax.parasites
        except AttributeError:
            pass
        else:
            for parisite in parasites:
                for axis in parisite.axis.values():
                    axis.major_ticklabels.set_fontsize(fs)
                    axis.label.set_fontsize(fs)
            for axis in ax.axis.values():
                axis.major_ticklabels.set_fontsize(fs)
                axis.label.set_fontsize(fs)
        if ax.legend_ != None:
            for entry in ax.legend_.get_texts():
                entry.set_fontsize(fs)
        for entry in ax.texts:
            entry.set_fontsize(fs)
        for entry in ax.tables:
            entry.set_fontsize(fs)

def nice_lines (exp,out,out_to_show,group_by= None,density=None,title=None, \
                exp_to_show = None,grouping_specifiers = None,legend = True, \
                paradigm = '',convert_to_t = False,convert_to_kt = False, \
                convert_to_Mt = False,zero = False ,yupperlim = None, \
                ylabel = False, alpha = None, sizex = None, sizey = None, \
                save_filename=None, dpi=600):
#Unit conversion applied when running the model by Van der Linden (2020)
    if convert_to_t == True:
        out[title] = out[out_to_show]/2204.622620
        lines(experiments = exp, outcomes = out,
              experiments_to_show = exp_to_show,
              outcomes_to_show = title, legend = legend,
              group_by = group_by, density = density,
              grouping_specifiers = grouping_specifiers)
    else:
        out[title] = out[out_to_show]
        lines(experiments = exp, outcomes = out, \
          experiments_to_show = exp_to_show, \
          outcomes_to_show = title,legend = legend, \
          group_by = group_by, density = density, \
          grouping_specifiers = grouping_specifiers)
    fig = plt.gcf()
    fig.set_size_inches(6,3)
    if sizex:
        fig.set_size_inches(sizex,sizey)
    ax = fig.get_axes()
    if zero == True:
        ax[0].set_ylim([0,yupperlim])
    ax[0].set_xticklabels(labels_time)
    if ylabel:
        ax[0].set(ylabel=ylabel)
    if alpha:
        for line in ax[0].get_lines():
            line.set_alpha(alpha)
    short_title = title.replace(" ","")
    change_fontsize(fig)
    sns.despine()
    #save_fig(fig,wd,paradigm+short_title)
    #fig.savefig(wd+paradigm+short_title+'.jpg')
#Only turn on ylim for specific plots with extreme values.    
    #plt.ylim(0,500000)
    # Save the figure if a filename is provided
    if save_filename:
        fig.savefig(save_filename, dpi=dpi, bbox_inches='tight', pad_inches=0.1)  # Use tight bounding box
        print(f"Figure saved as: {save_filename}")  # Confirmation message
    plt.show()


#%% Plotting (figure N1)

# The following lines require input from the runs including the hydrogen scenario

#nice_lines(exp_b,out_b,out_to_show = 'Sum final demand', \
#           group_by = 'Transport scenario switch', density = Density.KDE, \
#           grouping_specifiers = {'Electrification':1,'Hydrogen':2}, \
#           title= 'Final nickel demand', ylabel = '(tonne/year)', \
#           zero = True, alpha = 0.05)    
    
#nice_lines(exp_b,out_b,out_to_show = 'Sum substitution', \
#           group_by = 'Transport scenario switch', density = Density.KDE, \
#           grouping_specifiers = {'Electrification':1,'Hydrogen':2}, \
#           title= 'Total substitution', ylabel = '(tonne/year)', \
#           zero = True, alpha = 0.05)  

#%% Plotting (figure 3.1)

nice_lines(exp_b,out_b,out_to_show = 'Sum final demand', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Final nickel demand', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05, save_filename='final_nickel_demand_600dpi.png')
    
nice_lines(exp_b,out_b,out_to_show = 'Sum final demand', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP2-base':4}, \
           title= 'Final nickel demand', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative final demand', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Cumulative final demand', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)    

#%% Plotting  (figure 3.2)
 
nice_lines(exp_b,out_b,out_to_show = 'Sum total functional nickel demand', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Total functional nickel demand', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Sum substitution', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Total substitution', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)    

#%% Plotting  (figure N2)

nice_lines(exp_b,out_b,out_to_show = 'Sum demand change due to price elasticity', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Demand change due to price elast.', ylabel = '(tonne/year)', \
           alpha = 0.05)   
    
nice_lines(exp_b,out_b,out_to_show = 'Substitution[Batteries]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Substitution of batteries', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)    

#%% Plotting  (figure N3)
 
nice_lines(exp_b,out_b,out_to_show = 'Demand request', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Demand request OCP', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Postponed demand', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Postponed demand OCP', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
# The following lines require input from the FSP
 
nice_lines(exp_b,out_b,out_to_show = 'Demand request', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Demand request FSP', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Postponed demand', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Postponed demand FSP', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
      
#%% Plotting (figure 3.3)

nice_lines(exp_b,out_b,out_to_show = 'Total nickel demand for vehicle batteries[Batteries]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Nickel demand for vehicle batteries', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
  
nice_lines(exp_b,out_b,out_to_show = 'Sum demand RoE', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Nickel demand for the RoE', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)

#%% Plotting (figure N4)

nice_lines(exp_b,out_b,out_to_show = 'Nickel demand for electricity generation[Stainless steel]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Nickel demand for electr. generation', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Nickel demand for stationary batteries[Batteries]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Nickel demand for stationary batteries', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
      
#%% Plotting  (figure N5)
 
nice_lines(exp_b,out_b,out_to_show = 'Sum final demand', \
           group_by = 'Switch flexibility measures', density = Density.KDE, \
           grouping_specifiers = {'Low':1,'Mid':2,'High':3}, \
           title= 'Final nickel demand', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Nickel demand for stationary batteries[Batteries]', \
           group_by = 'Switch flexibility measures', density = Density.KDE, \
           grouping_specifiers = {'Low':1,'Mid':2,'High':3}, \
           title= 'Nickel demand for stationary batteries', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Nickel demand for stationary batteries[Batteries]', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Nickel demand for stationary batteries', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)

#%% Plotting  (figure 3.5)
 
nice_lines(exp_b,out_b,out_to_show = 'Sum processing', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Primary nickel processing', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Sum mining', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Nickel mining', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Sum mining', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP5-19':3}, \
           title= 'Nickel mining', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)  

nice_lines(exp_b,out_b,out_to_show = 'Sum mining', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP2-base':4}, \
           title= 'Nickel mining', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)        
    
nice_lines(exp_b,out_b,out_to_show = 'Final nickel availability', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Final nickel availability', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05, yupperlim=200000000)
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Resilience', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 

#%% Plotting  (figure 3.6)
 
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined cobalt', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Cumulative mined cobalt', ylabel = '(tonne)', \
           zero = True, alpha = 0.05, save_filename='cobalt_600dpi.png')    
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined palladium', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Cumulative mined palladium', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)   
    
#%% Plotting  Additional

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined cobalt', \
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title= 'Cumulative mined cobalt', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined palladium', \
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title= 'Cumulative mined palladium', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)   
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined cobalt', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'Cumulative mined cobalt', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined palladium', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'Cumulative mined palladium', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined cobalt', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Cumulative mined cobalt', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined palladium', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Cumulative mined palladium', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined cobalt', \
           group_by = 'High power for ore grades', density = Density.KDE,
           grouping_specifiers = {'low power ore.':0, 'High power ore.':1},
           title= 'Cumulative mined cobalt', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined palladium', \
           group_by = 'High power for ore grades', density = Density.KDE,
           grouping_specifiers = {'low power ore.':0, 'High power ore.':1},
           title= 'Cumulative mined palladium', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)   
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined cobalt', \
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Cumulative mined cobalt', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative mined palladium', \
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Cumulative mined palladium', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)   
    
#%% Plotting  (figure 3.7)

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, save_filename='nickel_price_600dpi.png')    
    
nice_lines(exp_b,out_b,out_to_show = 'Degree of nickel scarcity', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Degree of nickel scarcity', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Average marginal cost nickel', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average nickel marginal costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=5000) 

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000, save_filename='nickel_price_b_600dpi.png') 

#%% Plotting  (figure N10)
 
nice_lines(exp_b,out_b,out_to_show = 'Average nickel royalties', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average nickel royalties', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Reagents and other marginal costs', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Reagents and other marginal costs', ylabel = '(2005$/tonne)', \
           alpha = 0.05)    

#%% Plotting  (figure N11)
 
nice_lines(exp_b,out_b,out_to_show = 'Average credits for by products', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average credits for by-products', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Average marginal cost deposits', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average marginal cost deposits', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)    

nice_lines(exp_b,out_b,out_to_show = 'Average credits for by products', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average credits for by-products', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=100000)    
    
nice_lines(exp_b,out_b,out_to_show = 'Average marginal cost deposits', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average marginal cost deposits', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=100000)  
    
#%% Plotting  (figure 3.8)
 
nice_lines(exp_b,out_b,out_to_show = 'Total average energy costs', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average energy costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Total average energy costs', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average energy costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=8000)    

nice_lines(exp_b,out_b,out_to_show = 'Average total final energy use', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average final energy use', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Average total final energy use', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average final energy use', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05, yupperlim=655)      
    
#%% Plotting  additional

nice_lines(exp_b,out_b,out_to_show = 'Total average energy costs', \
           group_by = 'High power for ore grades', density = Density.KDE,
           grouping_specifiers = {'low power ore.':0, 'High power ore.':1},
           title= 'Average energy costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Total average energy costs', \
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Average energy costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Total average energy costs', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average energy costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Average total final energy use', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average final energy use', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Average total final energy use', \
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Average final energy use', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'High power for ore grades', density = Density.KDE,
           grouping_specifiers = {'low power ore.':0, 'High power ore.':1},
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 

    
#%% Plotting  (figure N12)
 
nice_lines(exp_b,out_b,out_to_show = 'Average final energy use mining', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average final energy use mining', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Average final energy use mining', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average final energy use mining', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05, yupperlim=600)    
       
nice_lines(exp_b,out_b,out_to_show = 'Average final energy use processing', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average final energy use processing', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05)      
    
#%% Plotting  (figure N13)
 
nice_lines(exp_b,out_b,out_to_show = 'Average energy costs mining', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average energy costs mining', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)      
    
nice_lines(exp_b,out_b,out_to_show = 'Average energy costs processing and refining', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average energy costs processing and refining', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Average energy costs mining', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average energy costs mining', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=5000)           

nice_lines(exp_b,out_b,out_to_show = 'Average energy costs processing and refining', \
           group_by = 'Switch price scenario', density = Density.KDE, \
           grouping_specifiers = {'Low':1,'Mid':2,'High':3}, \
           title= 'Average energy costs processing and refining', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)     
    
nice_lines(exp_b,out_b,out_to_show = 'Average energy costs processing and refining', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average energy costs processing and refining', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)       

#%% Plotting  (figure N14)    
    
nice_lines(exp_b,out_b,out_to_show = 'Sum final energy use in GJ', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Total final energy use', ylabel = '(GJ/year)', \
           zero = True, alpha = 0.05)      
    
nice_lines(exp_b,out_b,out_to_show = 'Sum final energy use in GJ', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Total final energy use', ylabel = '(GJ/year)', \
           zero = True, alpha = 0.05, yupperlim=5000000000)       
    
nice_lines(exp_b,out_b,out_to_show = 'Sum final energy use in GJ', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Total final energy use', ylabel = '(GJ/year)', \
           zero = True, alpha = 0.05, yupperlim=1000000)     
    
nice_lines(exp_b,out_b,out_to_show = 'Total GHG emissions', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Total GHG emissions', ylabel = '(tonne CO2eq/year)', \
           zero = True, alpha = 0.05)      
    
nice_lines(exp_b,out_b,out_to_show = 'Total GHG emissions', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Total GHG emissions', ylabel = '(tonne CO2eq/year)', \
           zero = True, alpha = 0.05, yupperlim=300000000)
    
nice_lines(exp_b,out_b,out_to_show = 'Total GHG emissions', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Total GHG emissions', ylabel = '(tonne CO2eq/year)', \
           zero = True, alpha = 0.05, yupperlim=100000) 
    
#%% Plotting  (figure N15)
 
nice_lines(exp_b,out_b,out_to_show = 'Fraction of mines per mine type[OC]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Fraction of OC mines', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Fraction of mines per ore type[Laterite]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Fraction of laterite mines', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)    

#%% Plotting  (figure 3.9)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05, save_filename='nickel_ore_grade_600dpi.png')    
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05) 
    
#%% Plotting  (figure 3.10)
 
nice_lines(exp_b,out_b,out_to_show = 'Average electricity price', \
           group_by = 'Switch price scenario', density = Density.KDE, \
           grouping_specifiers = {'Low':1,'Mid':2,'High':3}, \
           title= 'Average electricity price', ylabel = '(2005$/GJ)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Average electricity price', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average electricity price', ylabel = '(2005$/GJ)', \
           zero = True, alpha = 0.05)  
    
#%% Plotting  (figure 3.11)
 
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative GHG emissions', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Cumulative GHG emissions', ylabel = '(tonne CO2eq)', \
           zero = True, alpha = 0.05, save_filename='nickel_emissions_600dpi.png')    
    
nice_lines(exp_b,out_b,out_to_show = 'Average carbon costs', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average carbon costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 
    

#%% Plotting  (figure 3.12)
 
nice_lines(exp_b,out_b,out_to_show = 'Sum final demand', \
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title= 'Final nickel demand', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05, save_filename='final_nickel_demand_2_600dpi.png') 

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, save_filename='nickel_price_2_600dpi.png') 
    
nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, save_filename='nickel_price_2b_600dpi.png') 

nice_lines(exp_b,out_b,out_to_show = 'Substitution[Batteries]', \
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title= 'Substitution of batteries', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05) 
       
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative GHG emissions', \
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title= 'Cumulative GHG emissions', ylabel = '(tonne CO2eq)', \
           zero = True, alpha = 0.05)  
      
#%% Plotting  (figure N16)

nice_lines(exp_b,out_b,out_to_show = 'Cumulative final demand', \
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title= 'Cumulative final demand', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)  
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
  
#%% Plotting  (figure 3.13)

# The following lines require input from the FSP    

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average periodic nickel price FSP', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)  
    
nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average periodic nickel price FSP', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=500000)    
    
nice_lines(exp_b,out_b,out_to_show = 'Degree of nickel scarcity', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Degree of nickel scarcity FSP', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
#%% Plotting  (figure N17) 

# The following lines require input from the FSP

nice_lines(exp_b,out_b,out_to_show = 'Sum mining', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Nickel mining FSP', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)    

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Cumulative mined nickel FSP', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05) 
    
#%% Plotting  (figure 3.14a)
 
nice_lines(exp_b,out_b,out_to_show = 'R over P ratio', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'R/P ratio OCP', ylabel = '(year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'R over P ratio', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'R/P ratio OCP', ylabel = '(year)', \
           zero = True, alpha = 0.05, yupperlim=100)  

nice_lines(exp_b,out_b,out_to_show = 'Depletion of oringinal resources', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Depletion of original resources OCP', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)  

#%% Plotting  (figure 3.14b)    

# The following lines require input from the FSP

nice_lines(exp_b,out_b,out_to_show = 'R over P ratio', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'R/P ratio FSP', ylabel = '(year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'R over P ratio', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'R/P ratio FSP', ylabel = '(year)', \
           zero = True, alpha = 0.05, yupperlim=100)  

nice_lines(exp_b,out_b,out_to_show = 'Depletion of oringinal resources', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Depletion of original resources FSP', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)   

    
#%% Plotting  (figure 3.15)

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Supply disruption switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Supply disruption':2}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Supply disruption switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Supply disruption':2}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=120000) 

nice_lines(exp_b,out_b,out_to_show = 'Sum processing', \
           group_by = 'Supply disruption switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Supply disruption':2}, \
           title= 'Primary nickel processing', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)  

nice_lines(exp_b,out_b,out_to_show = 'Recycling input rate', \
           group_by = 'Supply disruption switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Supply disruption':2}, \
           title= 'Recycling input rate', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Total operating mining capacity utilisation', \
           group_by = 'Supply disruption switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Supply disruption':2}, \
           title= 'Total operating mining capacity utilisation', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)             
    
nice_lines(exp_b,out_b,out_to_show = 'Degree of nickel scarcity', \
           group_by = 'Supply disruption switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Supply disruption':2}, \
           title= 'Degree of nickel scarcity', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)   

    
#%% Plotting  (figure 3.16)

nice_lines(exp_b,out_b,out_to_show = 'Total EoL RR', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'EoL recycling rate', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05, yupperlim=1, save_filename='nickel_recycling_600dpi.png') 
    
nice_lines(exp_b,out_b,out_to_show = 'Total EoL RR', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'EoL recycling rate', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05, yupperlim=1)  
    
#%% Plotting  (figure 3.17)

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)  

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000)     
    
#%% Plotting  (figure N19)
    
nice_lines(exp_b,out_b,out_to_show = 'Recycling input rate', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'Recycling input rate', ylabel = '(Dmnl)', \
           alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Sum processing', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'Primary nickel processing', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)  

#%% Plotting  (figure N20)
    
nice_lines(exp_b,out_b,out_to_show = 'Sum recycling', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Total recycling', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)         
    
nice_lines(exp_b,out_b,out_to_show = 'Sum recycling', \
           group_by = 'EoL management of batteries switch', density = Density.KDE, \
           grouping_specifiers = {'Worse':1,'Same':2,'Better':3,'Improved': 4}, \
           title= 'Total recycling', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05) 
     
#%% Plotting  (figure 3.18)

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative GHG emissions', \
           group_by = 'Forward supply chain loss reduction switch', density = Density.KDE, \
           grouping_specifiers = {'No reduction':1,'Loss reduction':2}, \
           title= 'Cumulative GHG emissions', ylabel = '(tonne CO2eq)', \
           zero = True, alpha = 0.05)  

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'Forward supply chain loss reduction switch', density = Density.KDE, \
           grouping_specifiers = {'No reduction':1,'Loss reduction':2}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)

#%% Plotting  (figure 3.19)   
  
nice_lines(exp_b,out_b,out_to_show = 'Cumulative final demand', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Cumulative final demand', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)  
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Total EoL RR', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, 
           title= 'EoL recycling rate', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05, yupperlim=1)     
    
nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000)       
    
#%% Plotting  (figure N21)    
    
nice_lines(exp_b,out_b,out_to_show = 'Sum final demand', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Final nickel demand', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Total nickel demand for vehicle batteries[Batteries]', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Nickel demand for vehicle batteries', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative GHG emissions', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Cumulative GHG emissions', ylabel = '(tonne CO2eq)', \
           zero = True, alpha = 0.05)  
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05)  
    
nice_lines(exp_b,out_b,out_to_show = 'Sum substitution', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Total substitution', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05) 

#%% Plotting  (figure 3.20)

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000)   

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative GHG emissions', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Cumulative GHG emissions', ylabel = '(tonne CO2eq)', \
           zero = True, alpha = 0.05)  

nice_lines(exp_b,out_b,out_to_show = 'Average marginal cost nickel', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average nickel marginal costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Average total final energy use', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average final energy use', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05) 
   
#%% Plotting  (figure N22)

nice_lines(exp_b,out_b,out_to_show = 'Average carbon costs', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average carbon costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Total average energy costs', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average energy costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)  
       
#%% Plotting  (figure 3.21)

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000)   
    
nice_lines(exp_b,out_b,out_to_show = 'Average marginal cost nickel', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average nickel marginal costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative GHG emissions', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Cumulative GHG emissions', ylabel = '(tonne CO2eq)', \
           zero = True, alpha = 0.05)  
    
nice_lines(exp_b,out_b,out_to_show = 'Fraction of mines per ore type[Laterite]', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Fraction of laterite mines', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05)

#%% Plotting  (figure N23)    

nice_lines(exp_b,out_b,out_to_show = 'Total average energy costs', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average energy costs', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05)    

nice_lines(exp_b,out_b,out_to_show = 'Average total final energy use', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average final energy use', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Degree of nickel scarcity', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Degree of nickel scarcity', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 
   
#%% Plotting  (figure N24)    

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000)   
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)  
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Degree of nickel scarcity', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Degree of nickel scarcity', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Total operating mining capacity utilisation', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Total operating mining capacity utilisation', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Total operating mining capacity utilisation', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Mining resources':2}, \
           title= 'Total operating mining capacity utilisation', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
#%% Plotting  (figure N25)      
    
nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Switch mining energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass':1,'Price':2,'ERC':3}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000)   
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'Switch mining energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass':1,'Price':2,'ERC':3}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Switch mining energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass':1,'Price':2,'ERC':3}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative GHG emissions', \
           group_by = 'Switch mining energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass':1,'Price':2,'ERC':3}, \
           title= 'Cumulative GHG emissions', ylabel = '(tonne CO2eq)', \
           zero = True, alpha = 0.05)  

#%% Plotting  (figure N26)       

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'Switch price method', density = Density.KDE, \
           grouping_specifiers = {'Days in stock':1,'A&C':2}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000)   
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'Switch price method', density = Density.KDE, \
           grouping_specifiers = {'Days in stock':1,'A&C':2}, \
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Switch price method', density = Density.KDE, \
           grouping_specifiers = {'Days in stock':1,'A&C':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative GHG emissions', \
           group_by = 'Switch price method', density = Density.KDE, \
           grouping_specifiers = {'Days in stock':1,'A&C':2}, \
           title= 'Cumulative GHG emissions', ylabel = '(tonne CO2eq)', \
           zero = True, alpha = 0.05)   
        
#%% Plotting  (figure 3.22)  

nice_lines(exp_b,out_b, out_to_show = 'Average total final energy use',
           group_by = 'High power for ore grades', density = Density.KDE,
           grouping_specifiers = {'low power ore.':0, 'High power ore.':1},
           title = 'Average final energy use', ylabel = '(GJ/tonne)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Overall average nickel ore grade of existing mines',
           group_by = 'High power for ore grades', density = Density.KDE,
           grouping_specifiers = {'low power ore.':0, 'High power ore.':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

#%% Plotting  (figure N35)  
  
nice_lines(exp_b,out_b, out_to_show = 'Average total final energy use',
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title = 'Average final energy use', ylabel = '(GJ/tonne)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Average total final energy use',
           group_by = 'High average mine operation plan', density = Density.KDE,
           grouping_specifiers = {'Short mine plan':0, 'Long mine plan':1},
           title = 'Average final energy use', ylabel = '(GJ/tonne)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Average total final energy use',
           group_by = 'High maximum mothball time', density = Density.KDE,
           grouping_specifiers = {'Short mothball.':0, 'Long mothball':1},
           title = 'Average final energy use', ylabel = '(GJ/tonne)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Overall average nickel ore grade of existing mines',
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Overall average nickel ore grade of existing mines',
           group_by = 'High average mine operation plan', density = Density.KDE,
           grouping_specifiers = {'Short mine plan':0, 'Long mine plan':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Overall average nickel ore grade of existing mines',
           group_by = 'High maximum mothball time', density = Density.KDE,
           grouping_specifiers = {'Short mothball.':0, 'Long mothball':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b, out_to_show = 'Average total final energy use',
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title = 'Average final energy use', ylabel = '(GJ/tonne)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b, out_to_show = 'Overall average nickel ore grade of existing mines',
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

#%% Plotting  (figure N36)

nice_lines(exp_b,out_b, out_to_show = 'Average periodic nickel price',
           group_by = 'High maximum profit deficit as percentage of investment', density = Density.KDE,
           grouping_specifiers = {'Low deficit':0, 'High deficit':1},
           title = 'Average periodic nickel price', ylabel = '(2005$/tonne)',
           zero = True, alpha = 0.05, yupperlim=250000)

nice_lines(exp_b,out_b, out_to_show = 'Degree of nickel scarcity',
           group_by = 'High maximum profit deficit as percentage of investment', density = Density.KDE,
           grouping_specifiers = {'Low deficit':0, 'High deficit':1},
           title = 'Degree of nickel scarcity', ylabel = '(Dmnl)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Total operating mining capacity utilisation',
           group_by = 'High maximum profit deficit as percentage of investment', density = Density.KDE,
           grouping_specifiers = {'Low deficit':0, 'High deficit':1},
           title = 'Operating mining capacity utilisation', ylabel = '(Dmnl)',
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b, out_to_show = 'Average periodic nickel price',
           group_by = 'High maximum mothball time', density = Density.KDE,
           grouping_specifiers = {'Short mothball.':0, 'Long mothball':1},
           title = 'Average periodic nickel price', ylabel = '(2005$/tonne)',
           zero = True, alpha = 0.05, yupperlim=250000)

nice_lines(exp_b,out_b, out_to_show = 'Degree of nickel scarcity',
           group_by = 'High maximum mothball time', density = Density.KDE,
           grouping_specifiers = {'Short mothball.':0, 'Long mothball':1},
           title = 'Degree of nickel scarcity', ylabel = '(Dmnl)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'High maximum mothball time', density = Density.KDE,
           grouping_specifiers = {'Short mothball.':0, 'Long mothball':1},
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b, out_to_show = 'Average periodic nickel price',
           group_by = 'High average mine operation plan', density = Density.KDE,
           grouping_specifiers = {'Short mine plan':0, 'Long mine plan':1},
           title = 'Average periodic nickel price', ylabel = '(2005$/tonne)',
           zero = True, alpha = 0.05, yupperlim=250000)

nice_lines(exp_b,out_b, out_to_show = 'Degree of nickel scarcity',
           group_by = 'High average mine operation plan', density = Density.KDE,
           grouping_specifiers = {'Short mine plan':0, 'Long mine plan':1},
           title = 'Degree of nickel scarcity', ylabel = '(Dmnl)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'High average mine operation plan', density = Density.KDE,
           grouping_specifiers = {'Short mine plan':0, 'Long mine plan':1},
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b, out_to_show = 'Average periodic nickel price',
           group_by = 'High minimum profit over investment', density = Density.KDE,
           grouping_specifiers = {'Low target':0, 'High target':1},
           title = 'Average periodic nickel price', ylabel = '(2005$/tonne)',
           zero = True, alpha = 0.05, yupperlim=250000)

nice_lines(exp_b,out_b, out_to_show = 'Degree of nickel scarcity',
           group_by = 'High minimum profit over investment', density = Density.KDE,
           grouping_specifiers = {'Low target':0, 'High target':1},
           title = 'Degree of nickel scarcity', ylabel = '(Dmnl)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'High minimum profit over investment', density = Density.KDE,
           grouping_specifiers = {'Low target':0, 'High target':1},
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 

#%% Plotting  (figure 3.23)

nice_lines(exp_b,out_b, out_to_show = 'Sum processing',
           group_by = 'High short administration time', density = Density.KDE,
           grouping_specifiers = {'Short time':0, 'Long time':1},
           title = 'Primary nickel processing', ylabel = '(tonne/year)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Average periodic nickel price',
           group_by = 'High short administration time', density = Density.KDE,
           grouping_specifiers = {'Short time':0, 'Long time':1},
           title = 'Average periodic nickel price', ylabel = '(2005$/tonne)',
           zero = True, alpha = 0.05, yupperlim=250000)

nice_lines(exp_b,out_b, out_to_show = 'Degree of nickel scarcity',
           group_by = 'High short administration time', density = Density.KDE,
           grouping_specifiers = {'Short time':0, 'Long time':1},
           title = 'Degree of nickel scarcity', ylabel = '(Dmnl)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Demand request',
           group_by = 'High short administration time', density = Density.KDE,
           grouping_specifiers = {'Short time':0, 'Long time':1},
           title = 'Demand request', ylabel = '(tonne/year)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Postponed demand',
           group_by = 'High short administration time', density = Density.KDE,
           grouping_specifiers = {'Short time':0, 'Long time':1},
           title = 'Postponed demand', ylabel = '(tonne/year)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'High short administration time', density = Density.KDE,
           grouping_specifiers = {'Short time':0, 'Long time':1},
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'High short administration time', density = Density.KDE,
           grouping_specifiers = {'Short time':0, 'Long time':1},
           title= 'Cum. demand - cum. consumption', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)

#%% Plotting  (figure 3.24)

nice_lines(exp_b,out_b, out_to_show = 'Sum processing',
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title = 'Primary nickel processing', ylabel = '(tonne/year)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Average periodic nickel price',
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title = 'Average periodic nickel price', ylabel = '(2005$/tonne)',
           zero = True, alpha = 0.05, yupperlim=250000)

nice_lines(exp_b,out_b, out_to_show = 'Degree of nickel scarcity',
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title = 'Degree of nickel scarcity', ylabel = '(Dmnl)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b, out_to_show = 'Sum exploration',
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title = 'Exploration', ylabel = '(tonne/year)',
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Resilience', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Final nickel availability', \
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Final nickel availability', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
#%% Plotting  (resilience)
 
nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Cum. demand - cum. consumption', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)   

nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1}, \
           title= 'Cum. demand - cum. consumption', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)  

nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP2-19':2}, \
           title= 'Difference cumulative demand and consumption', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)  

nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP5-19':3}, \
           title= 'Difference cumulative demand and consumption', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)  

nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP2-base':4}, \
           title= 'Difference cumulative demand and consumption', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)   
    
nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'High short administration time', density = Density.KDE,
           grouping_specifiers = {'Short time':0, 'Long time':1},
           title= 'Cum. demand - cum. consumption', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)
    
#%% Plotting  (figure N37)

nice_lines(exp_b,out_b, out_to_show = 'Sum exploration',
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title = 'Exploration', ylabel = '(tonne/year)',
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b, out_to_show = 'Sum exploration',
           group_by = 'Radical innovation switch', density = Density.KDE, \
           grouping_specifiers = {'No disruption':1,'Radical innovation':2}, \
           title = 'Exploration', ylabel = '(tonne/year)',
           zero = True, alpha = 0.05)
    
#%% Plotting  (figure 3.25)

#The following lines require input from the runs with an adjusted global maximum capacity increase

nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000) 
    
nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05, yupperlim=250000) 
    
nice_lines(exp_b,out_b,out_to_show = 'Average periodic nickel price', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Average periodic nickel price', ylabel = '(2005$/tonne)', \
           zero = True, alpha = 0.05) 
    
#%% Plotting  (figure N39)  

#The following lines require input from the runs with an adjusted global maximum capacity increase  
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative mined nickel', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Cumulative mined nickel', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Cumulative final demand', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Cumulative final demand', ylabel = '(tonne)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Sum final demand', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Final nickel demand', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Total cumulative GHG emissions', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Cumulative GHG emissions', ylabel = '(tonne CO2eq)', \
           zero = True, alpha = 0.05)  
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05)  
    
nice_lines(exp_b,out_b,out_to_show = 'Sum substitution', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Total substitution', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Total EoL RR', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'EoL recycling rate', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05, yupperlim=1) 
    
    
#%% Plotting  (figure N40)  

# The following lines require input from the FSP   
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
   
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Forward supply chain loss reduction switch', density = Density.KDE, \
           grouping_specifiers = {'No reduction':1,'Loss reduction':2}, \
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Forward supply chain loss reduction switch', density = Density.KDE, \
           grouping_specifiers = {'No reduction':1,'Loss reduction':2}, \
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High average mine operation plan', density = Density.KDE,
           grouping_specifiers = {'Short mine plan':0, 'Long mine plan':1},
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High average mine operation plan', density = Density.KDE,
           grouping_specifiers = {'Short mine plan':0, 'Long mine plan':1},
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High maximum profit deficit as percentage of investment', density = Density.KDE,
           grouping_specifiers = {'Low deficit':0, 'High deficit':1},
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High maximum profit deficit as percentage of investment', density = Density.KDE,
           grouping_specifiers = {'Low deficit':0, 'High deficit':1},
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High maximum mothball time', density = Density.KDE,
           grouping_specifiers = {'Short mothball.':0, 'Long mothball':1},
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High maximum mothball time', density = Density.KDE,
           grouping_specifiers = {'Short mothball.':0, 'Long mothball':1},
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Average ore grade of existing mines FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Average ore grade of known deposits FSP', ylabel = '(Dmnl)', \
           alpha = 0.05)       
    
#%% Plotting  (figure N41)     

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Option to mine resources switch', density = Density.KDE, \
           grouping_specifiers = {'Only reserves':1,'Mining resources':2}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
   
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Switch processing energy allocation method', density = Density.KDE, \
           grouping_specifiers = {'Mass based':1,'Full nickel':2}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Forward supply chain loss reduction switch', density = Density.KDE, \
           grouping_specifiers = {'No reduction':1,'Loss reduction':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Forward supply chain loss reduction switch', density = Density.KDE, \
           grouping_specifiers = {'No reduction':1,'Loss reduction':2}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High average mine operation plan', density = Density.KDE,
           grouping_specifiers = {'Short mine plan':0, 'Long mine plan':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High average mine operation plan', density = Density.KDE,
           grouping_specifiers = {'Short mine plan':0, 'Long mine plan':1},
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'Switch inclusion of by products', density = Density.KDE, \
           grouping_specifiers = {'Inclusion':1,'Exclusion':2}, \
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High maximum profit deficit as percentage of investment', density = Density.KDE,
           grouping_specifiers = {'Low deficit':0, 'High deficit':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High maximum profit deficit as percentage of investment', density = Density.KDE,
           grouping_specifiers = {'Low deficit':0, 'High deficit':1},
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High maximum mothball time', density = Density.KDE,
           grouping_specifiers = {'Short mothball.':0, 'Long mothball':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High maximum mothball time', density = Density.KDE,
           grouping_specifiers = {'Short mothball.':0, 'Long mothball':1},
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05) 
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low cap. incr.':0, 'High cap. incr.':1},
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05)     

nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High power for ore grades', density = Density.KDE,
           grouping_specifiers = {'low power ore.':0, 'High power ore.':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High power for ore grades', density = Density.KDE,
           grouping_specifiers = {'low power ore.':0, 'High power ore.':1},
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of existing mines', \
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Average ore grade of existing mines', ylabel = '(Dmnl)', \
           alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Overall average nickel ore grade of all mines', \
           group_by = 'High power for price based exploration', density = Density.KDE,
           grouping_specifiers = {'low power exp.':0, 'High power exp.':1},
           title= 'Average ore grade of known deposits', ylabel = '(Dmnl)', \
           alpha = 0.05)   
    
#%% Plotting  (figure N42)   
    
nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Australia]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Share of operating capacity Australia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)   

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Russia]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Share of operating capacity Russia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Indonesia]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Share of operating capacity Indonesia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Canada]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Share of operating capacity Canada', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05) 

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[South Africa]', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Share of operating capacity South Africa', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
#%% Plotting  (figure N43) 

nice_lines(exp_b,out_b,out_to_show = 'Additional processing required', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Additional processing required', ylabel = '(tonne/year)', \
           alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Additional processing required', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Additional processing required', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)   

#%% Plotting  (mining increase)

nice_lines(exp_b,out_b,out_to_show = 'Global mining increase percentage', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Global mining increase percentage', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05, yupperlim=10) 

#%% Plotting  (capacity increase)

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Australia]', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Share of operating capacity Australia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Australia]', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Share of operating capacity Australia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Russia]', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Share of operating capacity Russia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Indonesia]', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Share of operating capacity Indonesia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Int Waters]', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Share of operating capacity Int Waters', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Resilience', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Percentage mothballed', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Percentage mothballed', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Average operating capacity', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Average operating capacity', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Operating mines', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Operating mines', ylabel = '(Mines)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Existing mines', \
           group_by = 'High global maximum capacity increase percentage', density = Density.KDE,
           grouping_specifiers = {'low':0, 'High':1},
           title= 'Existing mines', ylabel = '(Mines)', \
           zero = True, alpha = 0.05)
    
#%% Plotting  (additional processing)
 
nice_lines(exp_b,out_b,out_to_show = 'Additional processing required', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Additional processing required', ylabel = '(tonne/year)', \
           alpha = 0.05)    
    
nice_lines(exp_b,out_b,out_to_show = 'Additional processing required', \
           group_by = 'SSP scenario switch', density = Density.KDE, \
           grouping_specifiers = {'SSP1-19':1,'SSP2-19':2,'SSP5-19':3,'SSP2-base':4}, \
           title= 'Additional processing required', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)    
    
#%% Plotting (country shares)

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Australia]', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Share of operating capacity Australia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Australia]', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Share of operating capacity Australia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Russia]', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Share of operating capacity Russia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Indonesia]', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Share of operating capacity Indonesia', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Share of operating capacity per country[Int Waters]', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Share of operating capacity Int Waters', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Difference cumulative demand and consumption', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Resilience', ylabel = '(tonne)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Percentage mothballed', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Percentage mothballed', ylabel = '(Dmnl)', \
           zero = True, alpha = 0.05)

nice_lines(exp_b,out_b,out_to_show = 'Average operating capacity', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Average operating capacity', ylabel = '(tonne/year)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Operating mines', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Operating mines', ylabel = '(Mines)', \
           zero = True, alpha = 0.05)
    
nice_lines(exp_b,out_b,out_to_show = 'Existing mines', \
           group_by = 'Improved EV battery lifetime switch', density = Density.KDE, \
           grouping_specifiers = {'8 years':1,'16 years':2}, \
           title= 'Existing mines', ylabel = '(Mines)', \
           zero = True, alpha = 0.05)
