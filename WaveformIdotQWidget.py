import numpy as np
import pandas as pd

from MatplotlibQWidget import *
from WaveformIdotSettingsQWidget import *


class WaveformIdotQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, df_current, settings_dict=None, timeshift=0):
        super().__init__()
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.MatplotlibQWidget = MatplotlibQWidget()
        self.QHBoxLayout.addWidget(self.MatplotlibQWidget)
        self.ax = self.MatplotlibQWidget.figure.add_subplot(111)
        self.ax.set(
            xlabel='$t, \\mu s$',
            ylabel='$\\dot I, kA/ns$',

        )
        self.WaveformIdotSettingsQWidget = WaveformIdotSettingsQWidget(settings_dict)
        self.QHBoxLayout.addWidget(self.WaveformIdotSettingsQWidget)
        self.WaveformIdotSettingsQWidget.changed.connect(self.OnSettings)
        self.df_idot = pd.DataFrame({
            'time': df_current['time'],
            'Units': np.gradient(df_current['Units'].values) / np.gradient(df_current['time'].values)
        })
        self.dt = np.gradient(df_current['time'].values).mean()
        self.N_smoothing = int(self.WaveformIdotSettingsQWidget.SmoothingSettingsLine.value * 1.0e-9 / self.dt)
        self.df_idot_smoothed = self.df_idot.rolling(self.N_smoothing, min_periods=1).mean()
        self.df_idot_smoothed_to_plot = self.df_idot_smoothed.loc[self.df_idot_smoothed['time'] > 0]
        self.IdotPlot, = self.ax.plot(self.df_idot_smoothed_to_plot['time'] * 1e6,
                                      self.df_idot_smoothed_to_plot['Units'] * 1e-12)
        self.SettingsDict = self.WaveformIdotSettingsQWidget.SettingsDict

        self.Peak_time = self.WaveformIdotSettingsQWidget.PeakSettingsLine.value * 1e-9

        self.PeakPlot, = self.ax.plot([self.Peak_time * 1e6,
                                       self.Peak_time * 1e6],
                                      [self.df_idot_smoothed_to_plot['Units'].min() * 1e-12,
                                       self.df_idot_smoothed_to_plot['Units'].max() * 1e-12], '-o')

    def OnSettings(self):
        self.N_smoothing = int(self.WaveformIdotSettingsQWidget.SmoothingSettingsLine.value * 1.0e-9 / self.dt)
        self.df_idot_smoothed = self.df_idot.rolling(self.N_smoothing, min_periods=1).mean()
        self.df_idot_smoothed_to_plot = self.df_idot_smoothed.loc[self.df_idot_smoothed['time'] > 0]
        self.IdotPlot.set_data(self.df_idot_smoothed_to_plot['time'] * 1e6,
                               self.df_idot_smoothed_to_plot['Units'] * 1e-12)

        self.Peak_time = self.WaveformIdotSettingsQWidget.PeakSettingsLine.value * 1e-9

        self.PeakPlot.set_data([self.Peak_time * 1e6,
                                self.Peak_time * 1e6],
                               [self.df_idot_smoothed_to_plot['Units'].min() * 1e-12,
                                self.df_idot_smoothed_to_plot['Units'].max() * 1e-12,
                                ])

        self.ax.relim()
        self.ax.autoscale_view()
        self.MatplotlibQWidget.figure.canvas.draw()

        self.SettingsDict = self.WaveformIdotSettingsQWidget.SettingsDict
        self.changed.emit()

    def set_data(self, df_current):
        self.df_idot = pd.DataFrame({
            'time': df_current['time'],
            'Units': np.gradient(df_current['Units'].values) / np.gradient(df_current['time'].values)
        })
        self.dt = np.gradient(df_current['time'].values).mean()
        self.N_smoothing = int(self.WaveformIdotSettingsQWidget.SmoothingSettingsLine.value * 1.0e-9 / self.dt)
        self.df_idot_smoothed = self.df_idot.rolling(self.N_smoothing, min_periods=1).mean()
        self.df_idot_smoothed_to_plot = self.df_idot_smoothed.loc[self.df_idot_smoothed['time'] > 0]
        self.IdotPlot.set_data(self.df_idot_smoothed_to_plot['time'] * 1e6,
                               self.df_idot_smoothed_to_plot['Units'] * 1e-12)
        self.SettingsDict = self.WaveformIdotSettingsQWidget.SettingsDict

        self.Peak_time = self.WaveformIdotSettingsQWidget.PeakSettingsLine.value * 1e-9

        self.PeakPlot.set_data([self.Peak_time * 1e6,
                                self.Peak_time * 1e6],
                               [self.df_idot_smoothed_to_plot['Units'].min() * 1e-12,
                                self.df_idot_smoothed_to_plot['Units'].max() * 1e-12])
