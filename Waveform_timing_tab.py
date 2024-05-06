from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks


class Waveform_timing_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        t = np.arange(0, 2.0 * np.pi, 0.1)
        x = np.cos(t)
        y = np.sin(t)
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.figure.set_layout_engine(layout='tight')
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
        # self.ax_1.spines.right.set_position(("axes", 1.2))
        # self.ax_2.spines.right.set_position(("axes", 1.2))
        # self.ax_3.spines.right.set_position(("axes", 2.4))
        self.waveform_plots_dict = {
            'I': self.ax.plot(
                x,
                y, 'r',
                label=f'I')[0],
            'Systron': self.ax_1.plot(
                x * 2,
                y * 2,
                label=f'Systron')[0],
            '4Quick': self.ax_2.plot(
                x * 3,
                y * 3, 'g',
                label=f'4Quick')[0],

            'U': self.ax_3.plot(
                x * 4,
                y * 4, 'b',
                label=f'U')[0],

        }
        self.shutter_plot_list = []
        for i in range(8):
            self.shutter_plot_list.append(
                self.ax_2.plot(
                    x * 3,
                    y * 3, 'r', )[0])
        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.waveform_dict = dict()

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
        self.df_4quick['value'] = np.abs(np.gradient(self.df_4quick['value']))
        self.df_4quick['value'] /= self.df_4quick['value'].max()

        index_peak = find_peaks(self.df_4quick['value'].values, prominence=0.5, distance=20)[0]
        self.peak_time = self.df_4quick['time'].values[index_peak]
        self.peak_4quick = self.df_4quick['value'].values[index_peak]

        index_end = np.argwhere(self.df_4quick['value'].values > 0.5 * np.max(self.df_4quick['value'].values)).max()
        '''self.waveform_plots_dict['I'].set_data(self.df_current['time'][voltage_start_index:index_end] * 1.0e6,
                                               self.df_current['value'][voltage_start_index:index_end] * 1.0e-3)'''
        self.waveform_plots_dict['Systron'].set_data(self.df_systron['time'][voltage_start_index:index_end] * 1.0e6,
                                                     self.df_systron['value'][voltage_start_index:index_end])
        self.waveform_plots_dict['4Quick'].set_data(self.df_4quick['time'][voltage_start_index:index_end] * 1.0e6,
                                                    self.df_4quick['value'][voltage_start_index:index_end])
        '''try:
            self.waveform_plots_dict['4Quick_peak'].set_data(self.peak_time * 1.0e6, self.peak_4quick)
        except:
            self.waveform_plots_dict['4Quick_peak'] = self.ax_2.plot(self.peak_time * 1.0e6, self.peak_4quick, 'or')[0]'''
        self.waveform_plots_dict['U'].set_data(self.df_voltage['time'][voltage_start_index:index_end] * 1.0e6,
                                               self.df_voltage['value'][voltage_start_index:index_end] * 1.0e-3)
        pass

        self.ax.relim()
        self.ax_1.relim()
        self.ax_2.relim()
        self.ax_3.relim()
        self.ax.autoscale_view()
        self.ax_1.autoscale_view()
        self.ax_2.autoscale_view()
        self.ax_3.autoscale_view()
        self.figure.canvas.draw()
