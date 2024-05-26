from PyQt5.QtWidgets import QTabWidget
from XXRapidOverlappedCameraQWidget import *


class XXRapidOverlappedQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, camera_dict, settings_dict=None):
        super().__init__()
        self.OverlappedCameraQWidgetDict = dict()
        self.SettingsDict = dict()
        self.OverlappedImagesDict = dict()
        for my_key, my_camera_data in camera_dict.items():
            try:
                settings = settings_dict[my_key]
            except:
                settings = None
            try:
                self.OverlappedCameraQWidgetDict[my_key] = XXRapidOverlappedCameraQWidget(my_camera_data, settings)
                self.SettingsDict[my_key] = self.OverlappedCameraQWidgetDict[my_key].SettingsDict
                self.OverlappedImagesDict[my_key] = self.OverlappedCameraQWidgetDict[my_key].OverlappedImage
                self.addTab(self.OverlappedCameraQWidgetDict[my_key], my_key)
            except Exception as ex:
                print(f'OverlappedCameraQWidgetDict[{my_key}] {ex}')

    def Save_Report(self, folder_name):
        if 'XXRapid_overlapped' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/XXRapid_overlapped')
        for mykey, myOverlappedCameraQWidget in self.OverlappedCameraQWidgetDict.items():
            myOverlappedCameraQWidget.MatplotlibSingeAxQWidget.figure.savefig(
                f'{folder_name}/XXRapid_overlapped/{mykey}.png')
