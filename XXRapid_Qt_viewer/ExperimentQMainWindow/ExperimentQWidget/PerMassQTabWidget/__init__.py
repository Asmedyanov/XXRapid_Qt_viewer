from SettingsQWidgets.ChildQTabWidget import *
from .PowerEnergyQWidget import *


class PerMassQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Per_Mass_Unit')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.FoilQWidget = self.parent.FoilQWidget
        self.FoilQWidget.changed.connect(self.refresh)
        self.mass = self.FoilQWidget.mass
        self.WaveformQTabWidget = self.parent.WaveformQTabWidget.WaveformProcessingQTabWidget.WaveformPhysicalValuesQWidget
        try:
            self.PowerEnergyQWidget = PowerEnergyQWidget(self)
            self.addTab(self.PowerEnergyQWidget, self.PowerEnergyQWidget.settings_key)
        except Exception as ex:
            print(ex)

    def refresh(self):
        try:
            self.PowerEnergyQWidget.refresh()
        except Exception as ex:
            print(ex)

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        try:
            self.PowerEnergyQWidget.save_report()
        except Exception as ex:
            print(ex)

    def save_origin_pro(self, op):
        try:
            self.PowerEnergyQWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
