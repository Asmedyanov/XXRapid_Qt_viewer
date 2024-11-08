from .Settings import *
from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *


class WaveformTimingQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Timing'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        # self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.WaveformChannelsQTabWidget = self.parent.WaveformChannelsQTabWidget
        self.WaveformChannelsQTabWidget.changed.connect(self.refresh)
        self.physical_df_dict = self.WaveformChannelsQTabWidget.PhysicalDFDict
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=Settings(self)
        )
        self.max_time = self.get_max_time()
        self.normed_df_dict = self.get_normed_dict()
        self.MPLQWidget.ax.set(
            xlabel='t, ns',
            ylabel='Unit',
            title='Waveform timing'
        )
        self.Normed_plots_dict = dict()
        for my_key, my_df in self.normed_df_dict.items():
            self.Normed_plots_dict[my_key], = self.MPLQWidget.ax.plot(
                # my_df['time'].loc[my_df['time'] < self.max_time] * 1.0e9,
                # my_df['Units'].loc[my_df['time'] < self.max_time], label=my_key)
                my_df['time'] * 1.0e9,
                my_df['Units'], label=my_key)
        self.MPLQWidget.ax.legend()
        self.t_start = self.SettingsBox.StartLine.value * 1e-9
        self.t_end = self.SettingsBox.EndLine.value * 1e-9
        color = 0
        self.PulseStartLine = self.MPLQWidget.ax.axvline(self.t_start * 1e9, linestyle=':', c=f'{color}')
        color += 0.08
        self.EndLine = self.MPLQWidget.ax.axvline(self.t_end * 1e9, linestyle=':', c=f'{color}')
        self.t_shutter_dict = dict()
        self.ShutterLineDict = dict()
        self.time_list = [self.t_start]
        for my_key, my_shutter in self.SettingsBox.shutters_line_dict.items():
            color += 0.08
            self.t_shutter_dict[my_key] = my_shutter.value * 1e-9
            self.time_list.append(my_shutter.value * 1e-9)
            self.ShutterLineDict[my_key] = self.MPLQWidget.ax.axvline(self.t_shutter_dict[my_key] * 1e9, linestyle=':',
                                                                      c=f'{color}')
        self.period_quart_array = np.gradient(self.time_list)
        self.omega = np.pi / 2 / self.period_quart_array

        pass

    def refresh(self):
        self.physical_df_dict = self.WaveformChannelsQTabWidget.PhysicalDFDict
        try:
            self.max_time = self.get_max_time()
            self.normed_df_dict = self.get_normed_dict()
        except Exception as ex:
            print(ex)
            return
        for my_key, my_df in self.normed_df_dict.items():
            df_to_plot = my_df.loc[((my_df['time'] > 0) & (my_df['time'] < self.max_time))]
            self.Normed_plots_dict[my_key].set_data(df_to_plot['time'] * 1e9, df_to_plot['Units'])
        self.on_settings_box()

    def on_settings_box(self):
        self.t_start = self.SettingsBox.StartLine.value * 1e-9
        self.t_end = self.SettingsBox.EndLine.value * 1e-9
        self.PulseStartLine.set_xdata(self.t_start * 1e9)
        self.EndLine.set_xdata(self.t_end * 1e9)
        self.time_list = [self.t_start]
        for my_key, my_shutter in self.SettingsBox.shutters_line_dict.items():
            self.t_shutter_dict[my_key] = my_shutter.value * 1e-9
            self.ShutterLineDict[my_key].set_xdata(self.t_shutter_dict[my_key] * 1e9)
        self.period_quart_array = np.gradient(self.time_list)
        self.omega = np.pi / 2 / self.period_quart_array
        super().on_settings_box()

    def get_max_time(self):
        current_argmax = np.argmax(self.physical_df_dict['Current']['Units'].values)
        max_time = self.physical_df_dict['Current']['time'][current_argmax]
        return max_time * 1.5

    def get_normed_dict(self):
        normed_df_dict = {

            'Current': pd.DataFrame({
                'time': self.physical_df_dict['Current']['time'],
                'Units': np.abs(self.physical_df_dict['Current']['Units'] / self.physical_df_dict['Current'][
                    'Units'].max())
            }),

        }
        return normed_df_dict

    def save_report(self):
        self.MPLQWidget.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')

    def save_origin_pro(self, op):
        workbook = op.new_book(lname=self.settings_key)
        graph = op.new_graph(lname=self.settings_key)
        for my_key, my_df in self.normed_df_dict.items():
            sheet = workbook.add_sheet(name=my_key)
            sheet.from_df(my_df)
            plot = graph[0].add_plot(sheet, colx=0, coly=1)
            plot.name = my_key
        graph[0].rescale()
