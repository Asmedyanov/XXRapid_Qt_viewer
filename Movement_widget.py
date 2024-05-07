import numpy as np

from Quart_plots_widget import Quart_plots_widget


class Movement_widget(Quart_plots_widget):
    def __init__(self):
        super().__init__()
        t = np.arange(8)
        for i in range(4):
            key = f'Quart_{i + 1}'
            self.ax[i].set(xlabel='t, us', ylabel='expansion, mm')
            self.plot_by_quarts[key].append(self.ax[i].plot(t, t, '-o')[0])
            self.plot_by_quarts[key].append(self.ax[i].plot(t, 2 * t, '-o')[0])
            self.plot_by_quarts[key].append(self.ax[i].plot(t, 3 * t, '-o')[0])

    def set_data(self, expansion_by_cross_section_dict, shutter_times):
        for i in range(4):
            key = f'Quart_{i + 1}'
            self.plot_by_quarts[key][0].set_data(shutter_times*1.0e6, expansion_by_cross_section_dict[key][0])
            self.plot_by_quarts[key][1].set_data(shutter_times*1.0e6,
                                                 expansion_by_cross_section_dict[key][
                                                     expansion_by_cross_section_dict[key].shape[0] // 2])
            self.plot_by_quarts[key][2].set_data(shutter_times*1.0e6, expansion_by_cross_section_dict[key][-1])
            self.ax[i].relim()
            self.ax[i].autoscale_view()
        self.figure.canvas.draw()
