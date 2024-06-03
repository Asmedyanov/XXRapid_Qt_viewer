from MPLQWidgets.MatplotlibSingeAxQWidget import *


class WaveformCurrentQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, current_df, time_shift):
        super().__init__('Current')
        self.CurrentDF = current_df.copy()
        self.CurrentDF['time'] -= time_shift
        self.ax.set(
            xlabel='t, us',
            ylabel='I, kA',
            title='Physical current'
        )
        self.current_df_to_plot = self.CurrentDF.loc[self.CurrentDF['time'] > 0]
        self.CurrentLine, = self.ax.plot(self.current_df_to_plot['time'] * 1e6, self.current_df_to_plot['Units'] * 1e-3)

    def set_data(self, current_df, time_shift):
        self.CurrentDF = current_df.copy()
        self.CurrentDF['time'] -= time_shift
        self.current_df_to_plot = self.CurrentDF.loc[self.CurrentDF['time'] > 0]
        self.CurrentLine.set_data(self.current_df_to_plot['time'] * 1e6, self.current_df_to_plot['Units'] * 1e-3)
        self.changed.emit()

    def save_report(self, folder_name):
        if 'Current' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Current')
        super().save_report(f'{folder_name}/Current')
        self.current_df_to_plot.to_csv(f'{folder_name}/Current/Current.csv')
