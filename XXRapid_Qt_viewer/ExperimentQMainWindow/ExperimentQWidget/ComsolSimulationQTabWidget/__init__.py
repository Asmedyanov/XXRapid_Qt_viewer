from PyQt5.QtWidgets import QTabWidget
from .ComsolCutternQTabWidget import *
from .CAIComsolQWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class ComsolSimulationQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Comsol')
        self.folder_path = self.parent.folder_path
        self.folder_list = self.parent.folder_list
        self.TOFResultQTabWidget = self.parent.XXRapidTOFQTabWidget.TOFResultQTabWidget
        try:
            self.ComsolCurrentQTabWidget = ComsolCurrentQTabWidget(self)
            self.addTab(self.ComsolCurrentQTabWidget, self.ComsolCurrentQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
        '''self.ComsolCutternQTabWidget = ComsolCutternQTabWidget(self.parent, self.filename, settings_dict)
        self.SettingsDict = self.ComsolCutternQTabWidget.SettingsDict
        self.ComsolCutternQTabWidget.changed.connect(self.on_comsol_simulation)
        self.addTab(self.ComsolCutternQTabWidget, 'ComsolSimulation')
        try:
            self.CAIComsolQWidget = CAIComsolQWidget(self)
            self.addTab(self.CAIComsolQWidget, 'CAI_comsol')
        except Exception as ex:
            print(ex)'''

    def on_comsol_simulation(self):
        self.SettingsDict = self.ComsolSimulationQWidget.SettingsDict
        try:
            self.CAIComsolQWidget.update()
        except Exception as ex:
            print(ex)
        self.changed.emit()
