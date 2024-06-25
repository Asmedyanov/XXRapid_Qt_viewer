from SettingsQWidgets.ChildQTabWidget import *
from XXRapid_Qt_viewer.utility.rtv_reader import *
from .Graphics import *
import os


class XXRapidOriginalQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'XXRapid_original')
        self.folder_path = self.parent.folder_path
        self.folder_list = self.parent.folder_list
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.before_name = self.get_before_name()
        self.shot_name = self.get_shot_name()

        self.before_array = open_rtv(self.before_name)
        self.shot_array = open_rtv(self.shot_name)
        self.CameraDataDict = self.get_camera_data_dict()
        self.XXRapidOriginalCameraQWidgetDict = dict()
        for my_key, my_camera_data in self.CameraDataDict.items():
            self.current_key = my_key
            self.current_camera_data = my_camera_data
            try:
                self.XXRapidOriginalCameraQWidgetDict[my_key] = Graphics(self)
                self.addTab(self.XXRapidOriginalCameraQWidgetDict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def get_camera_data_dict(self):
        camera_data_dict = dict()
        for i in range(self.before_array.shape[0]):
            key = f'Camera_{i + 1}'
            camera_data_dict[key] = {
                'before': self.before_array[i],
                'shot': self.shot_array[i]
            }
        return camera_data_dict

    def get_before_name(self):
        before_files_list = [name for name in self.folder_list if
                             name.startswith('before') and name.endswith('rtv')]
        return f'{self.folder_path}/{before_files_list[-1]}'

    def get_shot_name(self):
        shot_files_list = [name for name in self.folder_list if
                           name.startswith('shot') and name.endswith('rtv')]
        # print(f'Folder contains shot files\n{shot_files_list}\nI took the last one')
        return f'{self.folder_path}/{shot_files_list[-1]}'

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for my_key, myXXRapidOriginalCameraQWidget in self.XXRapidOriginalCameraQWidgetDict.items():
            myXXRapidOriginalCameraQWidget.save_report()
