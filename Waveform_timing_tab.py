from Matplotlib_qtwidget import Matplotlib_qtwidget
import numpy as np
import pandas as pd
from scipy.signal import find_peaks


class Waveform_timing_tab(Matplotlib_qtwidget):
    def __init__(self):
        super().__init__()
        t = np.arange(0, 2.0 * np.pi, 0.1)
        x = np.cos(t)
        y = np.sin(t)
        self.ax = self.figure.add_subplot(111)
        self.ax.set(
            xlabel='t, us',
            ylabel='I, kA',
            title='Waveform timing'
        )
        self.ax_1 = self.ax.twinx()
        self.ax_1.set_ylabel('Systron, V')
        self.ax_2 = self.ax.twinx()
        self.ax_2.set_ylabel('4Quik, V')
        self.ax_3 = self.ax.twinx()
        self.ax_3.set_ylabel('U, kV')
        self.waveform_plots_dict = {
            'I': self.ax.plot(x, y, 'g', label=f'I')[0],
            'Systron': self.ax_1.plot(x * 2, y * 2, label=f'Systron')[0],
            'U': self.ax_3.plot(x * 4, y * 4, 'b', label=f'U')[0],
            '4Quick': self.ax_2.plot(x * 3, y * 3, 'r', label=f'4Quick')[0],
            '4Quick_peak': self.ax_2.plot(x * 3, y * 3, 'og', label=f'4Quick')[0]
        }

    def set_data(self, waveform_df, info_df):
        self.df_voltage = pd.DataFrame({
            'time': waveform_df['channel_3_time'].values,
            'value': waveform_df['channel_3'].values * float(info_df['Value']['Tektronix'])
        })
        voltage_start_index = np.argwhere(
            np.abs(self.df_voltage['value']) > np.max(np.abs(
                self.df_voltage['value'].values[np.argwhere(self.df_voltage['time'].values < 0)]))).min()
        voltage_timeshift = self.df_voltage['time'].values[voltage_start_index]
        self.df_voltage['time'] -= voltage_timeshift
        self.df_voltage['value'] = np.where(self.df_voltage['value'] < 0, 0, self.df_voltage['value'])

        self.df_current = pd.DataFrame({
            'time': waveform_df['channel_0_time'].values - voltage_timeshift,
            'value': waveform_df['channel_0'].values * info_df['Value']['Rogovski_ampl']
        })
        self.df_current['value'] = np.where(self.df_current['value'] < 0, 0, self.df_current['value'])
        self.df_systron = pd.DataFrame({
            'time': waveform_df['channel_1_time'].values - voltage_timeshift,
            'value': waveform_df['channel_1'].values
        })
        self.df_systron['value'] = np.where(self.df_systron['value'] < 0, 0, self.df_systron['value'])
        self.df_4quick = pd.DataFrame({
            'time': waveform_df['channel_2_time'].values - voltage_timeshift,
            'value': waveform_df['channel_2'].values
        })
        max_4quick = np.mean(self.df_4quick['value'].values[:voltage_start_index])
        self.df_4quick['value'] = np.where(self.df_4quick['value'] > max_4quick, 0,
                                           np.abs(self.df_4quick['value'] - max_4quick))
        self.df_4quick['value'] = np.gradient(self.df_4quick['value'])
        self.df_4quick['value_neg'] = np.where(self.df_4quick['value'] < 0, -self.df_4quick['value'], 0)
        self.df_4quick['value'] = np.where(self.df_4quick['value'] < 0, 0, self.df_4quick['value'])
        self.df_4quick['value'] /= self.df_4quick['value'].max()

        index_peak = find_peaks(self.df_4quick['value'].values, prominence=0.5, distance=30, width=10)[0][-8:]
        self.peak_time = self.df_4quick['time'].values[index_peak]
        self.peak_4quick = self.df_4quick['value'].values[index_peak]

        index_end = np.argwhere(
            self.df_4quick['value_neg'].values > 0.5 * np.max(self.df_4quick['value_neg'].values)).max()
        self.waveform_plots_dict['I'].set_data(self.df_current['time'][voltage_start_index:index_end] * 1.0e6,
                                               self.df_current['value'][voltage_start_index:index_end] * 1.0e-3)
        self.waveform_plots_dict['Systron'].set_data(self.df_systron['time'][voltage_start_index:index_end] * 1.0e6,
                                                     self.df_systron['value'][voltage_start_index:index_end])
        self.waveform_plots_dict['4Quick'].set_data(self.df_4quick['time'][voltage_start_index:index_end] * 1.0e6,
                                                    self.df_4quick['value'][voltage_start_index:index_end])
        self.waveform_plots_dict['4Quick_peak'].set_data(self.peak_time * 1.0e6, self.peak_4quick)
        self.waveform_plots_dict['U'].set_data(self.df_voltage['time'][voltage_start_index:index_end] * 1.0e6,
                                               self.df_voltage['value'][voltage_start_index:index_end] * 1.0e-3)

        self.ax.relim()
        self.ax_1.relim()
        self.ax_2.relim()
        self.ax_3.relim()
        self.ax.autoscale_view()
        self.ax_1.autoscale_view()
        self.ax_2.autoscale_view()
        self.ax_3.autoscale_view()
        self.figure.canvas.draw()
        self.changed.emit()
