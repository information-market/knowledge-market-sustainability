import csv
import numpy as np
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
sns.set_style({"ytick.direction": "in", "ytick.major.size": 6.0,  "ytick.minor.size": 3.0, "xtick.direction": "in", "xtick.major.size": 0.0,  "xtick.minor.size": 0.0})

from matplotlib import rc
font = {'family': 'serif', 'serif': ['Palatino'], 'size': 18}
rc('font', **font)

plt.rcParams["figure.figsize"] = (6, 4)

immature_sites = {}

data_file = open('Figure_Datasets/Immature_Site_List.csv')
csv_data = csv.reader(data_file)

for row in csv_data:
    immature_sites[row[0]] = 1

data_file = open('Figure_Datasets/Site_Basic_Stats.csv')
csv_data = csv.reader(data_file)

active_age = []
total_user = []
total_post = []

for row in csv_data:
    if row[0] not in immature_sites:
        active_age.append(int(row[1]))
        total_post.append(int(row[2]))
        total_user.append(int(row[3]))

print 'Maximum Age:', max(active_age), 'Minimum Age:', min(active_age)
print 'Maximum User:', max(total_user), 'Minimum User:', min(total_user)
print 'Maximum Post:', max(total_post), 'Minimum Post:', min(total_post)

cmap = matplotlib.cm.get_cmap('Greys')

rgb_1 = cmap(0.3)
rgb_2 = cmap(0.45)
rgb_3 = cmap(0.6)

#Plotting by seaborn
f, (ax1, ax2, ax3) = plt.subplots(nrows = 1, ncols = 3)

sns.lvplot(y = active_age, ax = ax1, color =  rgb_1)
sns.lvplot(y = total_user, ax = ax2, color =  rgb_2)
sns.lvplot(y = total_post, ax = ax3, color =  rgb_3)

ax1.set(xlabel='# of Months')
ax2.set(xlabel='# of Users')
ax3.set(xlabel='# of Posts')

ax1.set_yscale('log')
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.logspace(1, 2, 2))

ax2.set_yscale('log')
ax2.minorticks_off()
ax2.yaxis.set_ticks(np.logspace(3, 6, 4))

ax3.set_yscale('log')
ax3.minorticks_off()
ax3.yaxis.set_ticks(np.logspace(3, 6, 4))

sns.despine(offset = 10, trim=True, bottom = True)
sns.plt.tight_layout()
plt.savefig('Dataset_Statistics.pdf', bbox_inches='tight')
plt.close()
