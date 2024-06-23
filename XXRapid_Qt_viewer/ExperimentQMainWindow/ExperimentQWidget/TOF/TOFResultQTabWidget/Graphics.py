from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class Graphics(MatplotlibSingeAxTwinxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.velocity_df = self.parent.current_df
        super().__init__()
        self.ax_2.set(ylabel='Velocity, km/s', fc='r')
        self.ax_2.tick_params(axis='y', colors='red')
        self.ax.set(xlabel='width, mm', ylabel='Onset time, ns')

        self.fill_velocity = self.ax_2.fill_between(self.velocity_df['width'],
                                                    self.velocity_df['velocity'] - self.velocity_df['velocity_error'],
                                                    self.velocity_df['velocity'] + self.velocity_df['velocity_error'],
                                                    alpha=0.5, fc='r')

        self.fill_onset = self.ax.fill_between(self.velocity_df['width'],
                                               self.velocity_df['onset_time'] - self.velocity_df['onset_time_error'],
                                               self.velocity_df['onset_time'] + self.velocity_df['onset_time_error'],
                                               alpha=0.5)
        self.plot_velocity, = self.ax_2.plot(self.velocity_df['width'], self.velocity_df['velocity'], 'r')
        self.plot_onset, = self.ax.plot(self.velocity_df['width'], self.velocity_df['onset_time'])

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

    def refresh(self):
        self.velocity_df = self.parent.current_df
        '''self.fill_velocity.set_data(self.velocity_df['width'],
                                    self.velocity_df['velocity'] - self.velocity_df['velocity_error'],
                                    self.velocity_df['velocity'] + self.velocity_df['velocity_error'])
        self.fill_onset.set_data(self.velocity_df['width'],
                                 self.velocity_df['onset_time'] - self.velocity_df['onset_time_error'],
                                 self.velocity_df['onset_time'] + self.velocity_df['onset_time_error'], )'''
        self.plot_velocity.set_data(self.velocity_df['width'], self.velocity_df['velocity'])
        self.plot_onset.set_data(self.velocity_df['width'], self.velocity_df['onset_time'])
        self.changed.emit()
