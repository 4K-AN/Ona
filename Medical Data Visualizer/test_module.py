import unittest
import pandas as pd
import medical_data_visualizer as mviz


class CategoricalPlotTestCase(unittest.TestCase):
    def setUp(self):
        self.fig = mviz.draw_cat_plot()
        self.cat_plot_labels = [
            tick.get_text()
            for ax in self.fig.axes
            for tick in ax.get_xticklabels()
        ]

    def test_plot_exists(self):
        self.assertIsNotNone(self.fig)

    def test_plot_labels(self):
        self.assertEqual(
            self.cat_plot_labels,
            [
                'cholesterol',
                'gluc',
                'smoke',
                'alco',
                'active',
                'overweight',
                'cholesterol',
                'gluc',
                'smoke',
                'alco',
                'active',
                'overweight',
            ],
        )

    def test_plot_type(self):
        self.assertEqual(len(self.fig.axes), 2)


class HeatMapTestCase(unittest.TestCase):
    def setUp(self):
        self.fig = mviz.draw_heat_map()
        self.ax = self.fig.axes[0]

    def test_plot_exists(self):
        self.assertIsNotNone(self.fig)

    def test_heat_map_labels(self):
        labels = [tick.get_text() for tick in self.ax.get_xticklabels()]
        self.assertEqual(
            labels,
            [
                'id',
                'age',
                'sex',
                'height',
                'weight',
                'ap_hi',
                'ap_lo',
                'cholesterol',
                'gluc',
                'smoke',
                'alco',
                'active',
                'cardio',
                'overweight',
            ],
        )

    def test_heat_map_shape(self):
        self.assertEqual(len(self.ax.collections), 1)


if __name__ == '__main__':
    unittest.main()
