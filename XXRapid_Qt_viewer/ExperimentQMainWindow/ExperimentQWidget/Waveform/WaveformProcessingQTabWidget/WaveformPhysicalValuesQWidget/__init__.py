from .CurrentQWidget import *
from .FullVoltageQWidget import *
from .IdotQWidget import *
from .ResistiveVoltageQWidget import *
from .PowerQWidget import *
from .ResistanceQWidget import *
from .EnergyQWidget import *
import os
from SettingsQWidgets.ChildQTabWidget import *


class WaveformPhysicalValuesQWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Physical_values')
        self.WaveformTimingQWidget = self.parent.WaveformTimingQWidget
        self.timeshift = self.WaveformTimingQWidget.t_start
        self.physical_df_dict = self.WaveformTimingQWidget.physical_df_dict
        self.changed.connect(self.on_changed)

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
            self.ResistiveVoltageQWidget.changed.connect(self.on_resistive_voltage_changed)
        except Exception as ex:
            print(ex)
        try:
            self.PowerQWidget = PowerQWidget(self)
            self.addTab(self.PowerQWidget, self.PowerQWidget.settings_key)
            self.PowerQWidget.changed.connect(self.on_power_changed)
        except Exception as ex:
            print(ex)
        try:
            self.ResistanceQWidget = ResistanceQWidget(self)
            self.addTab(self.ResistanceQWidget, self.ResistanceQWidget.settings_key)
            self.ResistanceQWidget.changed.connect(self.on_resistance_changed)
        except Exception as ex:
            print(ex)

    def on_changed(self):
        print('Waveform physical values are changed')

    def on_energy_changed(self):
        pass

    def on_power_changed(self):
        try:
            self.EnergyQWidget.refresh()
        except Exception as ex:
            print(ex)

    def on_resistive_voltage_changed(self):
        try:
            self.PowerQWidget.refresh()
        except Exception as ex:
            print(ex)
        try:
            self.ResistanceQWidget.refresh()
        except Exception as ex:
            print(ex)
        self.changed.emit()

    def on_resistance_changed(self):
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

    def on_i_dot_changed(self):
        try:
            self.ResistiveVoltageQWidget.refresh()
        except Exception as ex:
            print(ex)
