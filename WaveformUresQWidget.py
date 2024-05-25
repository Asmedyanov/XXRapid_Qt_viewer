import pandas as pd

from MatplotlibSingeAxQWidget import *
import numpy as np


class WaveformUresQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, df_full_voltage, df_idot, idot_peak_time):
        super().__init__('Resistive_voltage')
        self.ax.set(
            xlabel='t, us',
            ylabel='U, kV',
            title='Resistive voltage'
        )
        self.df_full_voltage = df_full_voltage.copy()
        self.df_idot = df_idot.copy()
        self.idot_peak_time = idot_peak_time
        self.idot_peak_time_line = self.ax.axvline(self.idot_peak_time * 1.0e6, ls=':')
        voltageDFtoPlot = self.df_full_voltage.loc[self.df_full_voltage['time'] > 0]
        self.fullVoltageLine, = self.ax.plot(voltageDFtoPlot['time'] * 1e6, voltageDFtoPlot['Units'] * 1e-3,
                                             label='Full voltage')
        self.inductance = self.get_inductance()
        self.df_inductive_voltage = pd.DataFrame({
            'time': self.df_idot['time'],
            'Units': self.df_idot['Units'] * self.inductance
        })
        self.df_inductive_voltage_line, = self.ax.plot(self.df_inductive_voltage['time'] * 1e6,
                                                       self.df_inductive_voltage['Units'] * 1e-3,
                                                       label='Inductive voltage')
        self.df_resistive_voltage = pd.DataFrame({
            'time': self.df_idot['time'],
            'Units': self.resistive_voltage_function(self.df_idot['time'].values)
        })

        self.df_resistive_voltage_line, = self.ax.plot(self.df_resistive_voltage['time'] * 1e6,
                                                       self.df_resistive_voltage['Units'] * 1e-3,
                                                       label='Resistive voltage')
        self.ax.grid(ls=':')
        self.ax.legend()

    def full_voltage_function(self, time):
        ret = np.interp(time, self.df_full_voltage['time'].values, self.df_full_voltage['Units'].values)
        return ret

    def idot_function(self, time):
        ret = np.interp(time, self.df_idot['time'].values, self.df_idot['Units'].values)
        return ret

    def get_inductance(self):
        u_ind = self.full_voltage_function(self.idot_peak_time)
        idot_ind = self.idot_function(self.idot_peak_time)
        inductance = u_ind / idot_ind
        return inductance

    def inductive_voltage_function(self, time):
        ret = np.interp(time, self.df_inductive_voltage['time'].values, self.df_inductive_voltage['Units'].values)
        return ret

    def resistive_voltage_function(self, time):
        ret = self.full_voltage_function(time) - self.inductive_voltage_function(time)
        return ret

    def set_data(self, df_full_voltage, df_idot, idot_peak_time):
        self.df_full_voltage = df_full_voltage.copy()
        self.df_idot = df_idot.copy()
        self.idot_peak_time = idot_peak_time
        self.idot_peak_time_line.set_xdata(self.idot_peak_time * 1.0e6)
        voltageDFtoPlot = self.df_full_voltage.loc[self.df_full_voltage['time'] > 0]
        self.fullVoltageLine.set_data(voltageDFtoPlot['time'] * 1e6, voltageDFtoPlot['Units'] * 1e-3)
        self.inductance = self.get_inductance()
        self.df_inductive_voltage = pd.DataFrame({
            'time': self.df_idot['time'],
            'Units': self.df_idot['Units'] * self.inductance
        })
        self.df_inductive_voltage_line.set_data(self.df_inductive_voltage['time'] * 1e6,
                                                self.df_inductive_voltage['Units'] * 1e-3)
        self.df_resistive_voltage = pd.DataFrame({
            'time': self.df_idot['time'],
            'Units': self.resistive_voltage_function(self.df_idot['time'].values)
        })

        self.df_resistive_voltage_line.set_data(self.df_resistive_voltage['time'] * 1e6,
                                                self.df_resistive_voltage['Units'] * 1e-3)
        self.changed.emit()

    def Save_Raport(self, folder_name):
        if 'Resistive_voltage' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Resistive_voltage')
        super().Save_Raport(f'{folder_name}/Resistive_voltage')
        self.df_resistive_voltage.to_csv(f'{folder_name}/Resistive_voltage/Resistive_voltage.csv')
