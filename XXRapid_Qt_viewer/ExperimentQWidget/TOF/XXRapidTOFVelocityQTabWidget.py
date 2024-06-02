import pandas as pd
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
import os


class XXRapidTOFVelocityQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, motion_approximated_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.SettingsDict = settings_dict
        self.motion_approximated_dict = motion_approximated_dict
        self.velocity_dict = self.get_velocity_dict()
        self.XXRapidTOFVelocityQWidgetDict = dict()
        for my_key, my_velocity_df in self.velocity_dict.items():
            try:
                self.XXRapidTOFVelocityQWidgetDict[my_key] = XXRapidTOFVelocityQWidget(my_velocity_df)
                self.addTab(self.XXRapidTOFVelocityQWidgetDict[my_key], my_key)
                self.XXRapidTOFVelocityQWidgetDict[my_key].changed.connect(self.on_graph_changed)
            except Exception as ex:
                print(f'XXRapidTOFVelocityQWidgetDict[{my_key}] {ex}')

    def on_graph_changed(self):
        self.changed.emit()

    def set_data(self, motion_approximated_dict):
        self.motion_approximated_dict = motion_approximated_dict
        self.velocity_dict = self.get_velocity_dict()
        for my_key, myGraphics in self.XXRapidTOFVelocityQWidgetDict.items():
            myGraphics.set_data(self.velocity_dict[my_key])

    def get_velocity_dict(self):
        velocity_dict = dict()
        for my_key, my_quart in self.motion_approximated_dict.items():
            velocity_list = []
            velocity_error_list = []
            onset_list = []
            onset_error_list = []
            x_list = []
            cross_section_list = []
            for motion_data in my_quart:
                x_list.append(motion_data['x'])
                cross_section_list.append(motion_data['width'])
                velocity_list.append(motion_data['velocity'] * 1e3)
                velocity_error_list.append(motion_data['velocity_error'] * 1e3)
                onset_list.append(motion_data['onset_time'])
                onset_error_list.append(motion_data['onset_time_error'])

            velocity_dict[my_key] = pd.DataFrame({
                'x': x_list,
                'width': cross_section_list,
                'velocity': velocity_list,
                'velocity_error': velocity_error_list,
                'onset_time': onset_list,
                'onset_time_error': onset_error_list,
            })
        return velocity_dict

    def save_report(self, folder_name):
        key = 'XXRapid_velocity_and_onset'
        if key not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/{key}')

        for mykey, myGraphics in self.XXRapidTOFVelocityQWidgetDict.items():
            myGraphics.figure.savefig(
                f'{folder_name}/{key}/{mykey}.png')
            self.velocity_dict[mykey].to_csv(f'{folder_name}/{key}/{mykey}.csv')
