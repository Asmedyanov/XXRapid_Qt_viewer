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
        self.SettingsDict = self.ChannelSettingsQWidget.SettingsDict
        self.ChannelSettingsQWidget.changed.connect(self.OnChannelSettingsQWidgetChanged)
        self.MainQHBoxLayout.addWidget(self.ChannelSettingsQWidget)
        self.ax = self.MainMatplotlibQWidget.figure.add_subplot(111)
        self.ax.set(
            xlabel='t, s',
            ylabel='Units'
        )

        self.df_scaled = pd.DataFrame({
            'time': self.df_original['time'],
            'Units': self.df_original[
                         'Volts'] * self.ChannelSettingsQWidget.Coefficient + self.ChannelSettingsQWidget.Shift
        })

        self.dt = np.mean(np.gradient(self.df_original['time']))
        self.NSmooth = int(self.ChannelSettingsQWidget.TauSmooth / self.dt) + 1
        self.df_smoothed = self.df_scaled.rolling(self.NSmooth, min_periods=1).mean()
        self.ScaledPlot, = self.ax.plot(self.df_scaled['time'],
                                        self.df_scaled['Units'], label='Original')
        self.SmoothedPlot, = self.ax.plot(self.df_smoothed['time'],
                                          self.df_smoothed['Units'], label='Smoothed')

        self.ax.legend()
        self.ax.grid(ls=':')

    def OnChannelSettingsQWidgetChanged(self):
        nsmooth = int(self.ChannelSettingsQWidget.TauSmooth / self.dt)+1
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
        self.ax.relim()
        self.ax.autoscale_view()
        self.MainMatplotlibQWidget.figure.canvas.draw()
        self.changed.emit()

    def set_data(self, df_original):
        self.df_original = df_original
        self.OriginalPlot.set_data(
            self.df_original['time'],
            self.df_original['Volts'],
        )
        self.dt = np.mean(np.gradient(self.df_original['time']))
        self.NSmooth = int(self.TauSmooth / self.dt)+1

        self.df_smoothed = self.df_original.rolling(self.NSmooth, min_periods=1).mean()

        self.SmoothedPlot.set_data(
            self.df_smoothed['time'],
            self.df_smoothed['Volts']
        )
        self.ax.relim()
        self.ax.autoscale_view()

    def Save_Raport(self, folder_name):
        self.MainMatplotlibQWidget.figure.savefig(f'{folder_name}/{self.ChannelSettingsQWidget.Diagnostics}.png')
        self.df_smoothed.to_csv(f'{folder_name}/{self.ChannelSettingsQWidget.Diagnostics}.csv')
