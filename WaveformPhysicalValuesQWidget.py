from PyQt5.QtWidgets import QTabWidget
from WaveformCurrentQWidget import *
from WaveformFullVoltageQWidget import *
from WaveformIdotQWidget import *
from WaveformUresQWidget import *
from WaveformPowerQWidget import *
from WaveformResistanceQWidget import *


class WaveformPhysicalValuesQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, physical_df_dict=None, settings_dict=None, timeshift=0):
        super().__init__()
        self.setTabPosition(QTabWidget.TabPosition.West)
        try:
            self.WaveformCurrentQWidget = WaveformCurrentQWidget(physical_df_dict['Current'], timeshift)
            self.addTab(self.WaveformCurrentQWidget, 'Waveform_current')
        except Exception as ex:
            print(ex)
        try:
            self.WaveformFullVoltageQWidget = WaveformFullVoltageQWidget(physical_df_dict['Voltage'], timeshift)
            self.addTab(self.WaveformFullVoltageQWidget, 'Full voltage')
        except Exception as ex:
            print(ex)
        try:

            try:
                settings = settings_dict['I_dot']
            except:
                settings = None
            self.WaveformIdotQWidget = WaveformIdotQWidget(df_current=physical_df_dict['Current'], timeshift=timeshift,
                                                           settings_dict=settings)
            self.SettingsDict = {'I_dot': self.WaveformIdotQWidget.SettingsDict}
            self.WaveformIdotQWidget.changed.connect(self.OnWaveformIdotQWidgetChanged)
            self.addTab(self.WaveformIdotQWidget, 'Current derivative')
        except Exception as ex:
            print(ex)

        try:
            self.WaveformUresQWidget = WaveformUresQWidget(
                df_full_voltage=self.WaveformFullVoltageQWidget.voltageDF,
                df_idot=self.WaveformIdotQWidget.df_idot_smoothed_to_plot,
                idot_peak_time=self.WaveformIdotQWidget.Peak_time
            )
            self.WaveformUresQWidget.changed.connect(self.OnWaveformUresQWidget)
            self.addTab(self.WaveformUresQWidget, 'Resistive voltage')
        except Exception as ex:
            print(ex)

        try:
            self.WaveformPowerQWidget = WaveformPowerQWidget(
                df_current=self.WaveformCurrentQWidget.current_df_to_plot,
                df_Ures=self.WaveformUresQWidget.df_resistive_voltage
            )
            self.addTab(self.WaveformPowerQWidget, 'Resistive power')
        except Exception as ex:
            print(ex)
        try:
            self.WaveformResistanceQWidget = WaveformResistanceQWidget(
                df_current=self.WaveformCurrentQWidget.current_df_to_plot,
                df_Ures=self.WaveformUresQWidget.df_resistive_voltage,
                ind_peak_time=self.WaveformIdotQWidget.Peak_time
            )
            self.addTab(self.WaveformResistanceQWidget, 'Resistance')
        except Exception as ex:
            print(ex)

    def OnWaveformUresQWidget(self):
        self.WaveformPowerQWidget.set_data(
            df_current=self.WaveformCurrentQWidget.current_df_to_plot,
            df_Ures=self.WaveformUresQWidget.df_resistive_voltage
        )
        self.WaveformResistanceQWidget.set_data(
            df_current=self.WaveformCurrentQWidget.current_df_to_plot,
            df_Ures=self.WaveformUresQWidget.df_resistive_voltage,
            ind_peak_time=self.WaveformIdotQWidget.Peak_time
        )
        self.changed.emit()

    def OnWaveformIdotQWidgetChanged(self):
        self.SettingsDict['I_dot'] = self.WaveformIdotQWidget.SettingsDict
        self.WaveformUresQWidget.set_data(
            df_full_voltage=self.WaveformFullVoltageQWidget.voltageDF,
            df_idot=self.WaveformIdotQWidget.df_idot_smoothed_to_plot,
            idot_peak_time=self.WaveformIdotQWidget.Peak_time,
        )
        self.changed.emit()

    def set_data(self, physical_df_dict=None, timeshift=0):
        self.WaveformCurrentQWidget.set_data(physical_df_dict['Current'], timeshift)
        self.WaveformFullVoltageQWidget.set_data(physical_df_dict['Voltage'], timeshift)
        self.WaveformIdotQWidget.set_data(physical_df_dict['Current'], timeshift)
        self.WaveformUresQWidget.set_data(
            df_full_voltage=self.WaveformFullVoltageQWidget.voltageDF,
            df_idot=self.WaveformIdotQWidget.df_idot_smoothed_to_plot,
            idot_peak_time=self.WaveformIdotQWidget.Peak_time
        )
        self.changed.emit()
