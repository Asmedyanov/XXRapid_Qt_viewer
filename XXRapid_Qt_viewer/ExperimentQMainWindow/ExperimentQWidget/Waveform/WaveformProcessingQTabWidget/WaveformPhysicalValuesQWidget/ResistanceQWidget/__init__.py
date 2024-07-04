from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class ResistanceQWidget(MatplotlibSingeAxTwinxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Resistance'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.CurrentQWidget = self.parent.CurrentQWidget
        self.ResistiveVoltageQWidget = self.parent.ResistiveVoltageQWidget
        self.ResistiveVoltageQWidget.changed.connect(self.refresh)
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
        resistance = self.resistance_function_vect(self.df_u_resistive['time'].values)
        return pd.DataFrame({
            'time': self.df_u_resistive['time'],
            'Units': np.where(self.df_u_resistive['time'].values < self.ind_peak_time, 0,

                              np.where(resistance < 0, 0, resistance))
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

    def save_report(self):
        self.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')
        self.df_resistance.to_csv(f'{self.parent.report_path}/{self.settings_key}.csv')

    def refresh(self):
        self.df_current = self.CurrentQWidget.current_df_to_plot.copy()
        self.df_u_resistive = self.ResistiveVoltageQWidget.df_resistive_voltage.copy()
        self.ind_peak_time = self.ResistiveVoltageQWidget.idot_peak_time
        self.df_resistance = self.get_df_resistance()
        self.CurrentLine.set_data(self.df_current_to_plot['time'] * 1e6, self.df_current_to_plot['Units'] * 1e-3)
        self.ResistanceLine.set_data(self.df_resistance['time'] * 1e6, self.df_resistance['Units'])
        self.changed.emit()

    def save_origin_pro(self, op):
        workbook = op.new_book(lname=self.settings_key)
        current_sheet = workbook.add_sheet(name='Current')
        current_sheet.from_df(self.df_current_to_plot)
        resistance_sheet = workbook.add_sheet(name='Resistance')
        resistance_sheet.from_df(self.df_resistance)
        graph = op.new_graph(template='DOUBLEY', lname=self.settings_key)
        resistance_plot = graph[0].add_plot(resistance_sheet, type='line', colx=0, coly=1)
        current_plot = graph[1].add_plot(current_sheet, type='line', colx=0, coly=1)

        graph[0].rescale()
        graph[1].rescale()

        try:
            self.parent.graph_c_v_r[1].add_plot(resistance_sheet, type='line', colx=0, coly=1)
            self.parent.graph_c_v_r[1].rescale()
        except Exception as ex:
            print(ex)
