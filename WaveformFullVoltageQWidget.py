from MatplotlibSingeAxQWidget import *


class WaveformFullVoltageQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, voltage_df, time_shift):
        super().__init__('Full_voltage')
        self.voltageDF = voltage_df.copy()
        self.voltageDF['time'] -= time_shift
        self.ax.set(
            xlabel='t, us',
            ylabel='$U_{full}$, kV',
            title='Physical full voltage'
        )
        self.voltage_df_to_plot = self.voltageDF.loc[self.voltageDF['time'] > 0]
        self.voltageLine, = self.ax.plot(self.voltage_df_to_plot['time'] * 1e6, self.voltage_df_to_plot['Units'] * 1e-3)

    def set_data(self, voltage_df, time_shift):
        self.voltageDF = voltage_df.copy()
        self.voltageDF['time'] -= time_shift
        self.voltage_df_to_plot = self.voltageDF.loc[self.voltageDF['time'] > 0]
        self.voltageLine.set_data(self.voltage_df_to_plot['time'] * 1e6, self.voltage_df_to_plot['Units'] * 1e-3)
        self.changed.emit()

    def Save_Raport(self, folder_name):
        if 'Full_voltage' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Full_voltage')
        super().Save_Raport(f'{folder_name}/Full_voltage')
        self.voltage_df_to_plot.to_csv(f'{folder_name}/Full_voltage/Full_voltage.csv')
