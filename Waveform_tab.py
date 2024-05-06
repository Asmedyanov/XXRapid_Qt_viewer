import numpy as np
from Matplotlib_qtwidget import Matplotlib_qtwidget


class Waveform_tab(Matplotlib_qtwidget):
    def __init__(self):
        super().__init__()
        t = np.arange(0, 2.0 * np.pi, 0.1)
        x = np.cos(t)
        y = np.sin(t)
        self.ax = self.figure.add_subplot(111)
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
