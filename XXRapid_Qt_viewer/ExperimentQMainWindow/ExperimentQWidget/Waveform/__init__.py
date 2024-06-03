from MPLQWidgets.MatplotlibSingeAxQWidget import *


class WaveformOriginalQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, filename='Default_shot/shot57.csv'):
        super().__init__()
        self.filename = filename
        self.ax.set(
            xlabel='t, sec',
            ylabel='u, V',
            title='Waveform original'
        )
        self.waveform_plots_dict = dict()
        df = pd.read_csv(self.filename)
        self.NChannels = 0
        self.ChannelDFDict = dict()
        self.get_channel_dict(df)
        for mykey, myChannelDF in self.ChannelDFDict.items():
            self.waveform_plots_dict[mykey], = self.ax.plot(
                myChannelDF['time'],
                myChannelDF['Volts'],
                label=mykey
            )
        self.ax.legend()
        self.ax.grid(ls=':')

    def get_channel_dict(self, df):
        for key in df.columns:
            if key.startswith('s'):
                self.ChannelDFDict[f'Channel_{self.NChannels + 1}'] = pd.DataFrame({'time': df[key]})
            if key.startswith('Volts'):
                self.ChannelDFDict[f'Channel_{self.NChannels + 1}']['Volts'] = df[key]
                self.NChannels += 1

    def save_report(self, folder_name='Default_shot/QtTraceFolder'):
        if 'Waveform_original' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Waveform_original')
        self.figure.savefig(f'{folder_name}/Waveform_original/Waveform_original.png')

    def set_data(self, df):
        self.NChannels = 0
        self.ChannelDFDict = dict()
        for key in df.columns:
            if key.startswith('s'):
                self.ChannelDFDict[f'Channel_{self.NChannels + 1}'] = pd.DataFrame({'time': df[key]})
            if key.startswith('Volts'):
                self.ChannelDFDict[f'Channel_{self.NChannels + 1}']['Volts'] = df[key]
                self.NChannels += 1

        for mykey, myChannelDF in self.ChannelDFDict.items():
            try:
                self.waveform_plots_dict[mykey].set_data(
                    myChannelDF['time'],
                    myChannelDF['Volts']
                )
            except:
                self.waveform_plots_dict[mykey], = self.ax.plot(
                    myChannelDF['time'],
                    myChannelDF['Volts'],
                    label=mykey
                )
                self.ax.legend()
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()

    def __str__(self):
        return f'{self.__class__}'

    def getSettingsDict(self):
        print(self.objectName())
