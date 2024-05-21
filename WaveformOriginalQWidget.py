import numpy as np
import pandas as pd

from MatplotlibQWidget import *


class WaveformOriginalQWidget(MatplotlibQWidget):
    def __init__(self, filename='Default_shot/shot57.csv'):
        super().__init__()
        self.filename = filename
        self.ax = self.figure.add_subplot(111)
        self.ax.set(
            xlabel='t, sec',
            ylabel='u, V',
            title='Waveform original'
        )
        self.waveform_plots_dict = dict()
        df = pd.read_csv(self.filename)
        self.NChannels = 0
        self.ChannelDFDict = dict()
        for key in df.columns:
            if key.startswith('s'):
                self.ChannelDFDict[f'Channel_{self.NChannels + 1}'] = pd.DataFrame({'time': df[key]})
            if key.startswith('Volts'):
                self.ChannelDFDict[f'Channel_{self.NChannels + 1}']['Volts'] = df[key]
                self.NChannels += 1

        for mykey, myChannelDF in self.ChannelDFDict.items():
            self.waveform_plots_dict[mykey], = self.ax.plot(
                    myChannelDF['time'],
                    myChannelDF['Volts'],
                    label=mykey
                )
            self.ax.legend()



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

        '''for i, my_key in enumerate(self.waveform_plots_dict.keys()):
            self.waveform_dict[my_key] = df.iloc[:, 1::2].iloc[:, i].values
            self.waveform_dict[f'{my_key}_time'] = df.iloc[:, ::2].iloc[:, i].values
        for my_key, my_plot in self.waveform_plots_dict.items():
            my_plot.set_data(
                self.waveform_dict[f'{my_key}_time'],
                self.waveform_dict[f'{my_key}'],
            )'''
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()
