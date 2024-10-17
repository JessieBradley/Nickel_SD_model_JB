# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 18:02:10 2020

@author: Jessie Bradley
adapted from Erika van der Linden (2020)
"""

#%% Imports

from __future__ import (absolute_import, print_function, division, unicode_literals)
from ema_workbench import (Model, RealParameter, ScalarOutcome, Constant,Policy, perform_experiments, ema_logging,
TimeSeriesOutcome, perform_experiments,save_results, load_results)
from ema_workbench.analysis import (feature_scoring)
from ema_workbench.analysis.pairs_plotting import (pairs_lines, pairs_scatter,pairs_density)
from ema_workbench.connectors.vensim import (VensimModel) #LookupUncertainty,VensimModel, VensimModelStructureInterface)
from ema_workbench.em_framework import CategoricalParameter
from ema_workbench.em_framework.evaluators import LHS, SOBOL, MORRIS
from ema_workbench.analysis.plotting import lines, envelopes
from ema_workbench.analysis import clusterer, plotting, Density
#from Figures import plot_lines_with_envelopes
#from plotting_util import group_results, filter_scalar_outcomes,make_grid,make_legend
TIME_LABEL = 'Time'
from ema_workbench.analysis.plotting_util import prepare_data, COLOR_LIST,simple_kde, group_density,\
plot_envelope, simple_density,do_titles,\
do_ylabels, TIME
import ema_workbench.analysis.plotting_util as plt_util
from ema_workbench.analysis.plotting import group_by_envelopes,single_envelope, plot_lines_with_envelopes
from ema_workbench.analysis.pairs_plotting import pairs_scatter, pairs_density
from ema_workbench.analysis import pairs_plotting
from ema_workbench.analysis import (get_ex_feature_scores,
RuleInductionType)

import numpy as np
import seaborn as sns #; sns.set(style="ticks", color_codes=True)
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import copy
from copy import deepcopy
import numpy as np
import datetime
import math
import matplotlib.gridspec as gridspec
import scipy.stats.kde as kde
from matplotlib.colors import ColorConverter
from matplotlib.collections import PolyCollection, PathCollection
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie
from matplotlib.ticker import FormatStrFormatter, FuncFormatter
from matplotlib.patches import ConnectionPatch
import matplotlib.font_manager as fm
import matplotlib as mpl


#%% Load results

results = load_results(r'C:\Users\jessi\Desktop\Thesis\Python\NickelJBfinal.tar.gz')

experiments,outcomes = results

#%% Extra tree feature scoring (try to get it per 2 years instead of 0.5 without the length mismatch...)

def get_ex_feature_scores_topx (variable,top_nr):
    x= experiments.drop(['model', 'policy'], axis=1)
    y = outcomes[variable]
    all_scores = []
    top_x = set()
    for i in range(2, y.shape[1], 8):
        data = y[:, i]
        scores = get_ex_feature_scores(x, data,
                                       mode=RuleInductionType.REGRESSION)[0]
        top_x |= set(scores.nlargest(top_nr, 1).index.values)
        all_scores.append(scores)
    all_scores = pd.concat(all_scores, axis=1, sort=False)
    all_scores = all_scores.loc[top_x, :]
    all_scores.columns = np.arange(2015, 2060, 0.5)
    all_scores = all_scores.sort_values(by = [2015], ascending = False)
# for i in all_scores.T:
# if max(all_scores.T[i]) < 0.15:
# all_scores_transposed = all_scores.T.drop[i]
    return (all_scores)

def plot_heatmap_overtime (scores,title):
    sns.heatmap(scores, cmap='viridis')
    fig = plt.gcf()
    ax = fig.get_axes()
    ax[0].set_xticklabels(np.arange(2015, 2060, 2))
    fig.autofmt_xdate()
    fig.set_size_inches(15,5)
    fig.suptitle('Extra trees feature scores for variables with highest impact on '+title)
    shorttitle = title.replace(" ","")
    plt.show()

#%% Plotting 

all_scores_price = get_ex_feature_scores_topx('Sum final demand',2)
plot_heatmap_overtime(all_scores_price,title = 'Final nickel demand')

all_scores_price = get_ex_feature_scores_topx('Sum processing',2)
plot_heatmap_overtime(all_scores_price,title = 'Primary nickel processing')

all_scores_price = get_ex_feature_scores_topx('Sum mining',2)
plot_heatmap_overtime(all_scores_price,title = 'Nickel mining')

all_scores_price = get_ex_feature_scores_topx('Average periodic nickel price',2)
plot_heatmap_overtime(all_scores_price,title = 'Average periodic nickel price')

all_scores_price = get_ex_feature_scores_topx('Average total final energy use',2)
plot_heatmap_overtime(all_scores_price,title = 'Average total final energy use')

#%% Plotting 

all_scores_price = get_ex_feature_scores_topx('Overall average nickel ore grade of existing mines',2)
plot_heatmap_overtime(all_scores_price,title = 'Average ore grade of existing mines')

all_scores_price = get_ex_feature_scores_topx('Overall average nickel ore grade of all mines',2)
plot_heatmap_overtime(all_scores_price,title = 'Average ore grade of known deposits')

#%% Plotting 

all_scores_price = get_ex_feature_scores_topx('Total cumulative GHG emissions',2)
plot_heatmap_overtime(all_scores_price,title = 'Cumulative GHG emissions')

all_scores_price = get_ex_feature_scores_topx('Total EoL RR',2)
plot_heatmap_overtime(all_scores_price,title = 'EOL recycling rate')

#%% Plotting 

all_scores_price = get_ex_feature_scores_topx('Sum substitution',2)
plot_heatmap_overtime(all_scores_price,title = 'Substitution')

all_scores_price = get_ex_feature_scores_topx('Sum exploration',2)
plot_heatmap_overtime(all_scores_price,title = 'Exploration')

