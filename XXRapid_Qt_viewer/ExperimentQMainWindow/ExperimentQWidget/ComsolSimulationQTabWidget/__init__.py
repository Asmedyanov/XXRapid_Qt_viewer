from PyQt5.QtWidgets import QTabWidget
from .CAIComsolQTabWidget import *
from .ComsolCutternQTabWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class ComsolSimulationQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Comsol')
        self.folder_path = self.parent.folder_path
        self.folder_list = self.parent.folder_list
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.TOFResultQTabWidget = self.parent.XXRapidTOFQTabWidget.TOFResultQTabWidget
        try:
            self.ComsolCurrentQTabWidget = ComsolCurrentQTabWidget(self)
            self.addTab(self.ComsolCurrentQTabWidget, self.ComsolCurrentQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.CAIComsolQTabWidget = CAIComsolQTabWidget(self)
            self.addTab(self.CAIComsolQTabWidget, self.CAIComsolQTabWidget.settings_key)
        except Exception as ex:
            print(ex)

    def on_comsol_simulation(self):
        self.SettingsDict = self.ComsolSimulationQWidget.SettingsDict
        try:
            self.CAIComsolQWidget.update()
        except Exception as ex:
            print(ex)
        self.changed.emit()

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        try:
            self.ComsolCurrentQTabWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.CAIComsolQTabWidget.save_report()
        except Exception as ex:
            print(ex)
