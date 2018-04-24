import csv
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn import linear_model

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


r_asker = []
r_answerer = []
r_commenter = []

data_file = open('Figure_Datasets/Site_Monthly_Stats_Clean_with_Dummy.csv')
csv_data = csv.reader(data_file)

first_row = next(csv_data)
current_site = first_row[0]

asker_count = []
answerer_count = []
commenter_count = []
user_count = []

asker_count.append(int(first_row[6]))
answerer_count.append(int(first_row[7]))
commenter_count.append(int(first_row[12]))
user_count.append(int(first_row[14]))

figure_count = 1

for row in csv_data:

    #If current site, add data for model construction
    
    if row[0] == current_site:

        asker_count.append(int(row[6]))
        answerer_count.append(int(row[7]))
        commenter_count.append(int(row[12]))
        user_count.append(int(row[14]))
        
    #If new site, construct and plot current model, and reassign the data variables
        
    else:

        ransac = linear_model.RANSACRegressor()
        ransac.fit(np.array(user_count).reshape(-1, 1), np.array(asker_count).reshape(-1, 1))
        inlier_mask = ransac.inlier_mask_
        r_asker.append(ransac.score(np.array(user_count).reshape(-1, 1)[inlier_mask], np.array(asker_count).reshape(-1, 1)[inlier_mask]))

        ransac = linear_model.RANSACRegressor()
        ransac.fit(np.array(user_count).reshape(-1, 1), np.array(answerer_count).reshape(-1, 1))
        inlier_mask = ransac.inlier_mask_
        r_answerer.append(ransac.score(np.array(user_count).reshape(-1, 1)[inlier_mask], np.array(answerer_count).reshape(-1, 1)[inlier_mask]))

        ransac = linear_model.RANSACRegressor()
        ransac.fit(np.array(user_count).reshape(-1, 1), np.array(commenter_count).reshape(-1, 1))
        inlier_mask = ransac.inlier_mask_
        r_commenter.append(ransac.score(np.array(user_count).reshape(-1, 1)[inlier_mask], np.array(commenter_count).reshape(-1, 1)[inlier_mask]))


        current_site = row[0]
        
        asker_count[:] = []
        answerer_count[:] = []
        commenter_count[:] = []
        user_count[:] = []
        
        asker_count.append(int(row[6]))
        answerer_count.append(int(row[7]))
        commenter_count.append(int(row[12]))
        user_count.append(int(row[14]))

df = pd.DataFrame({'Asker': r_asker, 'Answerer': r_answerer, 'Commenter': r_commenter})
ax = sns.lvplot(data = df, palette=sns.mpl_palette("gist_yarg"))
ax.set(ylabel='Coeff. of Determination, $R^2$')
ax.set_yticks(np.arange(0.0, 1.0, 0.05), minor=True)
sns.despine(offset = 10, trim=True, bottom = True)
sns.plt.tight_layout()
plt.savefig('User_to_Roles_R_Squared_LV.pdf')

