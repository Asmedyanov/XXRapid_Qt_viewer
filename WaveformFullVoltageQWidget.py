from MatplotlibQWidget import *


class WaveformFullVoltageQWidget(MatplotlibQWidget):
    def __init__(self, voltage_df, time_shift):
        super().__init__()
        self.voltageDF = voltage_df
        self.voltageDF['time'] -= time_shift
        self.ax = self.figure.add_subplot(111)
        self.ax.set(
            xlabel='t, us',
            ylabel='$U_{full}$, kV',
            title='Physical full voltage'
        )
        voltageDFtoPlot = self.voltageDF.loc[self.voltageDF['time'] > 0]
        self.voltageLine, = self.ax.plot(voltageDFtoPlot['time'] * 1e6, voltageDFtoPlot['Units'] * 1e-3)

    def set_data(self, voltage_df, time_shift):
        self.voltageDF = voltage_df
        self.voltageDF['time'] -= time_shift
        voltage_df_to_plot = self.voltageDF.loc[self.voltageDF['time'] > 0]
        self.voltageLine.set_data(voltage_df_to_plot['time'] * 1e6, voltage_df_to_plot['Units'] * 1e-3)
