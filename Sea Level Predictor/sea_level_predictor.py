import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os
import numpy as np

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Import the data from epa-sea-level.csv
df = pd.read_csv(os.path.join(script_dir, 'epa-sea-level.csv'))


def draw_plot():
    # Create a copy of the data
    df_plot = df.copy()
    
    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(df_plot['Year'], df_plot['CSIRO Adjusted Sea Level'], alpha=0.5, s=30)
    
    # Get the line of best fit for all data
    slope_all, intercept_all, r_value_all, p_value_all, std_err_all = linregress(
        df_plot['Year'], df_plot['CSIRO Adjusted Sea Level']
    )
    
    # Create x values for the line of best fit (from first year to 2050)
    x_line_all = np.array([df_plot['Year'].min(), 2050])
    y_line_all = slope_all * x_line_all + intercept_all
    
    # Plot the line of best fit for all data
    ax.plot(x_line_all, y_line_all, color='red', label='Best fit line (all data)', linewidth=2)
    
    # Get the line of best fit for data from year 2000 onwards
    df_recent = df_plot[df_plot['Year'] >= 2000]
    slope_recent, intercept_recent, r_value_recent, p_value_recent, std_err_recent = linregress(
        df_recent['Year'], df_recent['CSIRO Adjusted Sea Level']
    )
    
    # Create x values for the line of best fit (from 2000 to 2050)
    x_line_recent = np.array([2000, 2050])
    y_line_recent = slope_recent * x_line_recent + intercept_recent
    
    # Plot the line of best fit for recent data
    ax.plot(x_line_recent, y_line_recent, color='green', label='Best fit line (2000 onwards)', linewidth=2)
    
    # Set labels and title
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Sea Level (inches)', fontsize=12)
    ax.set_title('Rise in Sea Level', fontsize=14)
    
    # Add legend
    ax.legend(loc='upper left')
    
    # Format the layout
    fig.tight_layout()
    
    # Save the figure
    fig.savefig(os.path.join(script_dir, 'sea_level_plot.png'))
    
    return fig


# Call the function to generate the plot
if __name__ == '__main__':
    draw_plot()
    plt.close('all')
