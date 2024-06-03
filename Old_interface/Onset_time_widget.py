from Quart_plots_widget import Quart_plots_widget


class Onset_time_widget(Quart_plots_widget):
    def __init__(self):
        super().__init__()
        for i in range(4):
            key = f'Quart_{i + 1}'
            self.ax[i].set(xlabel='x, mm', ylabel='onset time, ns')
            self.plot_by_quarts[key] = [self.ax[i].plot([0, 0], [0, 0])[0],
                                        self.ax[i].plot([0, 0], [0, 0])[0],
                                        self.ax[i].plot([0, 0], [0, 0])[0]]

    def set_data(self, approximation_df):
        for i in range(4):
            key = f'Quart_{i + 1}'
            self.plot_by_quarts[key][0].set_data(
                approximation_df[key]['x'] * 1.0e3,
                approximation_df[key]['onset_time'] * 1.0e9,
            )
            self.plot_by_quarts[key][1].set_data(
                approximation_df[key]['x'] * 1.0e3,
                (approximation_df[key]['onset_time'] - approximation_df[key]['onset_time_error']) * 1.0e9,
            )
            self.plot_by_quarts[key][2].set_data(
                approximation_df[key]['x'] * 1.0e3,
                (approximation_df[key]['onset_time'] + approximation_df[key]['onset_time_error']) * 1.0e9,
            )
            self.ax[i].relim()
            self.ax[i].autoscale_view()
        self.figure.canvas.draw()
        self.changed.emit()
