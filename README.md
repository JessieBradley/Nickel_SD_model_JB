# Description

This repository contains the data, model and code for the following research:

- Bradley, J. E. (2021). The Future of Nickel in a Transitioning World: Exploratory System Dynamics Modelling and Analysis of the Global Nickel Supply Chain and its Nexus with the Energy System. [Master’s thesis, Delft University of Technology]. TU Delft Research Repository. https://repository.tudelft.nl/islandora/object/uuid%3A48cc8ac4-6e3a-49d3-bb28-af7ecc40ff2b
- Bradley, J. E., Auping, W.L., Kleijn, R., Kwakkel, J.H., Mudd, G.M., Sprecher, B. (2025). System Dynamics Modelling of the Global Nickel Supply System at the Level of Individual Mines. [Manuscript in preparation]

# Files

- Input data: the excel file used as input for the Vensim model, which includes detailed information on individual mines (Nickel-subset-4-BSprecherxx.xlsx). 
- Model: two versions of the model are included: the main model following the Opportunity Cost Paradigm (OCP), which includes price feedbacks on demand and exploration, and an additional model following the Fixed Stock Paradigm (FSP), which excludes these feedbacks. Both the models themselves (.mdl) and the files for reading the models with python (.vpmx) are included.
- Code: scripts for running the model (Nickel_JB_final.py) and data visualisation (Nickel_JB_final_main_graphs.py, Nickel_JB_final_graphs.py, and Nickel_JB_final_trees.py, of which the first file includes the main figures in Bradley et al. (2025))
- Output data: the output data for the runs generated in our research is too large to upload directly to this repository. It can be found in release v1.0.0. (NickelJBfinal_data.tar.zip). This file contains two tarballs, one for the OCP (used to generate the figures in Bradley et al., 2025) and one for the FSP. These files are compressed files that contain CSV files.   
- Other: single run model output files (SSP2-base_GHG.csv and SSP5-19_GHG.csv) and script (Nickel_JB_final_map_figures.py) for creating maps for greenhouse gas emissions. 
  
# Software requirements

- Vensim DSS (version 8.1)
- Python (version 3.8.3)
- EMA workbench (version 2.0)

# Usage instructions

- Single runs: for single runs, the model can be opened and run in Vensim and the values of uncertain variables can be changed manually.
- Maps from single runs: maps can be generated using Nickel_JB_final_map_figures.py after exporting csvs for single variables from the model.
- Multiple runs: for multiple runs, first run the script for running the model (Nickel_JB_final.py). This will generate a file that can then be used in the scripts for data visualisation (Nickel_JB_final_main_graphs.py, Nickel_JB_final_graphs.py, and Nickel_JB_final_trees.py). The runtime for multiple runs depends on your computer. On a simple laptop, it takes about a day. When running the code, a new set of runs will be generated each time that can differ from the results used in our research. The output data for the runs generated in our research can be found in release v1.0.0. For further information, please contact jessiebrad@gmail.com. 
