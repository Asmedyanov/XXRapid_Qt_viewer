import numpy as np
import pandas as pd
from MatplotlibQWidget import MatplotlibQWidget


class WaveformSmoothingWidget(MatplotlibQWidget):
    def __init__(self):
        super().__init__()
        t = np.arange(0, 2.0 * np.pi, 0.1)
        x = np.cos(t)
        y = np.sin(t)

        self.ax = self.figure.add_subplot(111)
        self.ax.set(
            xlabel='t, sec',
            ylabel='u, V',
            title='Waveform original'
        )
        self.waveform_plots_dict = dict()
        for i in range(4):
            self.waveform_plots_dict[f'channel_{i}'], = self.ax.plot(
                x * (i + 1),
                y * (i + 1),
                label=f'channel_{i}')
        self.ax.legend()
        self.waveform_dict = dict()

    def set_data(self, waveform_dict, n_conv):
        df = pd.DataFrame(waveform_dict)
        df_smoothed = df.rolling(n_conv, min_periods=1).mean()
        for my_key, my_plot in self.waveform_plots_dict.items():
            my_plot.set_data(
                df_smoothed[f'{my_key}_time'],
                df_smoothed[f'{my_key}'],
            )
        df_4quick = pd.DataFrame({
            'time': waveform_dict['channel_2_time'],
            'voltage': waveform_dict['channel_2'],
        })
        initial_4quick = df_4quick['voltage'].loc[df_4quick['time'] < 0].mean()
        df_4quick['signal'] = df_4quick['voltage'] - initial_4quick
        df_4quick['signal'] = np.where(df_4quick['signal'] > 0, 0, -df_4quick['signal'])
        df_4quick['signal'] = np.abs(np.gradient(df_4quick['signal']))
        df_4quick['signal'] /= df_4quick['signal'].max()
        df_4quick['signal'] = np.where(df_4quick['signal'] <1/2, 0, df_4quick['signal'])
        self.df_4quick = df_4quick#.rolling(3, min_periods=1).mean()
        self.df_smoothed = df_smoothed
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()
        self.changed.emit()
