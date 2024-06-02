import pandas as pd
import numpy as np

from MatplotlibSingeAxQWidget import *


class WaveformPowerQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, df_current, df_Ures):
        super().__init__('Power')
        self.ax.set(
            xlabel='t, us',
            ylabel='$P_{res}$, GW',
            title='Resistive power'
        )
        self.ax_2 = self.ax.twinx()
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
        self.CurrentLine, = self.ax_2.plot(self.df_current['time'] * 1e6, self.df_current['Units'] * 1e-3, ':r')
        self.PowerLine, = self.ax.plot(self.df_Power['time'] * 1e6, self.df_Power['Units'] * 1e-9)

    def ures_function(self, time):
        ret = np.interp(time, self.df_Ures['time'].values, self.df_Ures['Units'].values)
        return ret

    def current_function(self, time):
        ret = np.interp(time, self.df_current['time'].values, self.df_current['Units'].values)
        return ret

    def power_function(self, time):
        ret = self.current_function(time) * self.ures_function(time)
        return ret

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
        self.CurrentLine.set_data(self.df_current['time'] * 1e6, self.df_current['Units'] * 1e-3)
        self.PowerLine.set_data(self.df_Power['time'] * 1e6, self.df_Power['Units'] * 1e-9)
        self.ax_2.relim()
        self.ax_2.autoscale_view()
        self.changed.emit()

    def save_report(self, folder_name):
        if 'Power' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Power')
        super().save_report(f'{folder_name}/Power')
        self.df_Power.to_csv(f'{folder_name}/Power/Power.csv')
