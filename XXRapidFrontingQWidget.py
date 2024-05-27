from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from XXRapidFrontingFramesQTabWidget import *


class XXRapidFrontingQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data_dict, settings_dict=None):
        super().__init__()
        self.camera_data_dict = camera_data_dict
        self.SettingsDict = dict()
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        try:
            settings = settings_dict['Fronting_frames']
        except:
            settings = None
        try:
            self.XXRapidFrontingFramesQTabWidget = XXRapidFrontingFramesQTabWidget(self.camera_data_dict, settings)
            self.QHBoxLayout.addWidget(self.XXRapidFrontingFramesQTabWidget)
            self.SettingsDict['Fronting_frames'] = self.XXRapidFrontingFramesQTabWidget.SettingsDict
            self.XXRapidFrontingFramesQTabWidget.changed.connect(self.OnXXRapidFrontingFramesQTabWidget)
        except Exception as ex:
            print(f'XXRapidFrontingFramesQTabWidget {ex}')

    def OnXXRapidFrontingFramesQTabWidget(self):
        self.SettingsDict['Fronting_frames'] = self.XXRapidFrontingFramesQTabWidget.SettingsDict
    def set_data(self, camera_data_dict):
        self.camera_data_dict = camera_data_dict
        self.changed.emit()
        pass
