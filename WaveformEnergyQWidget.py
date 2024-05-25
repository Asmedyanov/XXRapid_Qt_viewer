import pandas as pd
import numpy as np
from MatplotlibQWidget import *


class WaveformEnergyQWidget(MatplotlibQWidget):
    def __init__(self, df_current, df_Ures):
        super().__init__()
        self.ax_1 = self.figure.add_subplot(111)
        self.ax_1.set(
            xlabel='t, us',
            ylabel='E, J',
            title='Energy'
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
        self.df_Power = pd.DataFrame({
            'time': df_Ures['time'],
            'Units': self.power_function(df_Ures['time'].values)
        })
        self.dt = np.mean(np.gradient(self.df_Power['time']))
        self.energy_function_vect = np.vectorize(self.energy_function)
        self.df_Energy = pd.DataFrame({
            'time': df_Ures['time'],
            'Units': self.energy_function_vect(df_Ures['time'].values)
        })

        self.CurrentLine, = self.ax_2.plot(self.df_current['time'] * 1e6, self.df_current['Units'] * 1e-3, ':r')
        self.EnergyLine, = self.ax_1.plot(self.df_Energy['time'] * 1e6, self.df_Energy['Units'])

    def ures_function(self, time):
        ret = np.interp(time, self.df_Ures['time'].values, self.df_Ures['Units'].values)
        return ret

    def current_function(self, time):
        ret = np.interp(time, self.df_current['time'].values, self.df_current['Units'].values)
        return ret

    def power_function(self, time):
        ret = self.current_function(time) * self.ures_function(time)
        return ret

    def energy_function(self, time):
        power_to_sum = self.df_Power.loc[self.df_Power['time'] < time]
        energy = power_to_sum['Units'].sum() * self.dt
        return energy

    def set_data(self, df_current, df_Ures):
        self.df_current = pd.DataFrame({
            'time': df_current['time'],
            'Units': np.where(df_current['Units'].values < 0, 0, df_current['Units'].values)
        })
        self.df_Ures = pd.DataFrame({
            'time': df_Ures['time'],
            'Units': np.where(df_Ures['Units'].values < 0, 0, df_Ures['Units'].values)
        })
        self.df_Power = pd.DataFrame({
            'time': df_Ures['time'],
            'Units': self.power_function(df_Ures['time'].values)
        })
        self.dt = np.mean(np.gradient(self.df_Power['time']))
        self.energy_function_vect = np.vectorize(self.energy_function)
        self.df_Energy = pd.DataFrame({
            'time': df_Ures['time'],
            'Units': self.energy_function_vect(df_Ures['time'].values)
        })

        self.CurrentLine.set_data(self.df_current['time'] * 1e6, self.df_current['Units'] * 1e-3)
        self.EnergyLine.set_data(self.df_Energy['time'] * 1e6, self.df_Energy['Units'])
        self.ax_1.relim()
        self.ax_1.autoscale_view()
        self.ax_2.relim()
        self.ax_2.autoscale_view()
        self.figure.canvas.draw()
        self.changed.emit()
