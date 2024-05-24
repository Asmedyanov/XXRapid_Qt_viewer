import pandas as pd

from MatplotlibQWidget import *
from ChannelSettingsQWidget import *
import numpy as np
from PyQt5.QtCore import pyqtSignal


class ChannelQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, my_key, df, settings_dict=None):
        super().__init__()
        self.my_key = my_key
        self.df_original = df
        self.MainQHBoxLayout = QHBoxLayout()
        self.setLayout(self.MainQHBoxLayout)
        self.MainMatplotlibQWidget = MatplotlibQWidget()
        self.MainQHBoxLayout.addWidget(self.MainMatplotlibQWidget)
        self.ChannelSettingsQWidget = ChannelSettingsQWidget(settings_dict)

        self.df_scaled = pd.DataFrame({
            'time': self.df_original['time'],
            'Units': self.df_original[
                         'Volts'] * self.ChannelSettingsQWidget.Coefficient + self.ChannelSettingsQWidget.Shift
        })
        self.SettingsDict = self.ChannelSettingsQWidget.SettingsDict
        self.ChannelSettingsQWidget.changed.connect(self.OnChannelSettingsQWidgetChanged)

        self.MainQHBoxLayout.addWidget(self.ChannelSettingsQWidget)

        self.Axis = self.MainMatplotlibQWidget.figure.add_subplot(111)
        self.Axis.set(
            xlabel='t, s',
            ylabel='Units'
        )
        self.dt = np.mean(np.gradient(self.df_original['time']))
        self.NSmooth = int(self.ChannelSettingsQWidget.TauSmooth / self.dt)

        self.df_smoothed = self.df_scaled.rolling(self.NSmooth, min_periods=1).mean()

        self.ScaledPlot, = self.Axis.plot(self.df_scaled['time'],
                                          self.df_scaled['Units'], label='Original')
        self.SmoothedPlot, = self.Axis.plot(self.df_smoothed['time'],
                                            self.df_smoothed['Units'], label='Smoothed')

        self.Axis.legend()

    def OnChannelSettingsQWidgetChanged(self):
        nsmooth = int(self.ChannelSettingsQWidget.TauSmooth / self.dt)
        self.df_scaled['Units'] = self.df_original[
                                      'Volts'] * self.ChannelSettingsQWidget.Coefficient + self.ChannelSettingsQWidget.Shift
        self.df_smoothed = self.df_scaled.rolling(nsmooth, min_periods=1).mean()
        self.SettingsDict = self.ChannelSettingsQWidget.SettingsDict

        self.SmoothedPlot.set_data(
            self.df_smoothed['time'],
            self.df_smoothed['Units']
        )
        self.ScaledPlot.set_data(
            self.df_scaled['time'],
            self.df_scaled['Units']
        )
        self.Axis.relim()
        self.Axis.autoscale_view()
        self.MainMatplotlibQWidget.figure.canvas.draw()
        self.changed.emit()

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
