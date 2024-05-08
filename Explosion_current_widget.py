from Quart_plots_widget import Quart_plots_widget
import numpy as np
import pandas as pd


class Explosion_current_widget(Quart_plots_widget):
    def __init__(self):
        super().__init__()
        self.explosion_current_dict = dict()
        for i in range(4):
            key = f'Quart_{i + 1}'
            self.ax[i].set(xlabel='x, mm', ylabel='I, kA')
            self.plot_by_quarts[key], = self.ax[i].plot([0, 0], [0, 0])

    def set_data(self, explosion_time_dict, df_current):
        def f_current(t):
            ret = np.interp(t, df_current['time'], df_current['value'])
            return ret

        for i in range(4):
            key = f'Quart_{i + 1}'
            t_data = explosion_time_dict[key]['onset_time'].values
            x_data = explosion_time_dict[key]['x'].values
            current_data = f_current(t_data)
            self.explosion_current_dict[key] = pd.DataFrame(
                {
                    'x': x_data,  # m
                    'current': current_data  # A
                }
            )
            self.plot_by_quarts[key].set_data(x_data * 1.0e3, current_data * 1.0e-3)
            self.ax[i].relim()
            self.ax[i].autoscale_view()
        self.figure.canvas.draw()
        self.changed.emit()
