from PyQt5.QtWidgets import QTabWidget
from .WaveformCurrentQWidget import *
from .WaveformFullVoltageQWidget import *
from .WaveformIdotQWidget import *
from .WaveformResistiveVoltageQWidget import *
from .WaveformPowerQWidget import *
from .WaveformResistanceQWidget import *
from .WaveformEnergyQWidget import *
import os


class WaveformPhysicalValuesQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Physical_values'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.WaveformTimingQWidget = self.parent.WaveformTimingQWidget
        self.timeshift = self.WaveformTimingQWidget.t_start
        self.physical_df_dict = self.WaveformTimingQWidget.physical_df_dict
        super().__init__()
        try:
            self.WaveformCurrentQWidget = WaveformCurrentQWidget(self)
            # self.WaveformCurrentQWidget.changed.connect(self.OnWaveformCurrentQWidget)
            self.addTab(self.WaveformCurrentQWidget, self.WaveformCurrentQWidget.settings_key)
        except Exception as ex:
            print(f'WaveformCurrentQWidget {ex}')
        '''try:
            self.WaveformFullVoltageQWidget = WaveformFullVoltageQWidget(physical_df_dict['Voltage'], timeshift)
            self.WaveformFullVoltageQWidget.changed.connect(self.OnWaveformFullVoltageQWidget)
            self.addTab(self.WaveformFullVoltageQWidget, 'Full voltage')
        except Exception as ex:
            print(f'WaveformFullVoltageQWidget {ex}')
        key = 'I_dot'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.WaveformIdotQWidget = WaveformIdotQWidget(df_current=physical_df_dict['Current'],
                                                           settings_dict=settings, timeshift=timeshift)
            self.SettingsDict[key] = self.WaveformIdotQWidget.SettingsDict
            self.WaveformIdotQWidget.changed.connect(self.OnWaveformIdotQWidgetChanged)
            self.addTab(self.WaveformIdotQWidget, 'Current derivative')
        except Exception as ex:
            print(f'WaveformIdotQWidget {ex}')

        key = 'U_res'
        settings_dict = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.WaveformResistiveVoltageQWidget = WaveformResistiveVoltageQWidget(
                df_full_voltage=self.WaveformFullVoltageQWidget.voltageDF,
                df_idot=self.WaveformIdotQWidget.df_idot_smoothed_to_plot,
                settings_dict=settings
            )
            self.WaveformResistiveVoltageQWidget.changed.connect(self.OnWaveformUresQWidget)
            self.addTab(self.WaveformResistiveVoltageQWidget, 'Resistive voltage')
        except Exception as ex:
            print(f'WaveformResistiveVoltageQWidget {ex}')

        try:
            self.WaveformPowerQWidget = WaveformPowerQWidget(
                df_current=self.WaveformCurrentQWidget.current_df_to_plot,
                df_u_resistive=self.WaveformResistiveVoltageQWidget.df_resistive_voltage,
                ind_peak_time=self.WaveformResistiveVoltageQWidget.idot_peak_time
            )
            self.addTab(self.WaveformPowerQWidget, 'Resistive power')
        except Exception as ex:
            print(ex)
        try:
            self.WaveformResistanceQWidget = WaveformResistanceQWidget(
                df_current=self.WaveformCurrentQWidget.current_df_to_plot,
                df_u_resistive=self.WaveformResistiveVoltageQWidget.df_resistive_voltage,
                ind_peak_time=self.WaveformResistiveVoltageQWidget.idot_peak_time
            )
            self.addTab(self.WaveformResistanceQWidget, 'Resistance')
        except Exception as ex:
            print(ex)'''

        '''try:
            self.WaveformEnergyQWidget = WaveformEnergyQWidget(
                df_current=self.WaveformCurrentQWidget.current_df_to_plot,
                df_power=self.WaveformPowerQWidget.df_power
            )
            self.addTab(self.WaveformEnergyQWidget, 'Energy')
        except Exception as ex:
            print(ex)'''

    def OnWaveformUresQWidget(self):
        try:
            self.WaveformPowerQWidget.set_data(
                df_current=self.WaveformCurrentQWidget.current_df_to_plot,
                df_Ures=self.WaveformUresQWidget.df_resistive_voltage
            )
        except Exception as ex:
            print(f'WaveformPowerQWidget.set_data {ex}')
        try:
            self.WaveformResistanceQWidget.set_data(
                df_current=self.WaveformCurrentQWidget.current_df_to_plot,
                df_Ures=self.WaveformUresQWidget.df_resistive_voltage,
                ind_peak_time=self.WaveformIdotQWidget.Peak_time
            )
        except Exception as ex:
            print(f'WaveformResistanceQWidget.set_data {ex}')
        '''try:
            self.WaveformEnergyQWidget.set_data(
                df_current=self.WaveformCurrentQWidget.current_df_to_plot,
                df_power=self.WaveformPowerQWidget.df_Power
            )
        except Exception as ex:
            print(f'WaveformEnergyQWidget.set_data {ex}')'''
        self.changed.emit()

    def OnWaveformIdotQWidgetChanged(self):
        try:
            self.SettingsDict['I_dot'] = self.WaveformIdotQWidget.SettingsDict
            self.WaveformResistiveVoltageQWidget.set_data(
                df_full_voltage=self.WaveformFullVoltageQWidget.voltageDF,
                df_idot=self.WaveformIdotQWidget.df_idot_smoothed_to_plot,
            )
        except Exception as ex:
            print(f'OnWaveformIdotQWidgetChanged {ex}')
        self.changed.emit()

    def set_data(self, physical_df_dict=None, timeshift=0):
        try:
            self.WaveformCurrentQWidget.set_data(physical_df_dict['Current'], timeshift)
        except Exception as ex:
            print(f'WaveformCurrentQWidget.set_data {ex}')
        try:
            self.WaveformFullVoltageQWidget.set_data(physical_df_dict['Voltage'], timeshift)
        except Exception as ex:
            print(f'WaveformFullVoltageQWidget.set_data {ex}')

        self.changed.emit()

    def Save_Raport(self, folder_name):
        if 'Waveform_physical' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Waveform_physical')
        try:
            self.WaveformCurrentQWidget.save_report(f'{folder_name}/Waveform_physical')
        except Exception as ex:
            print(ex)
        try:
            self.WaveformFullVoltageQWidget.save_report(f'{folder_name}/Waveform_physical')
        except Exception as ex:
            print(ex)
        try:
            self.WaveformIdotQWidget.Save_Raport(f'{folder_name}/Waveform_physical')
        except Exception as ex:
            print(ex)
        try:
            self.WaveformUresQWidget.save_report(f'{folder_name}/Waveform_physical')
        except Exception as ex:
            print(ex)
        try:
            self.WaveformPowerQWidget.save_report(f'{folder_name}/Waveform_physical')
        except Exception as ex:
            print(ex)
        try:
            self.WaveformResistanceQWidget.save_report(f'{folder_name}/Waveform_physical')
        except Exception as ex:
            print(ex)
        '''try:
            self.WaveformEnergyQWidget.save_report(f'{folder_name}/Waveform_physical')
        except Exception as ex:
            print(ex)'''

    def OnWaveformCurrentQWidget(self):
        try:
            self.WaveformIdotQWidget.set_data(self.physical_df_dict['Current'], self.timeshift)
        except Exception as ex:
            print(f'WaveformIdotQWidget.set_data {ex}')
        self.changed.emit()

    def OnWaveformFullVoltageQWidget(self):
        try:
            self.WaveformUresQWidget.set_data(
                df_full_voltage=self.WaveformFullVoltageQWidget.voltageDF,
                df_idot=self.WaveformIdotQWidget.df_idot_smoothed_to_plot,
                idot_peak_time=self.WaveformIdotQWidget.Peak_time
            )
        except Exception as ex:
            print(f'WaveformFullVoltageQWidget.set_data {ex}')
        self.changed.emit()

    def test_settings_key(self, key_line):
        if key_line not in self.SettingsDict.keys():
            self.SettingsDict[key_line] = dict()
