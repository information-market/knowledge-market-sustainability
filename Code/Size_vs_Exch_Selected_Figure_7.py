import csv
import math
import copy
import random
import operator
import numpy as np
import pandas as pd
from scipy.spatial import distance
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

for row in csv_data:

    if row[0] not in site_month_aggregate_data:
        site_month_aggregate_data[row[0]] = {}

    if int(row[1]) not in site_month_aggregate_data[row[0]]:
        site_month_aggregate_data[row[0]][int(row[1])] = []

    site_month_aggregate_data[row[0]][int(row[1])].append(float(row[2]))
    site_month_aggregate_data[row[0]][int(row[1])].append(float(row[3]))
    site_month_aggregate_data[row[0]][int(row[1])].append(int(row[16]))

site_month_user_data = {}

data_file = open('Figure_Datasets/Contribution_of_Top_Users_Na_and_Nq_Selected.csv')
csv_data = csv.reader(data_file)

for row in csv_data:

    if row[0] not in site_month_user_data:
        site_month_user_data[row[0]] = {}

    if int(row[1]) not in site_month_user_data[row[0]]:
        site_month_user_data[row[0]][int(row[1])] = []
        
    site_month_user_data[row[0]][int(row[1])].append((float(row[4]), float(row[5]))) 


month_question_count = []
month_answer_count = []
month_no_of_users = []

month_user_data = []


df_column_site = []
df_column_size = []
df_column_metric = []
df_column_stability = []

for site in sorted(site_month_aggregate_data.keys()):
    print site
    for month in sorted(site_month_aggregate_data[site].keys()):
        month_question_count.append(site_month_aggregate_data[site][month][0])
        month_answer_count.append(site_month_aggregate_data[site][month][1])
        month_no_of_users .append(site_month_aggregate_data[site][month][2])
        month_user_data.append(site_month_user_data[site][month])

    avg_contribution_tuple_top_threshold = []
    avg_contribution_tuple_bottom_threshold = []
    avg_contribution_tuple_avg_threshold = []
    user_percent = []

    if min(month_no_of_users) >= 50:
        for ab_threshold in [x / 100.0 for x in range(5, 6, 1)]:
            contribution_tuple_top = []
            contribution_tuple_bottom = []
            contribution_tuple_avg = []

            for i, user_data in enumerate(month_user_data):
                top_user_contribution = (0, 0)
                bottom_user_contribution = (0, 0)
                avg_user_contribution = (0, 0)

                for N in range(0, int(ab_threshold*len(user_data))):
                    top_user_contribution = tuple(map(operator.add, top_user_contribution, user_data[N]))

                for N in range(len(user_data)-int(ab_threshold*len(user_data)), len(user_data)):
                    bottom_user_contribution = tuple(map(operator.add, bottom_user_contribution, user_data[N]))

                number_of_permutations = 20
                for perm in range(number_of_permutations):
                    randomized_user_data = copy.deepcopy(user_data)
                    random.shuffle(randomized_user_data)

                    for N in range(0, int(ab_threshold*len(user_data))):
                        avg_user_contribution = tuple(map(operator.add, avg_user_contribution, randomized_user_data[N]))
                        
                avg_user_contribution = tuple(ti/number_of_permutations for ti in avg_user_contribution)

                normalization = (month_question_count[i], month_answer_count[i])
                contribution_tuple_top.append(tuple(map(operator.truediv, top_user_contribution, normalization)))
                contribution_tuple_bottom.append(tuple(map(operator.truediv, bottom_user_contribution, normalization)))
                contribution_tuple_avg.append(tuple(map(operator.truediv, avg_user_contribution, normalization)))

            stability_metric = [(distance.euclidean(x, z)+distance.euclidean(y, z))*50 for x, y, z in zip(contribution_tuple_top,  contribution_tuple_bottom, contribution_tuple_avg)]
            stability_mean = np.mean(np.array(stability_metric))
            stability_sd = np.std(np.array(stability_metric))

            size_mean = np.mean(np.array(month_no_of_users))
            size_sd = np.std(np.array(month_no_of_users))

            for i, x in enumerate(month_no_of_users):
                y = stability_metric[i]
                df_column_site.append(site)
                df_column_size.append(x)
                df_column_metric.append('$I_1$')
                df_column_stability.append(y)
                '''
                if x > size_mean-2*size_sd and x < size_mean+2*size_sd and y > stability_mean-2*stability_sd and y < stability_mean+2*stability_sd:
                    df_column_site.append(site)
                    df_column_size.append(x)
                    df_column_metric.append('$S_1$')
                    df_column_stability.append(y)
                '''

    month_question_count[:] = []
    month_answer_count[:] = []
    month_no_of_users[:] = []
    month_user_data[:] = []

print min(df_column_stability), max(df_column_stability)

