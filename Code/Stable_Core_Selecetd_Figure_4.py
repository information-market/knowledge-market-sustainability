import csv
import math
import copy
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib

import seaborn as sns
sns.set_context(
    "talk",
    font_scale=1,
    rc={
        "lines.linewidth": 2,
        "text.usetex": True,
        "font.family": 'serif',
        "font.serif": ['Palatino'],
        "font.size": 18
    })
sns.set_style('ticks')
sns.set_style({"ytick.direction": "in", "ytick.major.size": 6.0,  "ytick.minor.size": 3.0, "xtick.major.size": 0.0,  "xtick.minor.size": 0.0})

from matplotlib import rc
font = {'family': 'serif', 'serif': ['Palatino'], 'size': 18}
rc('font', **font)

plt.rcParams["figure.figsize"] = (6, 4)
age_list = []
contribution_list = []

data_file = open('Figure_Datasets/Death_Answerer_Selected.csv')
csv_data = csv.reader(data_file)

first_row = next(csv_data)
current_site = first_row[0]
current_user = int(first_row[1])

current_age = 1
total_contribution = int(first_row[3])

figure_count = 1

age_wise_contribution_bins = {}

for i in range(1, 6):
    age_wise_contribution_bins[i] = []
    

for row in csv_data:

    if row[0] == current_site and int(row[1]) == current_user:
        current_age += 1
        total_contribution += int(row[3])
        
    elif row[0] == current_site and int(row[2]) <> current_user:
        age_list.append(current_age)
        contribution_list.append(float(total_contribution)/current_age)

        current_user = int(row[1])
        current_age = 1
        total_contribution = int(row[3])

#print max(age_list), min(age_list)
for i, age in enumerate(age_list):
    bin_id = (age-min(age_list))*5/(max(age_list)+1-min(age_list))+1
    age_wise_contribution_bins[bin_id].append(contribution_list[i])

#Plotting by seaborn
cmap = matplotlib.cm.get_cmap('Greys')

rgb_1 = cmap(0.3)
rgb_2 = cmap(0.37)
rgb_3 = cmap(0.44)
rgb_4 = cmap(0.51)
rgb_5 = cmap(0.58)

f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows = 1, ncols = 5, sharey=True)

sns.lvplot(y = age_wise_contribution_bins[1], ax = ax1, color =  rgb_1)
sns.lvplot(y = age_wise_contribution_bins[2], ax = ax2, color =  rgb_2)
sns.lvplot(y = age_wise_contribution_bins[3], ax = ax3, color =  rgb_3)
sns.lvplot(y = age_wise_contribution_bins[4], ax = ax4, color =  rgb_4)
sns.lvplot(y = age_wise_contribution_bins[5], ax = ax5, color =  rgb_5)

ax3.set_title('ANDROID')

ax1.set(xlabel='1 - 13')
ax2.set(xlabel='14 - 26')
ax3.set(xlabel='27 - 39\n # of Months')
ax4.set(xlabel='40 - 52')
ax5.set(xlabel='53 - 65')

ax1.set(ylabel='# of Answers')

ax1.set_yticks(np.arange(0, 30, 1), minor=True)

sns.despine(offset = 10, trim=True, bottom = True, left = True)
sns.despine(ax = ax1, offset = 10, trim=True, bottom = True)

ax2.tick_params(which = 'both', left = 'off')
ax3.tick_params(which = 'both', left = 'off')
ax4.tick_params(which = 'both', left = 'off')
ax5.tick_params(which = 'both', left = 'off')

sns.plt.tight_layout()
plt.savefig('Stable_Core.pdf')



