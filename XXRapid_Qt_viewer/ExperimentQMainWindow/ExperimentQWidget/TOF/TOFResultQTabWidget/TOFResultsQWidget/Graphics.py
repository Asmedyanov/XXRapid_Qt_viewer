from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class Graphics(MatplotlibSingeAxTwinxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.velocity_df = self.parent.velocity_smoothed_df
        super().__init__()
        self.ax_2.set(ylabel='Velocity, km/s', fc='r')
        self.ax_2.tick_params(axis='y', colors='red')
        self.ax.set(xlabel='width, mm', ylabel='Onset time, ns')

        '''self.fill_velocity = self.ax_2.fill_between(self.velocity_df['width'],
                                                    self.velocity_df['velocity'] - self.velocity_df['velocity_error'],
                                                    self.velocity_df['velocity'] + self.velocity_df['velocity_error'],
                                                    alpha=0.5, fc='r')

        self.fill_onset = self.ax.fill_between(self.velocity_df['width'],
                                               self.velocity_df['onset_time'] - self.velocity_df['onset_time_error'],
                                               self.velocity_df['onset_time'] + self.velocity_df['onset_time_error'],
                                               alpha=0.5)'''
        self.plot_velocity, = self.ax_2.plot(self.velocity_df['width'], self.velocity_df['velocity'], 'r')
        self.plot_velocity_up, = self.ax_2.plot(self.velocity_df['width'],
                                                self.velocity_df['velocity'] + self.velocity_df['velocity_error'], 'r')
        self.plot_velocity_down, = self.ax_2.plot(self.velocity_df['width'],
                                                  self.velocity_df['velocity'] - self.velocity_df['velocity_error'],
                                                  'r')
        self.plot_onset, = self.ax.plot(self.velocity_df['width'], self.velocity_df['onset_time'], 'b')
        self.plot_onset_up, = self.ax.plot(self.velocity_df['width'],
                                           self.velocity_df['onset_time'] + self.velocity_df['onset_time_error'], 'b')
        self.plot_onset_down, = self.ax.plot(self.velocity_df['width'],
                                             self.velocity_df['onset_time'] - self.velocity_df['onset_time_error'], 'b')

    def refresh(self):
        self.velocity_df = self.parent.velocity_smoothed_df
        self.plot_velocity.set_data(self.velocity_df['width'], self.velocity_df['velocity'])
        self.plot_velocity_up.set_data(self.velocity_df['width'],
                                       self.velocity_df['velocity'] + self.velocity_df['velocity_error'])
        self.plot_velocity_down.set_data(self.velocity_df['width'],
                                         self.velocity_df['velocity'] - self.velocity_df['velocity_error'])
        self.plot_onset.set_data(self.velocity_df['width'], self.velocity_df['onset_time'])
        self.plot_onset_up.set_data(self.velocity_df['width'],
                                    self.velocity_df['onset_time'] + self.velocity_df['onset_time_error'])
        self.plot_onset_down.set_data(self.velocity_df['width'],
                                      self.velocity_df['onset_time'] - self.velocity_df['onset_time_error'])
        self.changed.emit()
