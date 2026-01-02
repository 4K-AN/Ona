import unittest
import pandas as pd
import sea_level_predictor as slp
from scipy.stats import linregress
import numpy as np


class SeaLevelTestCase(unittest.TestCase):
    def setUp(self):
        self.df = slp.df.copy()

    def test_data_loaded(self):
        # Check that the data has been loaded
        self.assertIsNotNone(self.df)
        self.assertIn('Year', self.df.columns)
        self.assertIn('CSIRO Adjusted Sea Level', self.df.columns)

    def test_plot_exists(self):
        fig = slp.draw_plot()
        self.assertIsNotNone(fig)

    def test_plot_labels(self):
        fig = slp.draw_plot()
        ax = fig.axes[0]
        self.assertEqual(ax.get_xlabel(), 'Year')
        self.assertEqual(ax.get_ylabel(), 'Sea Level (inches)')
        self.assertEqual(ax.get_title(), 'Rise in Sea Level')

    def test_plot_lines(self):
        fig = slp.draw_plot()
        ax = fig.axes[0]
        # Check that there are lines in the plot (should have 2 lines of best fit)
        lines = ax.get_lines()
        self.assertGreaterEqual(len(lines), 2)

    def test_plot_scatter(self):
        fig = slp.draw_plot()
        ax = fig.axes[0]
        # Check that there is a scatter plot (collections)
        collections = ax.collections
        self.assertGreater(len(collections), 0)

    def test_predictions(self):
        # Test that predictions can be made
        # Get all data line
        slope_all, intercept_all = linregress(
            self.df['Year'], self.df['CSIRO Adjusted Sea Level']
        )[:2]
        
        # Predict for 2050
        prediction_all = slope_all * 2050 + intercept_all
        
        # Get recent data line
        df_recent = self.df[self.df['Year'] >= 2000]
        slope_recent, intercept_recent = linregress(
            df_recent['Year'], df_recent['CSIRO Adjusted Sea Level']
        )[:2]
        
        # Predict for 2050
        prediction_recent = slope_recent * 2050 + intercept_recent
        
        # Both predictions should be positive and greater than current values
        self.assertGreater(prediction_all, self.df['CSIRO Adjusted Sea Level'].max())
        self.assertGreater(prediction_recent, self.df['CSIRO Adjusted Sea Level'].max())


if __name__ == '__main__':
    unittest.main()
