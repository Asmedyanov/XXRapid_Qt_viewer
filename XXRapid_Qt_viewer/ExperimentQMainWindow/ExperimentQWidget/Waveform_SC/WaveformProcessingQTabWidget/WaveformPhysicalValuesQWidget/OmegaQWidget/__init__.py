from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class OmegaQWidget(MatplotlibSingeAxTwinxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Power'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.CurrentQWidget = self.parent.CurrentQWidget
        self.I2dotQWidget = self.parent.I2dotQWidget

        self.u_resistive_function = self.ResistiveVoltageQWidget.resistive_voltage_function
        self.current_function = self.CurrentQWidget.current_function
        self.df_current = self.CurrentQWidget.current_df_to_plot.copy()
        self.df_u_resistive = self.ResistiveVoltageQWidget.df_resistive_voltage.copy()
        self.ind_peak_time = self.ResistiveVoltageQWidget.idot_peak_time
        super().__init__()
        self.ax.set(
            xlabel='t, us',
            ylabel='P, GW',
            title='Power'
        )
        self.ax_2.set(
            ylabel='I, kA',
        )
        self.df_current_to_plot = self.get_df_current_to_plot()
        self.power_function_vect = np.vectorize(self.power_function)
        self.df_power = self.get_df_power()
        self.CurrentLine, = self.ax_2.plot(self.df_current_to_plot['time'] * 1e6,
                                           self.df_current_to_plot['Units'] * 1e-3, ':r')
        self.PowerLine, = self.ax.plot(self.df_power['time'] * 1e6, self.df_power['Units'] * 1e-9)

    def get_df_power(self):
        return pd.DataFrame({
            'time': self.df_u_resistive['time'],
            'Units': np.where(self.df_u_resistive['time'].values < self.ind_peak_time, 0,
                              self.power_function_vect(self.df_u_resistive['time'].values))
        })

    def get_df_current_to_plot(self):
        return pd.DataFrame({
            'time': self.df_current['time'],
            'Units': np.where(self.df_current['Units'].values < 0, 0, self.df_current['Units'].values)
        })

    def get_df_u_resistive_to_plot(self):
        return pd.DataFrame({
            'time': self.df_u_resistive['time'],
            'Units': np.where(self.df_u_resistive['Units'].values < 0, 0, self.df_u_resistive['Units'].values)
        })

    def power_function(self, time):
        ret = self.u_resistive_function(time) * self.current_function(time)
        return ret

    def refresh(self):
        self.df_current = self.CurrentQWidget.current_df_to_plot.copy()
        self.df_u_resistive = self.ResistiveVoltageQWidget.df_resistive_voltage.copy()
        self.ind_peak_time = self.ResistiveVoltageQWidget.idot_peak_time
        self.df_power = self.get_df_power()
        self.CurrentLine.set_data(self.df_current_to_plot['time'] * 1e6, self.df_current_to_plot['Units'] * 1e-3)
        self.PowerLine.set_data(self.df_power['time'] * 1e6, self.df_power['Units'] * 1e-9)
        super().changed.emit()

    def save_report(self):
        self.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')
        self.df_power.to_csv(f'{self.parent.report_path}/{self.settings_key}.csv')

    def save_origin_pro(self, op):
        workbook = op.new_book(lname=self.settings_key)
        current_sheet = workbook.add_sheet(name='Current')
        current_sheet.from_df(self.df_current_to_plot)
        power_sheet = workbook.add_sheet(name='Power')
        power_sheet.from_df(self.df_power)
        graph = op.new_graph(template='DOUBLEY', lname=self.settings_key)
        power_plot = graph[0].add_plot(power_sheet, type='line', colx=0, coly=1)
        current_plot = graph[1].add_plot(current_sheet, type='line', colx=0, coly=1)

        graph[0].rescale()
        graph[1].rescale()

        self.parent.graph_e_p[0].add_plot(power_sheet, type='line', colx=0, coly=1)
        self.parent.graph_e_p[0].rescale()
