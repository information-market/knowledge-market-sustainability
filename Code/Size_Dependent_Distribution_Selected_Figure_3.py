import csv
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

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

plt.rcParams["figure.figsize"] = (24, 12)

data_file = open('Figure_Datasets/Contribution_of_Top_Answerers_Selected.csv')
csv_data = csv.reader(data_file)

figure_count = 1
site_list = []
slope_list = []
population_list = []

first_row = next(csv_data)
current_site = first_row[0]
current_month = int(first_row[1])

user_contribution = float(first_row[3])

contribution_list = []

contribution_list.append(user_contribution)

for row in csv_data:

    #If current site and month, add data for model construction
    
    if row[0] == current_site and int(row[1]) == current_month:   
        user_contribution = float(row[3])
        contribution_list.append(user_contribution)
        
    #If current site and new month, construct and plot current model, and reassign the data variables
        
    elif row[0] == current_site and int(row[1]) <> current_month: 

        #At least 10 users for model construction
        
        if len(contribution_list) >= 50:
            
            log_contribution_list = np.log10(contribution_list)
            (n, bins, patches) = plt.hist(contribution_list, bins=np.logspace(min(log_contribution_list), max( log_contribution_list)+1, 21))
            center = (bins[:-1] + bins[1:]) / 2

            center = np.array(center)
            x = center[n!=0]
            x = np.log10(x)

            n = np.array(n)
            y = n[n!=0]
            y = np.log10(y)

            slope, intercept = np.poly1d(np.polyfit(x, y, 1))
            site_list.append(current_site)
            slope_list.append(slope)
            population_list.append(len(contribution_list))

        current_month = int(row[1])      
        contribution_list[:] = []    
        user_contribution = float(row[3])
        contribution_list.append(user_contribution)

    else: 

        current_site = row[0]
        current_month = int(first_row[1])     
        contribution_list[:] = []       
        user_contribution = float(row[3])
        contribution_list.append(user_contribution)


plt.clf()
df = pd.DataFrame({'Site': site_list, 'System Size': population_list, 'Exponent': slope_list})
g = sns.FacetGrid(df, col = 'Site', sharex = False)
#scatter_kws = {'alpha':0.25, 'color':'k', 's':50}
g.map(sns.regplot, 'System Size', 'Exponent', scatter_kws = {'alpha':0.125, 'color':'k'}, truncate = True)
g.fig.subplots_adjust(wspace = 0, hspace = 0)

g.axes[0, 0].set_ylabel(r'Power-law Exp., $\alpha$')

g.axes[0, 0].set_xlabel('# of Users, $U$')
g.axes[0, 1].set_xlabel('# of Users, $U$')
g.axes[0, 2].set_xlabel('# of Users, $U$')

g.axes[0, 0].set_title('ANDROID')
g.axes[0, 1].set_title('APPLE')
g.axes[0, 2].set_title('BIOLOGY')

major_yticks = np.arange(-1.8, -0.62, 0.2)
minor_yticks = np.arange(-1.8, -0.8, 0.04)
axes_count = 0
for ax in g.axes[-1, :]:
    ax.set_yticks(major_yticks)
    ax.set_yticks(minor_yticks, minor = True)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    if axes_count == 0:
        major_xticks = np.arange(100, 510, 100)
        minor_xticks = np.arange(100, 510, 20)
    elif axes_count == 1:
        major_xticks = np.arange(200, 1210, 250)
        minor_xticks = np.arange(200, 1210, 50)
    elif axes_count == 2:
        major_xticks = np.arange(50, 180, 30)
        minor_xticks = np.arange(50, 170, 6)
    ax.set_xticks(major_xticks)
    ax.set_xticks(minor_xticks, minor = True)     
    axes_count += 1

#g.set(xlabel = '')
sns.despine(trim=True, offset = 10)
sns.plt.tight_layout()
plt.savefig('Size_Dependent_Distribution.pdf', bbox_inches='tight')
plt.close()
