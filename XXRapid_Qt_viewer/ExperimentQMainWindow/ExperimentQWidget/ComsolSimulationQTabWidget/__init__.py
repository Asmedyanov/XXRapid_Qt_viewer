from PyQt5.QtWidgets import QTabWidget
from .ComsolSimulationQWidget import *
from .CAIComsolQWidget import *


class ComsolSimulationQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, parent, filename='Default_shot/Jmax.csv', settings_dict=None):
        super().__init__()
        self.parent = parent
        self.filename = filename
        self.ComsolSimulationQWidget = ComsolSimulationQWidget(self.parent, self.filename, settings_dict)
        self.SettingsDict = self.ComsolSimulationQWidget.SettingsDict
        self.ComsolSimulationQWidget.changed.connect(self.on_comsol_simulation)
        self.addTab(self.ComsolSimulationQWidget, 'ComsolSimulation')
        try:
            self.CAIComsolQWidget = CAIComsolQWidget(self)
            self.addTab(self.CAIComsolQWidget, 'CAI_comsol')
        except Exception as ex:
            print(ex)

    def on_comsol_simulation(self):
        self.SettingsDict = self.ComsolSimulationQWidget.SettingsDict
        try:
            self.CAIComsolQWidget.update()
        except Exception as ex:
            print(ex)
        self.changed.emit()
