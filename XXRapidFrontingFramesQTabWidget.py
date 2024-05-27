from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from XXRapidFrontingSingleFrameQTabWidget import *


class XXRapidFrontingFramesQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data_dict, settings_dict=None):
        super().__init__()
        self.camera_data_dict = camera_data_dict
        self.SettingsDict = dict()
        self.XXRapidFrontingSingleFrameQTabWidgetDict = dict()
        for mykey, mycameradata, in self.camera_data_dict.items():
            try:
                settings = settings_dict[mykey]
            except:
                settings = None
            try:
                self.XXRapidFrontingSingleFrameQTabWidgetDict[mykey] = XXRapidFrontingSingleFrameQTabWidget(
                    mycameradata,
                    settings)
                self.addTab(self.XXRapidFrontingSingleFrameQTabWidgetDict[mykey],mykey)
                self.SettingsDict[mykey] = self.XXRapidFrontingSingleFrameQTabWidgetDict[mykey].SettingsDict
                self.XXRapidFrontingSingleFrameQTabWidgetDict[mykey].changed.connect(
                    self.OnXXRapidFrontingSingleFrameQTabWidgetDict)
            except Exception as ex:
                print(f'XXRapidFrontingSingleFrameQTabWidgetDict[{mykey}] {ex}')

    def OnXXRapidFrontingSingleFrameQTabWidgetDict(self):
        for mykey, mycamera, in self.XXRapidFrontingSingleFrameQTabWidgetDict.items():
            self.SettingsDict[mykey] = mycamera.SettingsDict
        self.changed.emit()

    def set_data(self, camera_data_dict):
        self.camera_data_dict = camera_data_dict
        for mykey, mycamera, in self.XXRapidFrontingSingleFrameQTabWidgetDict.items():
            mycamera.set_data(self.camera_data_dict[mykey])
        self.changed.emit()
