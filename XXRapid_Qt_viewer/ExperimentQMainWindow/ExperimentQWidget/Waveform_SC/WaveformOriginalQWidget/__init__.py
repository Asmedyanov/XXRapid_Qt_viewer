from MPLQWidgets.MatplotlibSingeAxQWidget import *


class WaveformOriginalQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.settings_key = 'Waveform_original'
        self.parent = parent
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.folder_path = self.parent.folder_path
        self.folder_list = self.parent.folder_list
        self.file_name = self.get_file_name()
        self.df = pd.read_csv(self.file_name)
        self.NChannels = 0
        self.ChannelDFDict = self.get_channel_dict()
        super().__init__()
        self.ax.set(
            xlabel='t, sec',
            ylabel='u, V',
            title='Waveform original'
        )
        self.waveform_plots_dict = dict()
        for mykey, myChannelDF in self.ChannelDFDict.items():
            self.waveform_plots_dict[mykey], = self.ax.plot(
                myChannelDF['time'],
                myChannelDF['Volts'],
                label=mykey
            )
        self.ax.legend()

    def get_file_name(self):
        waveform_files_list = [name for name in self.folder_list if
                               name.startswith('SC') and name.endswith('csv')]
        return f'{self.folder_path}/{waveform_files_list[-1]}'

    def get_channel_dict(self):
        channels_dict = dict()
        for key in self.df.columns:
            if key.startswith('s'):
                channels_dict[f'Channel_{self.NChannels + 1}'] = pd.DataFrame({'time': self.df[key]})
            if key.startswith('Volts'):
                channels_dict[f'Channel_{self.NChannels + 1}']['Volts'] = self.df[key]
                self.NChannels += 1
        return channels_dict

    def save_report(self):
        self.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')

    def save_origin_pro(self, op):
        waveform_sheet = op.new_sheet(lname=self.settings_key)
        waveform_sheet.from_df(self.df)
        waveform_graph = op.new_graph(template='WaveformOriginal', lname=self.settings_key)
        waveform_graph[0].add_plot(waveform_sheet, colx=0, coly=1, type='line')
        waveform_graph[0].add_plot(waveform_sheet, colx=2, coly=3, type='line')
        waveform_graph[0].add_plot(waveform_sheet, colx=4, coly=5, type='line')
        waveform_graph[0].add_plot(waveform_sheet, colx=6, coly=7, type='line')
        waveform_graph[0].rescale()
