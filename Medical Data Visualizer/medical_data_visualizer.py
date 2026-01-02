import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Import the data from medical_examination.csv and assign it to the df variable
df = pd.read_csv(os.path.join(script_dir, 'medical_examination.csv'))

# 2. Add an overweight column to the data
# Calculate BMI: weight (kg) / (height (m))^2
# Height is in cm, so convert to meters by dividing by 100
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# 3. Normalize data by making 0 always good and 1 always bad
# If cholesterol or gluc is 1, set to 0. If more than 1, set to 1.
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


def draw_cat_plot():
    # 4. Draw the Categorical Plot in the draw_cat_plot function
    
    # 5. Create a DataFrame for the cat plot using pd.melt
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )
    
    # 6. Group and reformat the data in df_cat to split it by cardio
    # Show the counts of each feature
    df_cat['value'] = df_cat['value'].astype(int)
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='count')
    
    # 7. Convert the data into long format and create a chart
    fig = sns.catplot(
        data=df_cat,
        kind='bar',
        x='variable',
        y='count',
        hue='value',
        col='cardio',
        height=5,
        aspect=1.3
    ).figure
    
    # 8. Get the figure for the output and store it in the fig variable
    fig.savefig(os.path.join(script_dir, 'catplot.png'))
    plt.close(fig)
    return fig


def draw_heat_map():
    # 9. Draw the Heat Map in the draw_heat_map function
    
    # 10. Clean the data in the df_heat variable
    df_heat = df.copy()
    
    # Filter out incorrect data:
    # - diastolic pressure is higher than systolic
    df_heat = df_heat[df_heat['ap_lo'] <= df_heat['ap_hi']]
    
    # - height is less than the 2.5th percentile
    df_heat = df_heat[df_heat['height'] >= df_heat['height'].quantile(0.025)]
    
    # - height is more than the 97.5th percentile
    df_heat = df_heat[df_heat['height'] <= df_heat['height'].quantile(0.975)]
    
    # - weight is less than the 2.5th percentile
    df_heat = df_heat[df_heat['weight'] >= df_heat['weight'].quantile(0.025)]
    
    # - weight is more than the 97.5th percentile
    df_heat = df_heat[df_heat['weight'] <= df_heat['weight'].quantile(0.975)]
    
    # 11. Calculate the correlation matrix
    corr = df_heat.corr()
    
    # 12. Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # 13. Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 14. Plot the correlation matrix using sns.heatmap()
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8}
    )
    
    # 15. Do not modify the next two lines
    fig.savefig(os.path.join(script_dir, 'heatmap.png'))
    plt.close(fig)
    return fig


# Call the functions to generate the visualizations
if __name__ == '__main__':
    draw_cat_plot()
    draw_heat_map()
