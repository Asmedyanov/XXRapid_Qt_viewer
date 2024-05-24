from MatplotlibQWidget import *


class WaveformCurrentQWidget(MatplotlibQWidget):
    def __init__(self, current_df, time_shift):
        super().__init__()
        self.CurrentDF = current_df
        self.CurrentDF['time'] -= time_shift
        self.ax = self.figure.add_subplot(111)
        self.ax.set(
            xlabel='t, us',
            ylabel='I, kA',
            title='Physical current'
        )
        current_df_to_plot = self.CurrentDF.loc[self.CurrentDF['time'] > 0]
        self.CurrentLine, = self.ax.plot(current_df_to_plot['time'] * 1e6, current_df_to_plot['Units'] * 1e-3)

    def set_data(self, current_df, time_shift):
        self.CurrentDF = current_df
        self.CurrentDF['time'] -= time_shift
        current_df_to_plot = self.CurrentDF.loc[self.CurrentDF['time'] > 0]
        self.CurrentLine.set_data(current_df_to_plot['time'] * 1e6, current_df_to_plot['Units'] * 1e-3)

