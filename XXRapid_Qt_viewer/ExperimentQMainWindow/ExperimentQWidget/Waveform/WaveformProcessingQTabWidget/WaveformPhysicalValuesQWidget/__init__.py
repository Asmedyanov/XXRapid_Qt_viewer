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
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.WaveformTimingQWidget = self.parent.WaveformTimingQWidget
        self.WaveformTimingQWidget.changed.connect(self.refresh)
        self.timeshift = self.WaveformTimingQWidget.t_start
        self.physical_df_dict = self.WaveformTimingQWidget.physical_df_dict
        self.t_end = self.WaveformTimingQWidget.t_end
        self.changed.connect(self.on_changed)

        try:
            self.CurrentQWidget = CurrentQWidget(self)
            self.addTab(self.CurrentQWidget, self.CurrentQWidget.settings_key)
        except Exception as ex:
            print(f'CurrentQWidget {ex}')
        try:
            self.FullVoltageQWidget = FullVoltageQWidget(self)
            self.addTab(self.FullVoltageQWidget, self.FullVoltageQWidget.settings_key)
        except Exception as ex:
            print(ex)

        try:
            self.IdotQWidget = IdotQWidget(self)
            self.addTab(self.IdotQWidget, self.IdotQWidget.settings_key)
        except Exception as ex:
            print(ex)

        try:
            self.ResistiveVoltageQWidget = ResistiveVoltageQWidget(self)
            self.addTab(self.ResistiveVoltageQWidget, self.ResistiveVoltageQWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.PowerQWidget = PowerQWidget(self)
            self.addTab(self.PowerQWidget, self.PowerQWidget.settings_key)
            # self.PowerQWidget.changed.connect(self.on_power_changed)
        except Exception as ex:
            print(ex)
        try:
            self.ResistanceQWidget = ResistanceQWidget(self)
            self.addTab(self.ResistanceQWidget, self.ResistanceQWidget.settings_key)
            self.ResistanceQWidget.changed.connect(self.on_resistance_changed)
        except Exception as ex:
            print(ex)

        try:
            self.EnergyQWidget = EnergyQWidget(self)
            self.addTab(self.EnergyQWidget, self.EnergyQWidget.settings_key)
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
        self.changed.emit()

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
        # self.changed.emit()

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        try:
            self.CurrentQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.FullVoltageQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.IdotQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.ResistiveVoltageQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.PowerQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.ResistanceQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.EnergyQWidget.save_report()
        except Exception as ex:
            print(ex)

    def save_origin_pro(self, op):
        self.workbook_c_v_r = op.new_book(lname='Current Voltage Resistance')
        self.graph_c_v_r = op.new_graph(template='3Ys_Y-YY', lname='Current Voltage Resistance')
        self.workbook_e_p = op.new_book(lname='Power Energy')
        self.graph_e_p = op.new_graph(template='3Ys_Y-YY', lname='Power Energy')
        try:
            self.CurrentQWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
        try:
            self.FullVoltageQWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
        try:
            self.IdotQWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
        try:
            self.ResistiveVoltageQWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
        try:
            self.PowerQWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
        try:
            self.ResistanceQWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
        try:
            self.EnergyQWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
