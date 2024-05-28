from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from XXRapidFrontingSingleFrameQTabWidget import *


class XXRapidFrontingFramesQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.camera_data_dict = camera_data_dict
        self.SettingsDict = settings_dict
        self.XXRapidFrontingSingleFrameQTabWidgetDict = dict()
        self.expansion_dict = dict()
        for mykey, mycameradata in self.camera_data_dict.items():
            try:
                settings = settings_dict[mykey]
            except:
                settings = dict()
            try:
                self.XXRapidFrontingSingleFrameQTabWidgetDict[mykey] = XXRapidFrontingSingleFrameQTabWidget(
                    mycameradata,
                    settings)
                self.addTab(self.XXRapidFrontingSingleFrameQTabWidgetDict[mykey], mykey)
                self.SettingsDict[mykey] = self.XXRapidFrontingSingleFrameQTabWidgetDict[mykey].SettingsDict
                self.expansion_dict[mykey] = self.XXRapidFrontingSingleFrameQTabWidgetDict[mykey].expansion_dict
                self.XXRapidFrontingSingleFrameQTabWidgetDict[mykey].changed.connect(
                    self.OnXXRapidFrontingSingleFrameQTabWidgetDict)
            except Exception as ex:
                print(f'XXRapidFrontingSingleFrameQTabWidgetDict[{mykey}] {ex}')

    def OnXXRapidFrontingSingleFrameQTabWidgetDict(self):
        for mykey, mycamera, in self.XXRapidFrontingSingleFrameQTabWidgetDict.items():
            self.SettingsDict[mykey] = mycamera.SettingsDict
            self.expansion_dict[mykey] = mycamera.expansion_dict
        self.changed.emit()

    def set_data(self, camera_data_dict):
        self.camera_data_dict = camera_data_dict
        for mykey, mycamera, in self.XXRapidFrontingSingleFrameQTabWidgetDict.items():
            mycamera.set_data(self.camera_data_dict[mykey])
        self.changed.emit()
