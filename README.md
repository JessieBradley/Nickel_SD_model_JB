# Description

This repository contains the data, model and code for the following research:

- Bradley, J. E. (2021). The Future of Nickel in a Transitioning World: Exploratory System Dynamics Modelling and Analysis of the Global Nickel Supply Chain and its Nexus with the Energy System. [Master’s thesis, Delft University of Technology]. TU Delft Research Repository. https://repository.tudelft.nl/islandora/object/uuid%3A48cc8ac4-6e3a-49d3-bb28-af7ecc40ff2b
- Bradley, J. E., Auping, W.L., Kleijn, R., Kwakkel, J.H., Mudd, G.M., Sprecher, B. (2025). Toward Prospective Dynamic Criticality Assessment: Detailed System Dynamics Modelling of the Global Nickel Supply System. [Manuscript in preparation]

# Files

- Inputdata/ contains the excel file used as input for the Vensim models.
- Model/ contains the Vensim models, including the main model following the Opportunity Cost Paradigm (OCP), which includes price feedbacks on demand and exploration, and an additional model following the Fixed Stock Paradigm (FSP), which excludes these feedbacks. Both the models themselves (.mdl) and.... (.vpmx) are included.
- Code/ contains the scripts for running the model (title) and data visualisation (titles)
  
# Software requirements

- Vensim (version...)
- Python (version...)
- EMA workbench (version...)

# Usage instructions

- Single runs: for single runs, the model can be opened and run in Vensim and the values of uncertain variables can be changed manually. Maps can be generated after using single runs...
- Multiple runs: for multiple runs, first run the script for running the model (title). This will generate a file that can then be used in the scripts for data visualisation (titles)  

The runtime depends on your computer. On a simple laptop, it takes about a day.

# Reproducibility

When running the code, a new set of runs will be generated each time that can differ from the results used in our research. The output data for the runs generated in our research is too large to upload to GitHub. For access to this data, please contact jessiebrad@gmail.com. 
