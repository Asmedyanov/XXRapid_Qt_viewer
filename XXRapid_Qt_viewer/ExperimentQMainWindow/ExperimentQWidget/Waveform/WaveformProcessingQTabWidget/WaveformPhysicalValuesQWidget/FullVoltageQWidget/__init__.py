from MPLQWidgets.MatplotlibSingeAxQWidget import *


class FullVoltageQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Full_voltage'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.timeshift = self.parent.timeshift
        self.t_end = self.parent.t_end
        self.physical_df_dict = self.parent.physical_df_dict
        self.voltageDF = self.physical_df_dict['Voltage'].copy()
        self.voltageDF['time'] -= self.timeshift
        super().__init__()

        self.ax.set(
            xlabel='t, us',
            ylabel='$U_{full}$, kV',
            title='Full voltage'
        )
        self.voltage_df_to_plot = self.voltageDF.loc[self.voltageDF['time'] > 0]
        self.voltageLine, = self.ax.plot(self.voltage_df_to_plot['time'] * 1e6, self.voltage_df_to_plot['Units'] * 1e-3)

    def get_voltage_df_to_plot(self):
        return self.CurrentDF.loc[
            ((self.voltageDF['time'] > 0) & (self.voltageDF['time'] < self.t_end))]

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

    def save_origin_pro(self, op):
        sheet = op.new_sheet(lname=self.settings_key)
        sheet.from_df(self.voltage_df_to_plot)
        graph = op.new_graph(lname=self.settings_key)
        plot = graph[0].add_plot(sheet, colx=0, coly=1)
        graph[0].rescale()
