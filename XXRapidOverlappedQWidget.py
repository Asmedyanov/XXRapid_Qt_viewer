from PyQt5.QtWidgets import QTabWidget
from XXRapidOverlappedCameraQWidget import *


class XXRapidOverlappedQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, camera_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.OverlappedCameraQWidgetDict = dict()
        self.SettingsDict = settings_dict
        self.OverlappedImagesDict = dict()
        for my_key, my_camera_data in camera_dict.items():
            try:
                settings = settings_dict[my_key]
            except:
                settings = dict()
            try:
                self.OverlappedCameraQWidgetDict[my_key] = XXRapidOverlappedCameraQWidget(my_camera_data, settings)
                self.OverlappedCameraQWidgetDict[my_key].changed.connect(self.onOverlappedCameraQWidget)
                self.SettingsDict[my_key] = self.OverlappedCameraQWidgetDict[my_key].SettingsDict
                self.OverlappedImagesDict[my_key] = self.OverlappedCameraQWidgetDict[my_key].OverlappedImage
                self.addTab(self.OverlappedCameraQWidgetDict[my_key], my_key)
            except Exception as ex:
                print(f'OverlappedCameraQWidgetDict[{my_key}] {ex}')

    def onOverlappedCameraQWidget(self):
        for my_key, my_OverlappedCameraQWidget in self.OverlappedCameraQWidgetDict.items():
            self.SettingsDict[my_key] = self.OverlappedCameraQWidgetDict[my_key].SettingsDict
        self.changed.emit()

    def save_report(self, folder_name):
        if 'XXRapid_overlapped' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/XXRapid_overlapped')
        for mykey, myOverlappedCameraQWidget in self.OverlappedCameraQWidgetDict.items():
            myOverlappedCameraQWidget.MatplotlibSingeAxQWidget.figure.savefig(
                f'{folder_name}/XXRapid_overlapped/{mykey}.png')
