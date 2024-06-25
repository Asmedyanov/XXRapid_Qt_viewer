from MPLQWidgets.MatplotlibSingeAxQWidget import *


class CurrentQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Current'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.timeshift = self.parent.timeshift
        self.physical_df_dict = self.parent.physical_df_dict
        self.CurrentDF = self.physical_df_dict['Current'].copy()
        self.CurrentDF['time'] -= self.timeshift
        super().__init__()
        self.ax.set(
            xlabel='t, us',
            ylabel='I, kA',
            title='Physical current'
        )
        self.current_df_to_plot = self.CurrentDF.loc[self.CurrentDF['time'] > 0]
        self.CurrentLine, = self.ax.plot(self.current_df_to_plot['time'] * 1e6, self.current_df_to_plot['Units'] * 1e-3)

    def refresh(self):
        self.timeshift = self.parent.timeshift
        self.physical_df_dict = self.parent.physical_df_dict
        self.CurrentDF = self.physical_df_dict['Current'].copy()
        self.CurrentDF['time'] -= self.timeshift
        self.current_df_to_plot = self.CurrentDF.loc[self.CurrentDF['time'] > 0]
        self.CurrentLine.set_data(self.current_df_to_plot['time'] * 1e6, self.current_df_to_plot['Units'] * 1e-3)
        self.changed.emit()

    def set_data(self, current_df, time_shift):
        self.CurrentDF = current_df.copy()
        self.CurrentDF['time'] -= time_shift
        self.current_df_to_plot = self.CurrentDF.loc[self.CurrentDF['time'] > 0]
        self.CurrentLine.set_data(self.current_df_to_plot['time'] * 1e6, self.current_df_to_plot['Units'] * 1e-3)
        self.changed.emit()

    def save_report(self):
        self.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')
        self.current_df_to_plot.to_csv(f'{self.parent.report_path}/{self.settings_key}.csv')

    def current_function(self, time):
        ret = np.interp(time, self.CurrentDF['time'].values, self.CurrentDF['Units'].values)
        return ret
