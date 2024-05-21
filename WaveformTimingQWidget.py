from MatplotlibQWidget import MatplotlibQWidget
import numpy as np
import pandas as pd
from scipy.signal import find_peaks


class WaveformTimingQWidget(MatplotlibQWidget):
    def __init__(self, physical_df_dict=None):
        super().__init__()
        self.physical_df_dict = physical_df_dict
        self.max_time = self.get_max_time()
        self.Normed_df_dict = self.get_normed_dict()

        self.ax = self.figure.add_subplot(111)
        self.ax.set(
            xlabel='t, us',
            ylabel='Unit',
            # title='Waveform timing'
        )
        self.Normed_plots_dict = dict()
        for mykey, mydf in self.Normed_df_dict.items():
            self.Normed_plots_dict[mykey], = self.ax.plot(mydf['time'].loc[mydf['time'] < self.max_time] * 1.0e6,
                                                          mydf['Units'].loc[mydf['time'] < self.max_time], label=mykey)
        self.ax.legend()

    def get_max_time(self):
        current_argmax = np.argmax(self.physical_df_dict['Current']['Units'].values)
        max_time = self.physical_df_dict['Current']['time'][current_argmax]
        return max_time*1.5

    def get_normed_dict(self):
        Normed_df_dict = {
            'Trigger': pd.DataFrame({
                'time': self.physical_df_dict['Trigger']['time'],
                'Units': np.where(self.physical_df_dict['Trigger']['Units'] < 0,
                                  0,
                                  self.physical_df_dict['Trigger']['Units'] / self.physical_df_dict['Trigger'][
                                      'Units'].max()
                                  )
            }),
            'Current': pd.DataFrame({
                'time': self.physical_df_dict['Current']['time'],
                'Units': np.where(self.physical_df_dict['Current']['Units'] < 0,
                                  0,
                                  self.physical_df_dict['Current']['Units'] / self.physical_df_dict['Current'][
                                      'Units'].max()
                                  )
            }),
            'Voltage': pd.DataFrame({
                'time': self.physical_df_dict['Voltage']['time'],
                'Units': np.where(self.physical_df_dict['Voltage']['Units'] < 0,
                                  0,
                                  self.physical_df_dict['Voltage']['Units'] / self.physical_df_dict['Voltage'][
                                      'Units'].max()
                                  )
            }),

        }
        return Normed_df_dict

    def set_data(self, physical_df_dict):
        self.physical_df_dict = physical_df_dict
        self.max_time = self.get_max_time()
        self.Normed_df_dict = self.get_normed_dict()
        for mykey, mydf in self.Normed_df_dict.items():
            self.Normed_plots_dict[mykey].set_data(mydf['time'].loc[mydf['time'] < self.max_time] * 1.0e6,
                                                   mydf['Units'].loc[mydf['time'] < self.max_time])
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()
        self.changed.emit()
