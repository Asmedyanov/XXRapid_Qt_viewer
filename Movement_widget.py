import numpy as np

from Quart_plots_widget import Quart_plots_widget
import pandas as pd


class Movement_widget(Quart_plots_widget):
    def __init__(self):
        super().__init__()
        t = np.arange(8)
        for i in range(4):
            key = f'Quart_{i + 1}'
            self.ax[i].set(xlabel='t, us', ylabel='expansion, mm')
            for j in range(3):
                self.plot_by_quarts[key].append(
                    [self.ax[i].plot(t, (j + 1) * t, '-o')[0],
                     self.ax[i].plot(t, (j + 1) * t, )[0]]
                )

    def set_data(self, expansion_by_cross_section_dict, shutter_times, dx):
        approximation_dict = {}
        for i in range(4):
            key = f'Quart_{i + 1}'
            cross_section_number = expansion_by_cross_section_dict[key].shape[0]
            self.plot_by_quarts[key][0][0].set_data(shutter_times * 1.0e6, expansion_by_cross_section_dict[key][0])
            self.plot_by_quarts[key][1][0].set_data(shutter_times * 1.0e6,
                                                    expansion_by_cross_section_dict[key][cross_section_number // 2])
            self.plot_by_quarts[key][2][0].set_data(shutter_times * 1.0e6, expansion_by_cross_section_dict[key][-1])

            onset_time_list = []
            onset_time_error_list = []
            velocity_list = []
            velocity_error_list = []
            for j in range(cross_section_number):
                t_data = []
                expansion_data = []

                for k in range(8):
                    if expansion_by_cross_section_dict[key][j][k] == 0:
                        try:
                            if expansion_by_cross_section_dict[key][j + 1][k] == 0:
                                continue
                        except:
                            continue
                    t_data.append(shutter_times[k])
                    expansion_data.append(expansion_by_cross_section_dict[key][j][k])
                if len(t_data) < 4:
                    continue
                line_poly_coef = np.polyfit(t_data, expansion_data, 1)
                line_poly_func = np.poly1d(line_poly_coef)
                velocity = line_poly_coef[0]
                velocity_list.append(velocity)
                onset_time = -line_poly_coef[1] / velocity
                onset_time_list.append(onset_time)
                if j in [0, cross_section_number // 2, cross_section_number - 1]:
                    t_approx = np.arange(onset_time, shutter_times[-1], np.gradient(shutter_times).mean() / 10)
                    poly_y_data = line_poly_func(t_approx)
                    if j == 0:
                        self.plot_by_quarts[key][0][1].set_data(t_approx * 1.0e6, poly_y_data)
                    if j == cross_section_number // 2:
                        self.plot_by_quarts[key][1][1].set_data(t_approx * 1.0e6, poly_y_data)
                    if j == cross_section_number - 1:
                        self.plot_by_quarts[key][2][1].set_data(t_approx * 1.0e6, poly_y_data)
            approximation_dict[key] = pd.DataFrame({
                'x': np.arange(len(onset_time_list)) * dx * 1.0e-3,  # m
                'onset_time': onset_time_list,  # s
                'velocity': velocity_list,  # m/s
            })
            self.ax[i].relim()
            self.ax[i].autoscale_view()
        self.approximation_dict = approximation_dict
        self.figure.canvas.draw()
        self.changed.emit()