from .WaveformTimingSettingsQTabWidget import *
from .Settings import *
from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *


class WaveformTimingQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Timing'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.WaveformChannelsQTabWidget = self.parent.WaveformChannelsQTabWidget
        self.physical_df_dict = self.WaveformChannelsQTabWidget.PhysicalDFDict
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=Settings(self)
        )
        self.max_time = self.get_max_time()
        self.Normed_df_dict = self.get_normed_dict()
        self.MPLQWidget.ax.set(
            xlabel='t, ns',
            ylabel='Unit',
            title='Waveform timing'
        )
        self.Normed_plots_dict = dict()
        for my_key, mydf in self.Normed_df_dict.items():
            self.Normed_plots_dict[my_key], = self.MPLQWidget.ax.plot(
                mydf['time'].loc[mydf['time'] < self.max_time] * 1.0e9,
                mydf['Units'].loc[mydf['time'] < self.max_time], label=my_key)
        self.MPLQWidget.ax.legend()
        self.t_start = self.SettingsBox.StartLine.value * 1e-9
        self.PulseStartLine = self.MPLQWidget.ax.axvline(self.t_start * 1e9, linestyle=':', c='r')
        self.t_shutter_dict = dict()
        self.ShutterLineDict = dict()
        for my_key, my_shutter in self.SettingsBox.shutters_line_dict.items():
            self.t_shutter_dict[my_key] = my_shutter.value * 1e-9
            self.ShutterLineDict[my_key] = self.MPLQWidget.ax.axvline(self.t_shutter_dict[my_key] * 1e9, linestyle=':',
                                                                      c='r')

    def on_settings_box(self):
        self.t_start = self.SettingsBox.StartLine.value * 1e-9
        self.PulseStartLine.set_xdata(self.t_start * 1e9)
        for my_key, my_shutter in self.SettingsBox.shutters_line_dict.items():
            self.t_shutter_dict[my_key] = my_shutter.value * 1e-9
            self.ShutterLineDict[my_key].set_xdata(self.t_shutter_dict[my_key] * 1e9)
        super().on_settings_box()

    def get_max_time(self):
        current_argmax = np.argmax(self.physical_df_dict['Current']['Units'].values)
        max_time = self.physical_df_dict['Current']['time'][current_argmax]
        return max_time * 1.5

    def get_min_time(self):
        voltage_noise = np.abs(
            self.physical_df_dict['Voltage']['Units'].loc[self.physical_df_dict['Voltage']['time'] < 0]).max()

    def get_normed_dict(self):
        normed_df_dict = {
            'Trigger': pd.DataFrame({
                'time': self.physical_df_dict['Trigger']['time'],
                'Units': np.where(self.physical_df_dict['Trigger']['Units'] < 0,
                                  0,
                                  self.physical_df_dict['Trigger']['Units'] / self.physical_df_dict['Trigger'][
                                      'Units'].max()
                                  )
            }),
            'Current': pd.DataFrame({
                'time': self.physical_df_dict['Current']['time'],
                'Units': np.where(self.physical_df_dict['Current']['Units'] < 0,
                                  0,
                                  self.physical_df_dict['Current']['Units'] / self.physical_df_dict['Current'][
                                      'Units'].max()
                                  )
            }),
            'Voltage': pd.DataFrame({
                'time': self.physical_df_dict['Voltage']['time'],
                'Units': np.where(self.physical_df_dict['Voltage']['Units'] < 0,
                                  0,
                                  self.physical_df_dict['Voltage']['Units'] / self.physical_df_dict['Voltage'][
                                      'Units'].max()
                                  )
            }),

        }
        return normed_df_dict

    def set_data(self, physical_df_dict):
        self.physical_df_dict = physical_df_dict
        self.max_time = self.get_max_time()
        self.Normed_df_dict = self.get_normed_dict()
        for mykey, mydf in self.Normed_df_dict.items():
            df_to_plot = mydf.loc[((mydf['time'] > 0) & (mydf['time'] < self.max_time))]
            self.Normed_plots_dict[mykey].set_data(df_to_plot['time'] * 1e9, df_to_plot['Units'])
        self.MPLQWidget.ax.relim()
        self.MPLQWidget.ax.autoscale_view()
        self.on_settings_box()

    def Save_Raport(self, folder_name):
        if 'Waveform_timing' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Waveform_timing')
        self.MatplotlibQWidget.figure.savefig(f'{folder_name}/Waveform_timing/Waveform_timing.png')
