from MatplotlibQWidget import *


class XXRapidTOFVelocityQWidget(MatplotlibQWidget):
    def __init__(self, velocity_df):
        super().__init__()
        self.velocity_df = velocity_df
        gs = self.figure.add_gridspec(ncols=2)
        self.ax = gs.subplots()
        self.ax[1].set(xlabel='width, mm', ylabel='Velocity, km/s')
        self.ax[0].set(xlabel='width, mm', ylabel='Onset time, ns')

        self.fill_velocity = self.ax[1].fill_between(self.velocity_df['width'],
                                                     self.velocity_df['velocity'] - self.velocity_df['velocity_error'],
                                                     self.velocity_df['velocity'] + self.velocity_df['velocity_error'],
                                                     alpha=0.5)

        self.fill_onset = self.ax[0].fill_between(self.velocity_df['width'],
                                                  self.velocity_df['onset_time'] - self.velocity_df['onset_time_error'],
                                                  self.velocity_df['onset_time'] + self.velocity_df['onset_time_error'],
                                                  alpha=0.5)
        self.plot_velocity = self.ax[1].plot(self.velocity_df['width'], self.velocity_df['velocity'])
        self.plot_onset = self.ax[0].plot(self.velocity_df['width'], self.velocity_df['onset_time'])
        self.ax[0].grid(ls=':')
        self.ax[1].grid(ls=':')
