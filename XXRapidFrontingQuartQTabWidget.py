from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from XXRapidFrontingTracerQWidget import *


class XXRapidFrontingQuartQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data, settings_dict=None):
        super().__init__()
        self.camera_data = camera_data
        self.SettingsDict = dict()
        try:
            settings = settings_dict['Tracer']
        except:
            settings = None
        try:
            self.XXRapidFrontingTracerQWidget = XXRapidFrontingTracerQWidget(self.camera_data, settings)
            self.addTab(self.XXRapidFrontingTracerQWidget, 'Tracer')
            self.SettingsDict['Tracer'] = self.XXRapidFrontingTracerQWidget.SettingsDict
            self.XXRapidFrontingTracerQWidget.chandeg.connect(self.OnXXRapidFrontingTracerQWidget)
        except Exception as ex:
            print(f'XXRapidFrontingTracerQWidget {ex}')

    def set_data(self, camera_data):
        self.camera_data = camera_data
        self.XXRapidFrontingTracerQWidget.set_data(self.camera_data)

    def OnXXRapidFrontingTracerQWidget(self):
        self.SettingsDict['Tracer'] = self.XXRapidFrontingTracerQWidget.SettingsDict
        self.changed.emit()
