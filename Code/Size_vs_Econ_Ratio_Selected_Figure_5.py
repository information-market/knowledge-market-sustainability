import csv
import math
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn import linear_model
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
sns.set_style({"ytick.direction": "in", "ytick.major.size": 6.0,  "ytick.minor.size": 3.0, "xtick.direction": "in", "xtick.major.size": 6.0,  "xtick.minor.size": 3.0})

from matplotlib import rc
font = {'family': 'serif', 'serif': ['Palatino'], 'size': 18}
rc('font', **font)

plt.rcParams["figure.figsize"] = (24, 12)

cmap = matplotlib.cm.get_cmap('magma')
rgb = cmap(0.5)

def cobb_douglas_answer(x, A, lambda_0, lambda_1):
    return A * np.power(x[0], lambda_0) * np.power(x[1], lambda_1)

def cobb_douglas_question(x, A, lambda_0):
    return A * np.power(x, lambda_0)


df_column_site = []
df_column_size = []
df_column_metric = []
df_plot_x = []
df_plot_y = []


data_file = open('Figure_Datasets/Site_Monthly_Stats_Selected_with_Dummy.csv')
csv_data = csv.reader(data_file)


first_row = next(csv_data)
current_site = first_row[0]

month_no_of_questions = []
month_no_of_answers = []
month_no_of_askers = []
month_no_of_answerers = []
month_no_of_users = []

month_no_of_questions.append(int(first_row[2]))
month_no_of_answers.append(int(first_row[3]))
month_no_of_askers.append(int(first_row[6]))
month_no_of_answerers.append(int(first_row[7]))
month_no_of_users.append(int(first_row[16]))

for row in csv_data:

    if row[0] == current_site:
        month_no_of_questions.append(int(row[2]))
        month_no_of_answers.append(int(row[3]))
        month_no_of_askers.append(int(row[6]))
        month_no_of_answerers.append(int(row[7]))
        month_no_of_users.append(int(row[16]))
        
    else:

        if len(month_no_of_questions) >= 24:
            print current_site

            optimal_parameters_question, covariance_of_parameters_question = curve_fit(cobb_douglas_question, month_no_of_askers, month_no_of_questions)
            answer_factors = np.array([month_no_of_questions, month_no_of_answerers])
            optimal_parameters_answer, covariance_of_parameters_answer = curve_fit(cobb_douglas_answer, answer_factors, month_no_of_answers, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))
            print  optimal_parameters_question, optimal_parameters_answer

            month_fraction_of_askers = [float(a)/b for a,b in zip(month_no_of_askers, month_no_of_users)]
            month_fraction_of_answerers = [float(a)/b for a,b in zip(month_no_of_answerers, month_no_of_users)]

            month_no_of_users_sorted = sorted(month_no_of_users)

            ransac = linear_model.RANSACRegressor()
            ransac.fit(np.array(month_no_of_users).reshape(-1, 1), np.array(month_no_of_askers).reshape(-1, 1))
            print ransac.estimator_.coef_
            month_potential_no_of_askers = ransac.predict(np.array(month_no_of_users_sorted).reshape(-1, 1))

            ransac_2 = linear_model.RANSACRegressor()
            ransac_2.fit(np.array(month_no_of_users).reshape(-1, 1), np.array(month_no_of_answerers).reshape(-1, 1))
            print ransac_2.estimator_.coef_
            month_potential_no_of_answerers =  ransac_2.predict(np.array(month_no_of_users_sorted).reshape(-1, 1))

            month_potential_no_of_questions = cobb_douglas_question(month_potential_no_of_askers, *optimal_parameters_question)
            month_potential_no_of_answers = cobb_douglas_answer(np.array([month_potential_no_of_questions, month_potential_no_of_answerers]), *optimal_parameters_answer)

            metric = [float(a)/b for a,b in zip(month_no_of_answers, month_no_of_questions)]

            metric_sorted =  [float(a)/b for a,b in zip(month_potential_no_of_answers, month_potential_no_of_questions)]

            df_column_site +=  len(month_no_of_users)* [current_site]
            df_column_size.extend(month_no_of_users)
            df_column_metric.extend(metric)
            df_plot_x.append(month_no_of_users_sorted)
            df_plot_y.append(metric_sorted)

            
        current_site = row[0]
        
        month_no_of_questions[:] = []
        month_no_of_answers[:] = []
        month_no_of_askers[:] = []
        month_no_of_answerers[:] = []
        month_no_of_users[:] = []

        month_no_of_questions.append(int(row[2]))
        month_no_of_answers.append(int(row[3]))
        month_no_of_askers.append(int(row[6]))
        month_no_of_answerers.append(int(row[7]))
        month_no_of_users.append(int(row[16]))

print min(df_column_metric), max(df_column_metric)

plt.clf()
df = pd.DataFrame({'Site': df_column_site, 'System Size': df_column_size, '$N_a/N_q$': df_column_metric})
g = sns.FacetGrid(df, col = 'Site', sharex = False)
#scatter_kws = {'alpha':0.25, 'color':'k', 's':50}
g.map(sns.regplot, 'System Size', '$N_a/N_q$', scatter_kws = {'alpha':0.125, 'color':'k'}, logx = True, truncate = True)
g.fig.subplots_adjust(wspace = 0, hspace = 0)

g.axes[0, 0].set_ylabel('Econ. Ratio, $N_{a/q}$')

g.axes[0, 0].set_xlabel('# of Users, $U$')
g.axes[0, 1].set_xlabel('# of Users, $U$')
g.axes[0, 2].set_xlabel('# of Users, $U$')

g.axes[0, 0].set_title('SUPERUSER')
g.axes[0, 1].set_title('PUZZLING')
g.axes[0, 2].set_title('CSTHEORY')

major_yticks = np.arange(0.6, 3.5, 0.7)
minor_yticks = np.arange(0.6, 3.5, 0.14)
axes_count = 0
for ax in g.axes[-1, :]:
    ax.set_yticks(major_yticks)
    ax.set_yticks(minor_yticks, minor = True)
    if axes_count == 0:
        major_xticks = np.arange(2000, 8010, 1500)
        minor_xticks = np.arange(2000, 8000, 300)
        ax.plot(df_plot_x[0], df_plot_y[0], color = rgb, label = 'Cobb-Douglas')
    elif axes_count == 1:
        major_xticks = np.arange(200, 1010, 200)
        minor_xticks = np.arange(200, 1000, 40)
        ax.plot(df_plot_x[1], df_plot_y[1], color = rgb, label = 'Cobb-Douglas')
    elif axes_count == 2:
        major_xticks = np.arange(100, 310, 50)
        minor_xticks = np.arange(100, 300, 10)       
        ax.plot(df_plot_x[2], df_plot_y[2], color = rgb, label = 'Cobb-Douglas') 
    
    ax.legend()
    ax.set_xticks(major_xticks)
    ax.set_xticks(minor_xticks, minor = True)     
    axes_count += 1

#g.set(xlabel = '')
sns.despine(trim=True, offset = 10)
sns.plt.tight_layout()
plt.savefig('Size_vs_Econ_Ratio.pdf', bbox_inches='tight')
plt.close()

