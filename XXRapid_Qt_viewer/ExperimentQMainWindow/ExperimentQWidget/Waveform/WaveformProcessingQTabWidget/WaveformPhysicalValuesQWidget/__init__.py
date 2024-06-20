from .CurrentQWidget import *
from .FullVoltageQWidget import *
from .IdotQWidget import *
from .ResistiveVoltageQWidget import *
from .WaveformPowerQWidget import *
from .WaveformResistanceQWidget import *
from .WaveformEnergyQWidget import *
import os
from SettingsQWidgets.ChildQTabWidget import *


class WaveformPhysicalValuesQWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Physical_values')
        self.WaveformTimingQWidget = self.parent.WaveformTimingQWidget
        self.timeshift = self.WaveformTimingQWidget.t_start
        self.physical_df_dict = self.WaveformTimingQWidget.physical_df_dict

        try:
            self.CurrentQWidget = CurrentQWidget(self)
            self.addTab(self.CurrentQWidget, self.CurrentQWidget.settings_key)
            self.CurrentQWidget.changed.connect(self.on_current_changed)
        except Exception as ex:
            print(f'CurrentQWidget {ex}')
        try:
            self.FullVoltageQWidget = FullVoltageQWidget(self)
            self.addTab(self.FullVoltageQWidget, self.FullVoltageQWidget.settings_key)
            self.FullVoltageQWidget.changed.connect(self.on_full_voltage_changed)
        except Exception as ex:
            print(ex)

        try:
            self.IdotQWidget = IdotQWidget(self)
            self.addTab(self.IdotQWidget, self.IdotQWidget.settings_key)
            self.IdotQWidget.changed.connect(self.on_i_dot_changed)
        except Exception as ex:
            print(ex)

        try:
            self.ResistiveVoltageQWidget = ResistiveVoltageQWidget(self)
            self.addTab(self.ResistiveVoltageQWidget, self.ResistiveVoltageQWidget.settings_key)
            self.ResistiveVoltageQWidget.changed.connect(self.on_resistive_voltage)
        except Exception as ex:
            print(ex)
        '''try:
            self.FullVoltageQWidget = FullVoltageQWidget(physical_df_dict['Voltage'], timeshift)
            self.FullVoltageQWidget.changed.connect(self.OnWaveformFullVoltageQWidget)
            self.addTab(self.FullVoltageQWidget, 'Full voltage')
        except Exception as ex:
            print(f'FullVoltageQWidget {ex}')
        key = 'I_dot'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.IdotQWidget = IdotQWidget(df_current=physical_df_dict['Current'],
                                                           settings_dict=settings, timeshift=timeshift)
            self.SettingsDict[key] = self.IdotQWidget.SettingsDict
            self.IdotQWidget.changed.connect(self.OnWaveformIdotQWidgetChanged)
            self.addTab(self.IdotQWidget, 'Current derivative')
        except Exception as ex:
            print(f'IdotQWidget {ex}')

        key = 'U_res'
        settings_dict = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.ResistiveVoltageQWidget = ResistiveVoltageQWidget(
                df_full_voltage=self.FullVoltageQWidget.voltageDF,
                df_idot=self.IdotQWidget.df_idot_smoothed_to_plot,
                settings_dict=settings
            )
            self.ResistiveVoltageQWidget.changed.connect(self.OnWaveformUresQWidget)
            self.addTab(self.ResistiveVoltageQWidget, 'Resistive voltage')
        except Exception as ex:
            print(f'ResistiveVoltageQWidget {ex}')

        try:
            self.WaveformPowerQWidget = WaveformPowerQWidget(
                df_current=self.CurrentQWidget.current_df_to_plot,
                df_u_resistive=self.ResistiveVoltageQWidget.df_resistive_voltage,
                ind_peak_time=self.ResistiveVoltageQWidget.idot_peak_time
            )
            self.addTab(self.WaveformPowerQWidget, 'Resistive power')
        except Exception as ex:
            print(ex)
        try:
            self.WaveformResistanceQWidget = WaveformResistanceQWidget(
                df_current=self.CurrentQWidget.current_df_to_plot,
                df_u_resistive=self.ResistiveVoltageQWidget.df_resistive_voltage,
                ind_peak_time=self.ResistiveVoltageQWidget.idot_peak_time
            )
            self.addTab(self.WaveformResistanceQWidget, 'Resistance')
        except Exception as ex:
            print(ex)'''

        '''try:
            self.WaveformEnergyQWidget = WaveformEnergyQWidget(
                df_current=self.CurrentQWidget.current_df_to_plot,
                df_power=self.WaveformPowerQWidget.df_power
            )
            self.addTab(self.WaveformEnergyQWidget, 'Energy')
        except Exception as ex:
            print(ex)'''

    def on_resistive_voltage(self):
        pass

    def refresh(self):
        self.timeshift = self.WaveformTimingQWidget.t_start
        self.physical_df_dict = self.WaveformTimingQWidget.physical_df_dict
        try:
            self.CurrentQWidget.refresh()
        except Exception as ex:
            print(ex)
        try:
            self.FullVoltageQWidget.refresh()
        except Exception as ex:
            print(ex)
        self.changed.emit()

    """
    Here is the problem. 
    """

    def on_current_changed(self):
        try:
            self.IdotQWidget.changed.disconnect()
            self.IdotQWidget.refresh()
            self.IdotQWidget.changed.connect(self.on_i_dot_changed)
        except Exception as ex:
            print(ex)

    def on_full_voltage_changed(self):
        try:
            self.ResistiveVoltageQWidget.refresh()
        except Exception as ex:
            print(ex)

    def OnWaveformUresQWidget(self):
        try:
            self.WaveformPowerQWidget.set_data(
                df_current=self.CurrentQWidget.current_df_to_plot,
                df_Ures=self.WaveformUresQWidget.df_resistive_voltage
            )
        except Exception as ex:
            print(f'WaveformPowerQWidget.set_data {ex}')
        try:
            self.WaveformResistanceQWidget.set_data(
                df_current=self.CurrentQWidget.current_df_to_plot,
                df_Ures=self.WaveformUresQWidget.df_resistive_voltage,
                ind_peak_time=self.WaveformIdotQWidget.Peak_time
            )
        except Exception as ex:
            print(f'WaveformResistanceQWidget.set_data {ex}')
        '''try:
            self.WaveformEnergyQWidget.set_data(
                df_current=self.CurrentQWidget.current_df_to_plot,
                df_power=self.WaveformPowerQWidget.df_Power
            )
        except Exception as ex:
            print(f'WaveformEnergyQWidget.set_data {ex}')'''
        self.changed.emit()

    def OnWaveformIdotQWidgetChanged(self):
        try:
            self.SettingsDict['I_dot'] = self.WaveformIdotQWidget.SettingsDict
            self.WaveformResistiveVoltageQWidget.set_data(
                df_full_voltage=self.FullVoltageQWidget.voltageDF,
                df_idot=self.WaveformIdotQWidget.df_idot_smoothed_to_plot,
            )
        except Exception as ex:
            print(f'OnWaveformIdotQWidgetChanged {ex}')
        self.changed.emit()

    def set_data(self, physical_df_dict=None, timeshift=0):
        try:
            self.CurrentQWidget.set_data(physical_df_dict['Current'], timeshift)
        except Exception as ex:
            print(f'CurrentQWidget.set_data {ex}')
        try:
            self.FullVoltageQWidget.set_data(physical_df_dict['Voltage'], timeshift)
        except Exception as ex:
            print(f'FullVoltageQWidget.set_data {ex}')

        self.changed.emit()

    def Save_Raport(self, folder_name):
        if 'Waveform_physical' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Waveform_physical')
        try:
            self.CurrentQWidget.save_report(f'{folder_name}/Waveform_physical')
        except Exception as ex:
            print(ex)
        try:
            self.FullVoltageQWidget.save_report(f'{folder_name}/Waveform_physical')
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
            print(f'IdotQWidget.set_data {ex}')
        self.changed.emit()

    def OnWaveformFullVoltageQWidget(self):
        try:
            self.WaveformUresQWidget.set_data(
                df_full_voltage=self.FullVoltageQWidget.voltageDF,
                df_idot=self.WaveformIdotQWidget.df_idot_smoothed_to_plot,
                idot_peak_time=self.WaveformIdotQWidget.Peak_time
            )
        except Exception as ex:
            print(f'FullVoltageQWidget.set_data {ex}')
        self.changed.emit()

    def on_i_dot_changed(self):
        try:
            self.ResistiveVoltageQWidget.refresh()
        except Exception as ex:
            print(ex)
