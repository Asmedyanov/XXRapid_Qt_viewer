from SettingsQWidgets.ChildQTabWidget import *
from XXRapid_Qt_viewer.utility.rtv_reader import *
from .Graphics import *
import os


class XXRapidOriginalQWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'XXRapid_original')
        self.folder_path = self.parent.folder_path
        self.folder_list = self.parent.folder_list
        self.before_name = self.get_before_name()
        self.shot_name = self.get_shot_name()

        self.before_array = open_rtv(self.before_name)
        self.shot_array = open_rtv(self.shot_name)
        self.CameraDataDict = dict()
        for i in range(self.before_array.shape[0]):
            key = f'Camera_{i + 1}'
            self.CameraDataDict[key] = {
                'before': self.before_array[i],
                'shot': self.shot_array[i]
            }
        self.XXRapidOriginalCameraQWidgetDict = dict()
        for my_key, my_camera_data in self.CameraDataDict.items():
            self.XXRapidOriginalCameraQWidgetDict[my_key] = Graphics(
                image_before=my_camera_data['before'],
                image_shot=my_camera_data['shot']
            )
            self.addTab(self.XXRapidOriginalCameraQWidgetDict[my_key], my_key)

    def get_before_name(self):
        before_files_list = [name for name in self.folder_list if
                             name.startswith('before') and name.endswith('rtv')]
        return f'{self.folder_path}/{before_files_list[-1]}'

    def get_shot_name(self):
        shot_files_list = [name for name in self.folder_list if
                           name.startswith('shot') and name.endswith('rtv')]
        # print(f'Folder contains shot files\n{shot_files_list}\nI took the last one')
        return f'{self.folder_path}/{shot_files_list[-1]}'

    def save_report(self, folder_name):
        if 'XXRapid_original' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/XXRapid_original')
        for my_key, myXXRapidOriginalCameraQWidget in self.XXRapidOriginalCameraQWidgetDict.items():
            myXXRapidOriginalCameraQWidget.figure.savefig(f'{folder_name}/XXRapid_original/{my_key}.png')
