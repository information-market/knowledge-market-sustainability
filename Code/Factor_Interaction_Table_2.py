import matplotlib.pyplot as plt
import matplotlib


import seaborn as sns
sns.set_context(
    "talk",
    font_scale=1,
    rc={
        "lines.linewidth": 2.0,
        "text.usetex": True,
        "font.family": 'serif',
        "font.serif": ['Palatino'],
        "font.size": 24
    })
sns.set_style('ticks')
sns.set_style({"ytick.direction": "in", "ytick.major.size": 6.0,  "ytick.minor.size": 3.0, "xtick.direction": "in", "xtick.major.size": 6.0,  "xtick.minor.size": 3.0})

from matplotlib import rc
font = {'family': 'serif', 'serif': ['Palatino'], 'size': 24}
rc('font', **font)

cmap = matplotlib.cm.get_cmap('magma')

rgb_1 = cmap(0.2)
rgb_2 = cmap(0.5)
rgb_3 = cmap(0.8)


#Plotting by seaborn
fig = plt.figure(figsize = (6, 6))
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4, 5], [1, 1, 1, 1, 1], label = '$z = 1$', color = rgb_1, linewidth = 3)
ax.plot([2, 3, 4, 5], [2, 2, 2, 2], label = '$z = 2$', color = rgb_2, linewidth = 3)
ax.plot([3, 4, 5], [3, 3, 3], label = '$z = 3$', color = rgb_3, linewidth = 3)
ax.plot([1, 1, 1, 1, 1], [1, 2, 3, 4, 5], color = rgb_1 , linewidth = 3)
ax.plot([2, 2, 2, 2], [2, 3, 4, 5], color = rgb_2, linewidth = 3)
ax.plot([3, 3, 3], [3, 4, 5], color = rgb_3, linewidth = 3)
ax.annotate('$z = 1$', xy =(1, 1), xytext=(1.2, 1.2))
ax.annotate('$z = 2$', xy =(2, 2), xytext=(2.2, 2.2))
ax.annotate('$z = 3$', xy =(3, 3), xytext=(3.2, 3.2))
ax.annotate('$z = min(y_1, y_2)$', xy =(0, 0), xytext=(1.4, 0.4))
plt.xticks([0, 1, 2, 3, 4, 5])
plt.yticks([0, 1, 2, 3, 4, 5])
ax.tick_params(axis='both', which='major', labelsize = 24)
ax.set_xlabel('$y_1$', fontsize = 24)
ax.set_ylabel('$y_2$', fontsize = 24)
plt.tight_layout()
fig.savefig('Essential.pdf', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(figsize = (6, 6))
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4, 5], [1, 0.5, 0.33, 0.25, 0.2], label = '$z = 1$', color = rgb_1 , linewidth = 3)
ax.plot([1, 1.5, 2, 3, 4, 5], [2, 1.33, 1, 0.67, 0.5, 0.4], label = '$z = 2$', color = rgb_2, linewidth = 3)
ax.plot([1, 1.5, 2, 3, 4, 5], [3, 2, 1.5, 1, 0.75, 0.6], label = '$z = 3$', color = rgb_3, linewidth = 3)
ax.plot([1, 0.5, 0.33, 0.25, 0.2], [1, 2, 3, 4, 5], color = rgb_1 , linewidth = 3)
ax.plot([1, 0.67, 0.5, 0.4], [2, 3, 4, 5], color = rgb_2, linewidth = 3)
ax.plot([1, 0.75, 0.6], [3, 4, 5], color = rgb_3, linewidth = 3)
ax.annotate('$z = 1$', xy =(1, 1), xytext=(0.5, 0.5))
ax.annotate('$z= 2$', xy =(2, 0.5), xytext=(1.0, 1.0))
ax.annotate('$z = 3$', xy =(3, 0.33), xytext=(1.5, 1.5))
ax.annotate('$z = y_1y_2$', xy =(0, 0), xytext=(3.4, 4.4))
plt.xticks([0, 1, 2, 3, 4, 5])
plt.yticks([0, 1, 2, 3, 4, 5])
ax.tick_params(axis='both', which='major', labelsize = 24)
ax.set_xlabel('$y_1$', fontsize = 24)
ax.set_ylabel('$y_2$', fontsize = 24)
plt.tight_layout()
fig.savefig('Interactive_Essential.pdf', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(figsize = (6, 6))
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4, 5], [5, 5, 5, 5, 5], label = '$z = 5$', color = rgb_3, linewidth = 3)
ax.plot([1, 2, 3, 4], [4, 4, 4, 4], label = '$z = 2$', color = rgb_2, linewidth = 3)
ax.plot([1, 2, 3], [3, 3, 3], label = '$z = 3$', color = rgb_1, linewidth = 3)
ax.plot([5, 5, 5, 5, 5], [1, 2, 3, 4, 5], color = rgb_3 , linewidth = 3)
ax.plot([4, 4, 4, 4], [1, 2, 3, 4], color = rgb_2, linewidth = 3)
ax.plot([3, 3, 3], [1, 2, 3], color = rgb_1, linewidth = 3)
ax.annotate('$z = 5$', xy =(5, 5), xytext=(3.5, 4.5))
ax.annotate('$z = 4$', xy =(4, 4), xytext=(2.5, 3.5))
ax.annotate('$z = 3$', xy =(3, 3), xytext=(1.5, 2.5))
ax.annotate('$z = max(y_1, y_2)$', xy =(0, 0), xytext=(0.4, 0.4))
plt.xticks([0, 1, 2, 3, 4, 5])
plt.yticks([0, 1, 2, 3, 4, 5])
ax.tick_params(axis='both', which='major', labelsize = 24)
ax.set_xlabel('$y_1$', fontsize = 24)
ax.set_ylabel('$y_2$', fontsize = 24)
plt.tight_layout()
fig.savefig('Antagonistic.pdf', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(figsize = (6, 6))
ax = fig.add_subplot(111)
ax.plot([0, 1], [1, 0], label = '$z = 1$', color = rgb_1 , linewidth = 3)
ax.plot([0, 3], [3, 0], label = '$z = 3$', color = rgb_2, linewidth = 3)
ax.plot([0, 5], [5, 0], label = '$z = 5$', color = rgb_3, linewidth = 3)
ax.annotate('$z = 1$', xy =(1, 1), xytext=(0.6, 0.6))
ax.annotate('$z = 3$', xy =(3, 3), xytext=(1.6, 1.6))
ax.annotate('$z = 5$', xy =(5, 5), xytext=(2.6, 2.6))
ax.annotate('$z = y_1+y_2$', xy =(0, 0), xytext=(2.4, 4.4))
plt.xticks([0, 1, 2, 3, 4, 5])
plt.yticks([0, 1, 2, 3, 4, 5])
ax.tick_params(axis='both', which='major', labelsize = 24)
ax.set_xlabel('$y_1$', fontsize = 24)
ax.set_ylabel('$y_2$', fontsize = 24)
plt.tight_layout()
fig.savefig('Substitutable.pdf', bbox_inches='tight')
plt.close(fig)





