from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class ResistanceQWidget(MatplotlibSingeAxTwinxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Resistance'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.CurrentQWidget = self.parent.CurrentQWidget
        self.ResistiveVoltageQWidget = self.parent.ResistiveVoltageQWidget
        self.u_resistive_function = self.ResistiveVoltageQWidget.resistive_voltage_function
        self.current_function = self.CurrentQWidget.current_function
        self.df_current = self.CurrentQWidget.current_df_to_plot.copy()
        self.df_u_resistive = self.ResistiveVoltageQWidget.df_resistive_voltage.copy()
        self.ind_peak_time = self.ResistiveVoltageQWidget.idot_peak_time
        super().__init__()
        self.ax.set(
            xlabel='t, us',
            ylabel='R, $\\Omega$',
            title='Resistance'
        )
        self.ax_2.set(
            ylabel='I, kA',
        )
        self.df_current_to_plot = self.get_df_current_to_plot()
        self.resistance_function_vect = np.vectorize(self.resistance_function)
        self.df_resistance = self.get_df_resistance()
        self.CurrentLine, = self.ax_2.plot(self.df_current_to_plot['time'] * 1e6,
                                           self.df_current_to_plot['Units'] * 1e-3, ':r')
        self.ResistanceLine, = self.ax.plot(self.df_resistance['time'] * 1e6, self.df_resistance['Units'])

    def get_df_resistance(self):
        return pd.DataFrame({
            'time': self.df_u_resistive['time'],
            'Units': np.where(self.df_u_resistive['time'].values < self.ind_peak_time, 0,
                              self.resistance_function_vect(self.df_u_resistive['time'].values))
        })

    def get_df_current_to_plot(self):
        return pd.DataFrame({
            'time': self.df_current['time'],
            'Units': np.where(self.df_current['Units'].values < 0, 0, self.df_current['Units'].values)
        })

    def resistance_function(self, time):
        current = self.current_function(time)
        if current == 0:
            return 0
        ret = self.u_resistive_function(time) / current
        return ret

    def set_data(self, df_current, df_u_resistive, ind_peak_time=0):
        self.df_current = df_current.copy()
        self.df_u_resistive = df_u_resistive.copy()
        self.ind_peak_time = ind_peak_time
        self.df_current_to_plot = self.get_df_current_to_plot()
        self.df_u_resistive_to_plot = self.get_df_u_resistive_to_plot()
        self.resistance_function_vect = np.vectorize(self.resistance_function)
        self.df_resistance = self.get_df_resistance()
        self.CurrentLine.set_data(self.df_current_to_plot['time'] * 1e6, self.df_current_to_plot['Units'] * 1e-3)
        self.ResistanceLine.set_data(self.df_resistance['time'] * 1e6, self.df_resistance['Units'])
        self.changed.emit()

    def save_report(self, folder_name):
        if 'Resistance' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Resistance')
        super().save_report(f'{folder_name}/Resistance')
        self.df_resistance.to_csv(f'{folder_name}/Resistance/Resistance.csv')

    def refresh(self):
        self.df_current = self.CurrentQWidget.current_df_to_plot.copy()
        self.df_u_resistive = self.ResistiveVoltageQWidget.df_resistive_voltage.copy()
        self.ind_peak_time = self.ResistiveVoltageQWidget.idot_peak_time
        self.df_resistance = self.get_df_resistance()
        self.CurrentLine.set_data(self.df_current_to_plot['time'] * 1e6, self.df_current_to_plot['Units'] * 1e-3)
        self.ResistanceLine.set_data(self.df_resistance['time'] * 1e6, self.df_resistance['Units'])
        super().on_changed()
