import csv
import math
import copy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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
sns.set_style({"ytick.direction": "in", "ytick.major.size": 6.0,  "ytick.minor.size": 3.0, "xtick.direction": "in", "xtick.major.size": 6.0,  "xtick.minor.size": 3.0})

from matplotlib import rc
font = {'family': 'serif', 'serif': ['Palatino'], 'size': 18}
rc('font', **font)

plt.rcParams["figure.figsize"] = (24, 24)

site_month_aggregate_data = {}

data_file = open('Figure_Datasets/Site_Monthly_Stats_Selected.csv')
csv_data = csv.reader(data_file)

site = []
health = []
metric = []
size = []


for row in csv_data:

    site.append(row[0])
    health.append(float(row[4])/float(row[2]))
    metric.append('$H_1$')
    size.append(int(row[16]))

    site.append(row[0])
    health.append(float(row[5])/float(row[2]))
    metric.append('$H_2$')
    size.append(int(row[16]))


plt.clf()
df = pd.DataFrame({'Site': site, 'System Size': size, 'Metric': metric, 'Health': health})
g = sns.FacetGrid(df, col = 'Site', row = 'Metric', sharex = False)

#scatter_kws = {'alpha':0.25, 'color':'k', 's':50}
g.map(sns.regplot, 'System Size', 'Health', scatter_kws = {'alpha':0.125, 'color':'k'}, truncate = True)
g.fig.subplots_adjust(wspace = 0, hspace = 0)

g.axes[0, 0].set_ylabel('Health Metric, $H_1$')
g.axes[1, 0].set_ylabel('Health Metric, $H_2$')

g.axes[1, 0].set_xlabel('# of Users, $U$')
g.axes[1, 1].set_xlabel('# of Users, $U$')
g.axes[1, 2].set_xlabel('# of Users, $U$')

g.axes[0, 0].set_title('SUPERUSER')
g.axes[0, 1].set_title('PUZZLING')
g.axes[0, 2].set_title('CSTHEORY')

g.axes[1, 0].set_title('')
g.axes[1, 1].set_title('')
g.axes[1, 2].set_title('')

major_yticks = np.arange(0.20, 1.10, 0.20)
minor_yticks = np.arange(0.20, 1.00, 0.05)
axes_count = 0
for ax in g.axes[-1, :]:
    ax.set_yticks(major_yticks)
    ax.set_yticks(minor_yticks, minor = True)
    if axes_count == 0:
        major_xticks = np.arange(2000, 8010, 1500)
        minor_xticks = np.arange(2000, 8000, 300)
    elif axes_count == 1:
        major_xticks = np.arange(200, 1010, 200)
        minor_xticks = np.arange(200, 1000, 40)
    elif axes_count == 2:
        major_xticks = np.arange(100, 310, 50)
        minor_xticks = np.arange(100, 300, 10)
    ax.set_xticks(major_xticks)
    ax.set_xticks(minor_xticks, minor = True)    
    axes_count += 1
    
axes_count = 0
for ax in g.axes[-2, :]:
    ax.set_yticks(major_yticks)
    ax.set_yticks(minor_yticks, minor = True)
    if axes_count == 0:
        major_xticks = np.arange(2000, 8010, 1500)
        minor_xticks = np.arange(2000, 8000, 300)
    elif axes_count == 1:
        major_xticks = np.arange(200, 1010, 200)
        minor_xticks = np.arange(200, 1000, 40)
    elif axes_count == 2:
        major_xticks = np.arange(100, 310, 50)
        minor_xticks = np.arange(100, 300, 10)        
    ax.set_xticks(major_xticks)
    ax.set_xticks(minor_xticks, minor = True)     
    axes_count += 1

#g.set(xlabel = '')
sns.despine(trim=True, offset = 10)
sns.plt.tight_layout()
plt.savefig('Size_vs_Health.pdf', bbox_inches='tight')
plt.close()
        
        
