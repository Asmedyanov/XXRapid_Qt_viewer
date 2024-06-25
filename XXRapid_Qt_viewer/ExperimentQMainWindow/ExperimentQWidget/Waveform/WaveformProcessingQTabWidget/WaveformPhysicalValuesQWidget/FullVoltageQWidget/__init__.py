from MPLQWidgets.MatplotlibSingeAxQWidget import *


class FullVoltageQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Full_voltage'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.timeshift = self.parent.timeshift
        self.physical_df_dict = self.parent.physical_df_dict
        self.voltageDF = self.physical_df_dict['Voltage'].copy()
        self.voltageDF['time'] -= self.timeshift
        super().__init__()

        self.ax.set(
            xlabel='t, us',
            ylabel='$U_{full}$, kV',
            title='Physical full voltage'
        )
        self.voltage_df_to_plot = self.voltageDF.loc[self.voltageDF['time'] > 0]
        self.voltageLine, = self.ax.plot(self.voltage_df_to_plot['time'] * 1e6, self.voltage_df_to_plot['Units'] * 1e-3)

    def set_data(self, voltage_df, time_shift):
        self.voltageDF = voltage_df.copy()
        self.voltageDF['time'] -= time_shift
        self.voltage_df_to_plot = self.voltageDF.loc[self.voltageDF['time'] > 0]
        self.voltageLine.set_data(self.voltage_df_to_plot['time'] * 1e6, self.voltage_df_to_plot['Units'] * 1e-3)
        self.changed.emit()

    def save_report(self):
        self.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')
        self.voltage_df_to_plot.to_csv(f'{self.parent.report_path}/{self.settings_key}.csv')

    def refresh(self):
        self.timeshift = self.parent.timeshift
        self.physical_df_dict = self.parent.physical_df_dict
        self.voltageDF = self.physical_df_dict['Voltage'].copy()
        self.voltageDF['time'] -= self.timeshift
        self.voltage_df_to_plot = self.voltageDF.loc[self.voltageDF['time'] > 0]
        self.voltageLine.set_data(self.voltage_df_to_plot['time'] * 1e6, self.voltage_df_to_plot['Units'] * 1e-3)
        self.changed.emit()

    def full_voltage_function(self, time):
        ret = np.interp(time, self.voltageDF['time'].values, self.voltageDF['Units'].values)
        return ret
