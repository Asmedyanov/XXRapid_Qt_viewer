import os

from PyQt5.QtWidgets import QTabWidget
from .XXRapidOverlappedCameraQWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class XXRapidOverlappedQWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Overlapped_image')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.XXRapidOriginalQWidget = self.parent.XXRapidOriginalQWidget
        self.camera_dict = self.XXRapidOriginalQWidget.CameraDataDict
        self.OverlappedCameraQWidgetDict = dict()
        self.OverlappedImagesDict = dict()
        for my_key, my_camera_data in self.camera_dict.items():
            self.current_key = my_key
            self.current_camera_data = my_camera_data
            try:
                self.OverlappedCameraQWidgetDict[my_key] = XXRapidOverlappedCameraQWidget(self)
                self.addTab(self.OverlappedCameraQWidgetDict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def onOverlappedCameraQWidget(self):
        for my_key, my_OverlappedCameraQWidget in self.OverlappedCameraQWidgetDict.items():
            self.SettingsDict[my_key] = self.OverlappedCameraQWidgetDict[my_key].SettingsDict
        self.changed.emit()

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for mykey, myOverlappedCameraQWidget in self.OverlappedCameraQWidgetDict.items():
            myOverlappedCameraQWidget.save_report()
