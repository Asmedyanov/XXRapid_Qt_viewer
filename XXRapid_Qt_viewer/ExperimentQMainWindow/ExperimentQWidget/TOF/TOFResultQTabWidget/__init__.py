from PyQt5.QtWidgets import QTabWidget
from .Graphics import *
from SettingsQWidgets.ChildQTabWidget import *


class TOFResultQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Result')
        self.MotionQTabWidget = self.parent.MotionQTabWidget
        self.MotionQTabWidget.changed.connect(self.refresh)
        self.motion_approximated_dict = self.MotionQTabWidget.motion_approximated_dict
        self.velocity_dict = self.get_velocity_dict()
        self.XXRapidTOFVelocityQWidgetDict = dict()
        for my_key, my_df in self.velocity_dict.items():
            self.current_key = my_key
            self.current_df = my_df
            try:
                self.XXRapidTOFVelocityQWidgetDict[my_key] = Graphics(self)
                self.addTab(self.XXRapidTOFVelocityQWidgetDict[my_key], my_key)
            except Exception as ex:
                print(f'XXRapidTOFVelocityQWidgetDict[{my_key}] {ex}')

    def refresh(self):
        self.motion_approximated_dict = self.MotionQTabWidget.motion_approximated_dict
        self.velocity_dict = self.get_velocity_dict()
        for my_key, my_df in self.velocity_dict.items():
            self.current_key = my_key
            self.current_df = my_df
            try:
                self.XXRapidTOFVelocityQWidgetDict[my_key].refresh()
            except Exception as ex:
                print(f'XXRapidTOFVelocityQWidgetDict[{my_key}] {ex}')
        self.changed.emit()

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

            df= pd.DataFrame({
                'x': x_list,
                'width': cross_section_list,
                'velocity': velocity_list,
                'velocity_error': velocity_error_list,
                'onset_time': onset_list,
                'onset_time_error': onset_error_list,
            })
            df_smooth = df.rolling(40, min_periods=1).mean()
            velocity_dict[my_key]=df_smooth
        return velocity_dict

    def save_report(self, folder_name):
        key = 'XXRapid_velocity_and_onset'
        if key not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/{key}')

        for mykey, myGraphics in self.XXRapidTOFVelocityQWidgetDict.items():
            myGraphics.figure.savefig(
                f'{folder_name}/{key}/{mykey}.png')
            self.velocity_dict[mykey].to_csv(f'{folder_name}/{key}/{mykey}.csv')