################################################################################################################
#2nd Innings
site_month_user_data = {}

data_file = open('Figure_Datasets/Contribution_of_Top_Users_Na_by_Nq_Selected.csv')
csv_data = csv.reader(data_file)

for row in csv_data:

    if row[0] not in site_month_user_data:
        site_month_user_data[row[0]] = {}

    if int(row[1]) not in site_month_user_data[row[0]]:
        site_month_user_data[row[0]][int(row[1])] = []
        
    site_month_user_data[row[0]][int(row[1])].append(float(row[3])) 

month_no_of_users = []

month_user_data = []

for site in sorted(site_month_aggregate_data.keys()):
    print site
    
    for month in sorted(site_month_aggregate_data[site].keys()):
        
        month_no_of_users .append(site_month_aggregate_data[site][month][2])
        
        month_user_data.append(site_month_user_data[site][month])

    avg_contribution_ratio_top_threshold = []
    avg_contribution_ratio_bottom_threshold = []
    avg_contribution_ratio_avg_threshold = []
    user_percent = []

    if min(month_no_of_users) >= 50:
        
        for ab_threshold in [x / 100.0 for x in range(5, 6, 1)]:

            contribution_ratio_top = []
            contribution_ratio_bottom = []
            contribution_ratio_avg = []

            for i, user_data in enumerate(month_user_data):
                top_user_contribution = 0
                bottom_user_contribution = 0
                avg_user_contribution = 0

                for N in range(0, int(ab_threshold*len(user_data))):
                    top_user_contribution = top_user_contribution+user_data[N]

                for N in range(len(user_data)-int(ab_threshold*len(user_data)), len(user_data)):
                    bottom_user_contribution = bottom_user_contribution+user_data[N]

                number_of_permutations = 20
                for perm in range(number_of_permutations):
                    randomized_user_data = copy.deepcopy(user_data)
                    random.shuffle(randomized_user_data)

                    for N in range(0, int(ab_threshold*len(user_data))):
                        avg_user_contribution = avg_user_contribution+randomized_user_data[N]
                avg_user_contribution = avg_user_contribution / number_of_permutations

                contribution_ratio_top.append(top_user_contribution)
                contribution_ratio_bottom.append(bottom_user_contribution)
                contribution_ratio_avg.append(avg_user_contribution)

            stability_metric = [x/y for x, y in zip(contribution_ratio_top, contribution_ratio_bottom)]
            print stability_metric
            stability_mean = np.mean(np.array(stability_metric))
            stability_sd = np.std(np.array(stability_metric))

            size_mean = np.mean(np.array(month_no_of_users))
            size_sd = np.std(np.array(month_no_of_users))

            for i, x in enumerate(month_no_of_users):
                y = stability_metric[i]
                df_column_site.append(site)
                df_column_size.append(x)
                df_column_metric.append('$I_2$')
                df_column_stability.append(y)
                '''
                if x > size_mean-2*size_sd and x < size_mean+2*size_sd and y > stability_mean-2*stability_sd and y < stability_mean+2*stability_sd:
                    df_column_site.append(site)
                    df_column_size.append(x)
                    df_column_metric.append('$S_2$')
                    df_column_stability.append(y)
                '''

    month_no_of_users[:] = []
    month_user_data[:] = []

df_column_site = df_column_site[::-1]
df_column_size = df_column_size[::-1]
df_column_metric = df_column_metric[::-1]
df_column_stability = df_column_stability[::-1]

plt.clf()
df = pd.DataFrame({'Site': df_column_site, 'System Size': df_column_size, 'Metric': df_column_metric,'Instability': df_column_stability})

g = sns.FacetGrid(df, col = 'Site', row = 'Metric', sharex = False)
g.map(sns.regplot, 'System Size', 'Instability', scatter_kws = {'alpha':0.125, 'color':'k'}, truncate = True)

g.fig.subplots_adjust(wspace = 0, hspace = 0)

g.axes[0, 0].set_ylabel('Exch. Metric, $E_1$')
g.axes[1, 0].set_ylabel('Exch. Metric, $E_2$')

g.axes[1, 0].set_xlabel('# of Users, $U$')
g.axes[1, 1].set_xlabel('# of Users, $U$')
g.axes[1, 2].set_xlabel('# of Users, $U$')

g.axes[0, 0].set_title('SUPERUSER')
g.axes[0, 1].set_title('PUZZLING')
g.axes[0, 2].set_title('CSTHEORY')

g.axes[1, 0].set_title('')
g.axes[1, 1].set_title('')
g.axes[1, 2].set_title('')


major_yticks = np.arange(10, 100, 20)
minor_yticks = np.arange(10, 90, 5)
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
plt.savefig('Size_vs_Exch.pdf', bbox_inches='tight')
plt.close()

        
        
        
        
