from PyQt5.QtWidgets import QTabWidget
from XXRapid_Qt_viewer.utility.rtv_reader import *
from .XXRapidOriginalCameraQWidget import *
import os


class XXRapidOriginalQWidget(QTabWidget):
    def __init__(self, before_name='Default_shot/before.rtv', shot_name='Default_shot/shot57.rtv'):
        super().__init__()
        self.before_array = open_rtv(before_name)
        self.shot_array = open_rtv(shot_name)
        self.CameraDataDict = dict()
        for i in range(self.before_array.shape[0]):
            key = f'Camera_{i + 1}'
            self.CameraDataDict[key] = {
                'before': self.before_array[i],
                'shot': self.shot_array[i]
            }
        self.XXRapidOriginalCameraQWidgetDict = dict()
        for my_key, my_camera_data in self.CameraDataDict.items():
            self.XXRapidOriginalCameraQWidgetDict[my_key] = XXRapidOriginalCameraQWidget(
                image_before=my_camera_data['before'],
                image_shot=my_camera_data['shot']
            )
            self.addTab(self.XXRapidOriginalCameraQWidgetDict[my_key], my_key)

    def save_report(self, folder_name):
        if 'XXRapid_original' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/XXRapid_original')
        for mykey, myXXRapidOriginalCameraQWidget in self.XXRapidOriginalCameraQWidgetDict.items():
            myXXRapidOriginalCameraQWidget.figure.savefig(f'{folder_name}/XXRapid_original/{mykey}.png')
