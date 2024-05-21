import pandas as pd

from MatplotlibQWidget import *
from ChannelSettingsQWidget import *
import scipy.signal as signal
import numpy as np


class ChannelQWidget(QWidget):
    def __init__(self, df):
        super().__init__()
        self.df_original = df
        self.MainQHBoxLayout = QHBoxLayout()
        self.setLayout(self.MainQHBoxLayout)
        self.MainMatplotlibQWidget = MatplotlibQWidget()
        self.MainQHBoxLayout.addWidget(self.MainMatplotlibQWidget)
        self.ChannelSettingsQWidget = ChannelSettingsQWidget()
        self.ChannelSettingsQWidget.changed.connect(self.OnChannelSettingsQWidgetChanged)

        self.MainQHBoxLayout.addWidget(self.ChannelSettingsQWidget)

        self.Axis = self.MainMatplotlibQWidget.figure.add_subplot(111)
        self.Axis.set(
            xlabel='t, s',
            ylabel='U, V'
        )
        self.dt = np.mean(np.gradient(self.df_original['time']))
        self.NSmooth = int(self.ChannelSettingsQWidget.TauSmooth / self.dt)

        self.df_smoothed = self.df_original.rolling(self.NSmooth, min_periods=1).mean()

        self.OriginalPlot, = self.Axis.plot(self.df_original['time'],
                                            self.df_original['Volts'], label='Original')
        self.SmoothedPlot, = self.Axis.plot(self.df_smoothed['time'],
                                            self.df_smoothed['Volts'], label='Smoothed')

        self.Axis.legend()

    def OnChannelSettingsQWidgetChanged(self):
        nsmooth = int(self.ChannelSettingsQWidget.TauSmooth / self.dt)
        self.df_smoothed = self.df_original.rolling(nsmooth, min_periods=1).mean()

        self.SmoothedPlot.set_data(
            self.df_smoothed['time'],
            self.df_smoothed['Volts']
        )
        self.Axis.relim()
        self.Axis.autoscale_view()
        self.MainMatplotlibQWidget.figure.canvas.draw()

    def set_data(self, df_original):
        self.df_original = df_original
        self.OriginalPlot.set_data(
            self.df_original['time'],
            self.df_original['Volts'],
        )
        self.dt = np.mean(np.gradient(self.df_original['time']))
        self.NSmooth = int(self.TauSmooth / self.dt)

        self.df_smoothed = self.df_original.rolling(self.NSmooth, min_periods=1).mean()

        self.SmoothedPlot.set_data(
            self.df_smoothed['time'],
            self.df_smoothed['Volts']
        )
        self.Axis.relim()
        self.Axis.autoscale_view()
