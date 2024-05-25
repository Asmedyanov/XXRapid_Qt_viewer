import pandas as pd
import numpy as np
from MatplotlibQWidget import *


class WaveformResistanceQWidget(MatplotlibQWidget):
    def __init__(self, df_current, df_Ures, ind_peak_time=0):
        super().__init__()
        self.ax_1 = self.figure.add_subplot(111)
        self.ax_1.set(
            xlabel='t, us',
            ylabel='R, $\\Omega$',
            title='Resistance'
        )
        self.ax_2 = self.ax_1.twinx()
        self.ax_2.set(
            ylabel='I, kA',
        )
        self.ax_2.tick_params(axis='y', colors='red')
        self.df_current = pd.DataFrame({
            'time': df_current['time'],
            'Units': np.where(df_current['Units'].values < 0, 0, df_current['Units'].values)
        })
        self.df_Ures = pd.DataFrame({
            'time': df_Ures['time'],
            'Units': np.where(df_Ures['Units'].values < 0, 0, df_Ures['Units'].values)
        })
        self.ind_peak_time = ind_peak_time
        self.resistance_function_vect = np.vectorize(self.resistance_function)
        self.df_Resistance = pd.DataFrame({
            'time': df_Ures['time'],
            'Units': np.where(df_Ures['time'].values < self.ind_peak_time, 0,
                              self.resistance_function_vect(df_Ures['time'].values))
        })

        self.CurrentLine, = self.ax_2.plot(self.df_current['time'] * 1e6, self.df_current['Units'] * 1e-3, ':r')
        self.ResistanceLine, = self.ax_1.plot(self.df_Resistance['time'] * 1e6, self.df_Resistance['Units'])

    def ures_function(self, time):
        ret = np.interp(time, self.df_Ures['time'].values, self.df_Ures['Units'].values)
        return ret

    def current_function(self, time):
        ret = np.interp(time, self.df_current['time'].values, self.df_current['Units'].values)
        return ret

    def resistance_function(self, time):
        current = self.current_function(time)
        if current == 0:
            return 0
        ret = self.ures_function(time) / current
        return ret

    def set_data(self, df_current, df_Ures, ind_peak_time=0):
        self.df_current = pd.DataFrame({
            'time': df_current['time'],
            'Units': np.where(df_current['Units'].values < 0, 0, df_current['Units'].values)
        })
        self.df_Ures = pd.DataFrame({
            'time': df_Ures['time'],
            'Units': np.where(df_Ures['Units'].values < 0, 0, df_Ures['Units'].values)
        })
        self.ind_peak_time = ind_peak_time
        self.resistance_function_vect = np.vectorize(self.resistance_function)
        self.df_Resistance = pd.DataFrame({
            'time': df_Ures['time'],
            'Units': np.where(df_Ures['time'].values < self.ind_peak_time, 0,
                              self.resistance_function_vect(df_Ures['time'].values))
        })
        self.CurrentLine.set_data(self.df_current['time'] * 1e6, self.df_current['Units'] * 1e-3)
        self.ResistanceLine.set_data(self.df_Resistance['time'] * 1e6, self.df_Resistance['Units'])
        self.ax_1.relim()
        self.ax_1.autoscale_view()
        self.ax_2.relim()
        self.ax_2.autoscale_view()
        self.figure.canvas.draw()
        self.changed.emit()
