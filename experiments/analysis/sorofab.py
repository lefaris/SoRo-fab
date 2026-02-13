# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import pandas as pd
import seaborn as sns

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The Axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

fig, ax_kwargs = plt.subplots(figsize=(6, 6))
dependency_kwargs = [[-0.8, 0.5],
                     [-0.2, 0.5]]
mu = 2, -3
scale = 6, 5

#file_path = 'allTwist.xlsx' # Change file name as needed
file_path = 'Twist_Translation.xlsx' # Change file name as needed
#B = str(file_path).split('_')[1].split('.')[0]
#ax_kwargs.set_title(B.upper())
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name, usecols='A:K')

sns.set_style("white") #Options: deep, muted, bright, pastel, dark, colorblind

# Plt the mean with cross mark
#ax_kwargs.scatter(df['Del X1'].mean(), df['Del Y1'].mean(), c='blue', s=3, marker='x')

confidence_ellipse(df['black x'], df['black y'], ax_kwargs,
                   alpha=0.4, facecolor=[166/255, 166/255, 166/255], edgecolor='black', zorder=0, label='_nolegend_')
sns.scatterplot(x='black x', y='black y', data=df, ax=ax_kwargs,color=[0/255, 0/255, 0/255],label='Black')

confidence_ellipse(df['blue x'], df['blue y'], ax_kwargs,
                   alpha=0.4, facecolor=[102/255, 102/255, 255/255], edgecolor='blue', zorder=0,label='_nolegend_')
sns.scatterplot(x='blue x', y='blue y', data=df, ax=ax_kwargs, color=[0/255, 0/255, 255/255],label='Blue')

confidence_ellipse(df['purple x'], df['purple y'], ax_kwargs,
                   alpha=0.4, facecolor=[204/255, 128/255, 255/255], edgecolor='purple', zorder=0,label='_nolegend_')
sns.scatterplot(x='purple x', y='purple y', data=df, ax=ax_kwargs,color=[153/255, 0/255, 255/255],label='Purple')

# confidence_ellipse(df['pose11'], df['pose12'], ax_kwargs,
#                    alpha=0.4, facecolor=[166/255, 166/255, 166/255], edgecolor='black', zorder=0, label='_nolegend_')
# sns.scatterplot(x='pose11', y='pose12', data=df, ax=ax_kwargs,color=[0/255, 0/255, 0/255],label='Black')

# confidence_ellipse(df['p1'], df['p2'], ax_kwargs,
#                    alpha=0.4, facecolor=[102/255, 102/255, 255/255], edgecolor='blue', zorder=0,label='_nolegend_')
# sns.scatterplot(x='p1', y='p2', data=df, ax=ax_kwargs, color=[0/255, 0/255, 255/255],label='Blue')

# confidence_ellipse(df['pur1'], df['pur2'], ax_kwargs,
#                    alpha=0.4, facecolor=[204/255, 128/255, 255/255], edgecolor='purple', zorder=0,label='_nolegend_')
# sns.scatterplot(x='pur1', y='pur2', data=df, ax=ax_kwargs,color=[153/255, 0/255, 255/255],label='Purple')

# confidence_ellipse(df['pose41'], df['pose42'], ax_kwargs,
#                    alpha=0.2, facecolor=[255/255, 194/255, 102/255], edgecolor='orange', zorder=0,label='_nolegend_')
# sns.scatterplot(x='pose41', y='pose42', data=df, ax=ax_kwargs,color=[255/255, 153/255, 0/255],label='Run4')

# confidence_ellipse(df['pose51'], df['pose52'], ax_kwargs,
#                    alpha=0.2, facecolor=[102/255, 102/255, 255/255], edgecolor='blue', zorder=0,label='_nolegend_')
# sns.scatterplot(x='pose51', y='pose52', data=df, ax=ax_kwargs,color=[0/255, 0/255, 255/255],label='Run5')




# Change legend order
# handles, labels = ax_kwargs.get_legend_handles_labels()
# h0 = handles[0]
# h2 = handles[1]
# h1 = handles[2]
# l1 = labels[0]
# l2 = labels[1]
# l0 = labels[2]
# new_order = ['0ML', '1ML', '2ML']
# ax_kwargs.legend([h0,h2,h1], [l0,l2,l1])
# handles, labels = plt.get_legend_handles_labels()
# handle_dict = dict(zip(labels, handles))
# new_handles = [handle_dict[label] for label in new_order]
# plt.legend(handles=new_handles, labels=new_order)
# plt.legend()

# axis title
ax_kwargs.set_xlabel('$\Delta$ X (cm)')
ax_kwargs.set_ylabel('$\Delta$ Y (cm)')

# bold the axis title
ax_kwargs.xaxis.label.set_fontweight('bold')
ax_kwargs.yaxis.label.set_fontweight('bold')

# increase font size
ax_kwargs.xaxis.label.set_fontsize(14)
ax_kwargs.yaxis.label.set_fontsize(14)

# increase the legend size
ax_kwargs.legend(fontsize=14)

# Increase tick size
#ax_kwargs.tick_params(axis='both', which='major', labelsize=24)

# Increase the title size
ax_kwargs.title.set_text('Body Twist Translation')
ax_kwargs.title.set_fontsize(20)
ax_kwargs.title.set_fontweight('bold')

# increase number of ticks
ax_kwargs.locator_params(axis='x', nbins=8)
ax_kwargs.locator_params(axis='y', nbins=8)

ax_kwargs.axvline(c='grey', lw=0.5)
ax_kwargs.axhline(c='grey', lw=0.5)

#legend = plt.legend(title='Robots', loc='upper left', frameon=True, shadow=True, borderpad=1)
plt.show()