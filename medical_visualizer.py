
''' Project By: Kunal Mehta #

freeCodeCamp Project3 - Data Analysis with Python Course'''

# Install Pandas seaborn numpy matplotlib

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys

# Import data
df = pd.read_csv('https://raw.githubusercontent.com/Jppbrbs/fcc-medical-data-visualizer/master/medical_examination.csv')
# Add 'overweight' column
overweight = (df['weight'] / ((df['height'] / 100)**2) > 25).astype(int)
# print(overweight)
df['overweight'] = overweight

''' Normalize data  
0: always good
1: always bad
If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
'''

df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
# print(df['cholesterol'])
df['gluc'] = (df['gluc'] > 1).astype(int)

# print(df['gluc'])
# print(df.info())


# Draw Categorical Plot
def categorical_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=[
            'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'
        ])
    # print(df_cat)
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = pd.DataFrame(
        df_cat.groupby(['cardio', 'variable',
                        'value'])['value'].count()).rename(columns={
                            'value': 'total'
                        }).reset_index()
    # print(df_cat)

    g = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar')

    fig = g.fig

    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def heat_map():
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])
                 & (df['height'] >= df['height'].quantile(0.025))
                 & (df['height'] <= df['height'].quantile(0.975))
                 & (df['weight'] >= df['weight'].quantile(0.025))
                 & (df['weight'] <= df['weight'].quantile(0.975))]

    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    fig, ax = plt.subplots(figsize=(12, 12))

    ax = sns.heatmap(
        corr,
        linewidths=.5,
        annot=True,
        fmt='.1f',
        mask=mask,
        square=True,
        center=0,
        vmin=-0.1,
        vmax=0.25,
        cbar_kws={
            'shrink': .45,
            'format': '%.2f'
        })

    fig.savefig('heatmap.png')
    return fig