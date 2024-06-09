from MPLQWidgets.MatplotlibSingeAxQWidget import *


class XXRapidTOFVelocityQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, velocity_df):
        super().__init__()
        self.velocity_df = velocity_df
        self.ax_1 = self.ax.twinx()
        self.ax_1.set(ylabel='Velocity, km/s', fc='r')
        self.ax_1.tick_params(axis='y', colors='red')
        self.ax.set(xlabel='width, mm', ylabel='Onset time, ns')

        self.fill_velocity = self.ax_1.fill_between(self.velocity_df['width'],
                                                    self.velocity_df['velocity'] - self.velocity_df['velocity_error'],
                                                    self.velocity_df['velocity'] + self.velocity_df['velocity_error'],
                                                    alpha=0.5, fc='r')

        self.fill_onset = self.ax.fill_between(self.velocity_df['width'],
                                               self.velocity_df['onset_time'] - self.velocity_df['onset_time_error'],
                                               self.velocity_df['onset_time'] + self.velocity_df['onset_time_error'],
                                               alpha=0.5)
        self.plot_velocity = self.ax_1.plot(self.velocity_df['width'], self.velocity_df['velocity'], 'r')
        self.plot_onset = self.ax.plot(self.velocity_df['width'], self.velocity_df['onset_time'])

    def set_data(self, velocity_df):
        self.velocity_df = velocity_df
        self.fill_velocity.set_data(self.velocity_df['width'],
                                    self.velocity_df['velocity'] - self.velocity_df['velocity_error'],
                                    self.velocity_df['velocity'] + self.velocity_df['velocity_error'])
        self.fill_onset.set_data(self.velocity_df['width'],
                                 self.velocity_df['onset_time'] - self.velocity_df['onset_time_error'],
                                 self.velocity_df['onset_time'] + self.velocity_df['onset_time_error'], )
        self.plot_velocity.set_data(self.velocity_df['width'], self.velocity_df['velocity'])
        self.plot_onset.set_data(self.velocity_df['width'], self.velocity_df['onset_time'])
        self.changed.emit()
