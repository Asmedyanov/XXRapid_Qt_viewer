from PyQt5.QtWidgets import QTabWidget
from .ComsolSimulationQWidget import *


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

    def on_comsol_simulation(self):
        self.SettingsDict = self.ComsolSimulationQWidget.SettingsDict
        self.changed.emit()
