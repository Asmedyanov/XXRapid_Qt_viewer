from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


class Waveform(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        t = np.arange(0, 2.0 * np.pi, 0.1)
        x = np.cos(t)
        y = np.sin(t)
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.figure.set_layout_engine(layout='tight')
        self.ax.set(
            xlabel='t, sec',
            ylabel='u, V',
            title='Waveform original'
        )
        self.waveform_plots_dict = dict()
        for i in range(4):
            self.waveform_plots_dict[f'channel_{i}'], = self.ax.plot(
                x * (i + 1),
                y * (i + 1),
                label=f'channel_{i}')
        self.ax.legend()

        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.waveform_dict = dict()

    def set_data(self, df):
        for i, my_key in enumerate(self.waveform_plots_dict.keys()):
            self.waveform_dict[my_key] = df.iloc[:, 1::2].iloc[:, i].values
            self.waveform_dict[f'{my_key}_time'] = df.iloc[:, ::2].iloc[:, i].values
        for my_key, my_plot in self.waveform_plots_dict.items():
            my_plot.set_data(
                self.waveform_dict[f'{my_key}_time'],
                self.waveform_dict[f'{my_key}'],
            )
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()
