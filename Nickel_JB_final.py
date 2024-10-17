# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 23:12:47 2020

@author: Jessie Bradley
adapted from Erika van der Linden (2020)
"""

#%% Imports

from ema_workbench import RealParameter, ema_logging, TimeSeriesOutcome, perform_experiments, save_results
from ema_workbench.connectors.vensim import VensimModel
from ema_workbench.em_framework import CategoricalParameter

#%% Set working directory (needs to change)
wd = 'C:/Users/jessi/Desktop/Thesis/Python/'

# Turn on logging
ema_logging.log_to_stderr(ema_logging.INFO)

#%% Define model
Nickel_model = VensimModel('Vensim', wd = wd,model_file=wd+'NickelJBfinal.vpmx')

#%% Define uncertainties
Nickel_model.uncertainties = [
# Disruption scenario switches (energy transition)
    CategoricalParameter('SSP scenario switch', (1,2,3,4)),
#    CategoricalParameter('Transport scenario switch',(1,2) ),
    CategoricalParameter('Switch flexibility measures',(1,2,3) ),
    CategoricalParameter('Switch price scenario',(1,2,3) ),
# Disruption scenario switches (other disruptions)
    CategoricalParameter('Radical innovation switch', (1,2) ),
    CategoricalParameter('Supply disruption switch', (1,2)),
# Structural uncertainty switches
#    CategoricalParameter('Paradigm switch',(1,2)),
    CategoricalParameter('Switch processing energy allocation method', (1,2)),
    CategoricalParameter('Switch mining energy allocation method', (1,2,3)),
#    CategoricalParameter('Energy calculation method switch', (1,2,3)),
    CategoricalParameter('Switch inclusion of by products', (1,2)),
    CategoricalParameter('Option to mine resources switch', (1,2)),
    CategoricalParameter('Switch price method', (1,2)),
#    CategoricalParameter('Stockpiling inclusion switch', (1,2)),
# Sustainability policy switches
    CategoricalParameter('EoL management of batteries switch', (1,2,3,4)),
    CategoricalParameter('Improved EV battery lifetime switch', (1,2)),
    CategoricalParameter('Forward supply chain loss reduction switch', (1,2)),
# Important parametric uncertainties 
    RealParameter('Substitution threshold[Batteries]',2.5 ,5 ), 
    RealParameter('Administration postponed demand',0.5 ,2 ),
    RealParameter('Power for price based exploration',0.5 ,1 ),
    RealParameter('Opportunity check frequency',2 ,3 ),
    RealParameter('Maximum capacity',100000 ,1000000 ),  
    RealParameter('Global maximum capacity increase percentage',0.1 ,0.5 ),
    RealParameter('Average mine operation plan',10 ,20 ),
    RealParameter('Average maximum profit deficit as percentage of investment',0.03 ,0.08 ),
    RealParameter('Average minimum profit surplus as percentage of investment',0.03 ,0.08 ),
    RealParameter('Average maximum mothball time',10 ,30 ),
    RealParameter('Power for ore grades',0.1 ,0.5 ),
    RealParameter('Minimum profit over investment',1.2 ,2 ),
    RealParameter('Additional expenses for DSM',2 ,20 ),
#    RealParameter('Intensity of stockpiling',0.5 ,0.95 ),
]

#%% Define outcomes

Nickel_model.outcomes = [
# General
        TimeSeriesOutcome('TIME'),
# Demand projections     
        TimeSeriesOutcome('Sum final demand'),
        TimeSeriesOutcome('Cumulative final demand'),
        TimeSeriesOutcome('Sum total functional nickel demand'), 
        TimeSeriesOutcome('Sum substitution'),
        TimeSeriesOutcome('Substitution[Batteries]'),
        TimeSeriesOutcome('Sum demand change due to price elasticity'),
        TimeSeriesOutcome('Demand request'),
        TimeSeriesOutcome('Postponed demand'),
        TimeSeriesOutcome('Total nickel demand for vehicle batteries[Batteries]'),
        TimeSeriesOutcome('Nickel demand for electricity generation[Stainless steel]'), 
        TimeSeriesOutcome('Nickel demand for stationary batteries[Batteries]'),
        TimeSeriesOutcome('Sum demand RoE'),
# Energy transition
        TimeSeriesOutcome('Sum mining'),
        TimeSeriesOutcome('Total cumulative mined nickel'),
        TimeSeriesOutcome('Cumulative mined cobalt'),
        TimeSeriesOutcome('Cumulative mined palladium'),
        TimeSeriesOutcome('Average periodic nickel price'),  
        TimeSeriesOutcome('Degree of nickel scarcity'),         
        TimeSeriesOutcome('Average marginal cost nickel'), 
        TimeSeriesOutcome('Average nickel royalties'),   
        TimeSeriesOutcome('Reagents and other marginal costs'),
        TimeSeriesOutcome('Average credits for by products'),
        TimeSeriesOutcome('Average marginal cost deposits'),
        TimeSeriesOutcome('Average total final energy use'),
        TimeSeriesOutcome('Total average energy costs'),        
        TimeSeriesOutcome('Average final energy use mining'),
        TimeSeriesOutcome('Average final energy use processing'),  #Does not include refining          
        TimeSeriesOutcome('Average energy costs mining'),  
        TimeSeriesOutcome('Average energy costs processing and refining'), 
        TimeSeriesOutcome('Fraction of mines per mine type[OC]'),           
        TimeSeriesOutcome('Fraction of mines per ore type[Laterite]'), 
        TimeSeriesOutcome('Overall average nickel ore grade of existing mines'),
        TimeSeriesOutcome('Overall average nickel ore grade of all mines'),          
        TimeSeriesOutcome('Average electricity price'),
        TimeSeriesOutcome('Total cumulative GHG emissions'),     
        TimeSeriesOutcome('Average carbon costs'), 
# Other disruptions     
        TimeSeriesOutcome('Sum processing'),
        TimeSeriesOutcome('Depletion of oringinal resources'),  
# EoL waste management      
        TimeSeriesOutcome('Total EoL RR'),
        TimeSeriesOutcome('Sum recycling'), 
        TimeSeriesOutcome('Recycling input rate'),       
# Other
        TimeSeriesOutcome('Total operating mining capacity utilisation'),
        TimeSeriesOutcome('Sum exploration'),
        TimeSeriesOutcome('Sum final energy use in GJ'),
        TimeSeriesOutcome('Total GHG emissions'), 
        TimeSeriesOutcome('Additional processing required'),
        TimeSeriesOutcome('Share of operating capacity per country[Australia]'),
        TimeSeriesOutcome('Share of operating capacity per country[Russia]'),
        TimeSeriesOutcome('Share of operating capacity per country[Indonesia]'),
        TimeSeriesOutcome('Share of operating capacity per country[Int Waters]'),
        TimeSeriesOutcome('Share of operating capacity per country[Canada]'),
        TimeSeriesOutcome('Share of operating capacity per country[South Africa]'),
        TimeSeriesOutcome('Global capacity increase percentage'),
        TimeSeriesOutcome('Global mining increase percentage'),        
        TimeSeriesOutcome('Total GHG emissions per capita'),   
        TimeSeriesOutcome('Consumption'), 
        TimeSeriesOutcome('Final nickel availability'), 
        TimeSeriesOutcome('R over P ratio'),
        TimeSeriesOutcome('Difference cumulative demand and consumption'),
        TimeSeriesOutcome('Existing mines'),
        TimeSeriesOutcome('Operating mines'),
        TimeSeriesOutcome('Average operating capacity'), 
        TimeSeriesOutcome('Percentage mothballed'),   
        TimeSeriesOutcome('Finished nickel stock'),
        TimeSeriesOutcome('Days of demand in stock'),                       
]

#%% Create results

nr_experiments =1000
results = perform_experiments([Nickel_model],nr_experiments)

#File path needs to change
save_results(results, r'C:/Users/jessi/Desktop/Thesis/Python/NickelJBfinal_2.tar.gz')
