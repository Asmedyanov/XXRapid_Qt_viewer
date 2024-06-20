from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *
from XXRapid_Qt_viewer.ExperimentQMainWindow.ExperimentQWidget.Waveform.WaveformProcessingQTabWidget.WaveformPhysicalValuesQWidget.ResistiveVoltageQWidget.Settings import *


class ResistiveVoltageQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Resistive_voltage'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.FullVoltageQWidget = self.parent.FullVoltageQWidget
        self.IdotQWidget = self.parent.IdotQWidget
        self.full_voltage_function = self.FullVoltageQWidget.full_voltage_function
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=Settings(self)
        )
        self.MPLQWidget.ax.set(
            xlabel='t, ns',
            ylabel='U, kV',
            title='Resistive voltage'
        )
        self.df_full_voltage = self.FullVoltageQWidget.voltage_df_to_plot.copy()
        self.df_idot = self.IdotQWidget.df_idot_smoothed_to_plot.copy()
        self.idot_peak_time = self.get_peak()
        self.idot_peak_time_line = self.MPLQWidget.ax.axvline(self.idot_peak_time * 1e9, ls=':')
        self.df_voltage_to_plot = self.get_df_voltage_to_plot()
        self.fullVoltageLine, = self.MPLQWidget.ax.plot(self.df_voltage_to_plot['time'] * 1e9,
                                                        self.df_voltage_to_plot['Units'] * 1e-3,
                                                        label='Full voltage')
        self.inductance = self.get_inductance()
        self.df_inductive_voltage = self.get_df_inductive_voltage()
        self.df_inductive_voltage_line, = self.MPLQWidget.ax.plot(self.df_inductive_voltage['time'] * 1e9,
                                                                  self.df_inductive_voltage['Units'] * 1e-3,
                                                                  label='Inductive voltage')
        self.df_resistive_voltage = self.get_df_resistive_voltage()

        self.df_resistive_voltage_line, = self.MPLQWidget.ax.plot(self.df_resistive_voltage['time'] * 1e9,
                                                                  self.df_resistive_voltage['Units'] * 1e-3,
                                                                  label='Resistive voltage')
        self.MPLQWidget.ax.legend()

    def get_df_inductive_voltage(self):
        return pd.DataFrame({
            'time': self.df_idot['time'],
            'Units': self.df_idot['Units'] * self.inductance
        })

    def get_df_resistive_voltage(self):
        return pd.DataFrame({
            'time': self.df_idot['time'],
            'Units': self.resistive_voltage_function(self.df_idot['time'].values)
        })

    def get_df_voltage_to_plot(self):
        return self.df_full_voltage.loc[self.df_full_voltage['time'] > 0]

    def get_peak(self):
        return self.SettingsBox.PeakSettingsLine.value * 1e-9

    def idot_function(self, time):
        ret = np.interp(time, self.df_idot['time'].values, self.df_idot['Units'].values)
        return ret

    def get_inductance(self):
        u_ind = self.full_voltage_function(self.idot_peak_time)
        idot_ind = self.idot_function(self.idot_peak_time)
        inductance = u_ind / idot_ind
        return inductance

    def inductive_voltage_function(self, time):
        ret = np.interp(time, self.df_inductive_voltage['time'].values, self.df_inductive_voltage['Units'].values)
        return ret

    def resistive_voltage_function(self, time):
        ret = self.full_voltage_function(time) - self.inductive_voltage_function(time)
        return ret

    def on_settings_box(self):
        self.idot_peak_time = self.get_peak()
        self.idot_peak_time_line.set_xdata(self.idot_peak_time * 1e9)
        self.df_voltage_to_plot = self.get_df_voltage_to_plot()
        self.fullVoltageLine.set_data(self.df_voltage_to_plot['time'] * 1e9,
                                      self.df_voltage_to_plot['Units'] * 1e-3, )
        self.inductance = self.get_inductance()
        self.df_inductive_voltage = self.get_df_inductive_voltage()
        self.df_inductive_voltage_line.set_data(self.df_inductive_voltage['time'] * 1e9,
                                                self.df_inductive_voltage['Units'] * 1e-3)
        self.df_resistive_voltage = self.get_df_resistive_voltage()

        self.df_resistive_voltage_line.set_data(self.df_resistive_voltage['time'] * 1e9,
                                                self.df_resistive_voltage['Units'] * 1e-3)
        self.MPLQWidget.changed.emit()
        super().on_settings_box()

    def refresh(self):

        self.df_full_voltage = self.FullVoltageQWidget.voltage_df_to_plot.copy()
        self.df_idot = self.IdotQWidget.df_idot_smoothed_to_plot.copy()
        self.on_settings_box()

    def set_data(self, df_full_voltage, df_idot):
        self.df_full_voltage = df_full_voltage.copy()
        self.df_idot = df_idot.copy()
        self.idot_peak_time = self.get_peak()
        self.idot_peak_time_line.set_xdata(self.idot_peak_time * 1.0e9)
        self.df_voltage_to_plot = self.get_df_voltage_to_plot()
        self.fullVoltageLine.set_data(self.df_voltage_to_plot['time'] * 1e9,
                                      self.df_voltage_to_plot['Units'] * 1e-3)
        self.inductance = self.get_inductance()
        self.df_inductive_voltage = self.get_df_inductive_voltage()
        self.df_inductive_voltage_line.set_data(self.df_inductive_voltage['time'] * 1e9,
                                                self.df_inductive_voltage['Units'] * 1e-3)
        self.df_resistive_voltage = self.get_df_resistive_voltage()

        self.df_resistive_voltage_line.set_data(self.df_resistive_voltage['time'] * 1e6,
                                                self.df_resistive_voltage['Units'] * 1e-3)
        self.MPLQWidget.changed.emit()

    def save_report(self, folder_name):
        if 'Resistive_voltage' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Resistive_voltage')
        super().save_report(f'{folder_name}/Resistive_voltage')
        self.df_resistive_voltage.to_csv(f'{folder_name}/Resistive_voltage/Resistive_voltage.csv')
