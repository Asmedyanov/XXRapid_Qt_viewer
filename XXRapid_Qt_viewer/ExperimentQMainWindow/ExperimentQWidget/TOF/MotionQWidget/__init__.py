from PyQt5.QtWidgets import QWidget, QHBoxLayout
import numpy as np
from .Settings import *
from .GraphicsQTabWidget import *
import os
from SettingsQWidgets.ChildQWidget import *


class MotionQWidget(ChildQWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Motion')
        self.PhysicalExpansionQWidget = self.parent.PhysicalExpansionQWidget

        self.expansion_dict = self.PhysicalExpansionQWidget.expansion_dict
        self.PhysicalExpansionQWidget.changed.connect(self.refresh)

        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.SettingsQWidget = Settings(self)
        self.cross_1 = int(self.SettingsQWidget.CrossSection1SettingLine.value)
        self.cross_2 = int(self.SettingsQWidget.CrossSection2SettingLine.value)
        self.index_to_plot_list = [self.cross_1, self.cross_2]
        self.motion_dict = self.get_motion_dict()
        self.motion_approximated_dict = self.get_approximation()
        self.GraphicsQTabWidget = GraphicsQTabWidget(self)

        self.QHBoxLayout.addWidget(self.GraphicsQTabWidget, stretch=1)

        self.QHBoxLayout.addWidget(self.SettingsQWidget)
        self.SettingsQWidget.changed.connect(self.on_settings)

    def get_motion_dict(self):
        motion_dict = dict()
        for my_key, my_quart in self.expansion_dict.items():
            x_values = [item['x'] for item in my_quart.values()]
            min_x = min(len(x) for x in x_values)
            motion_list = []
            for i in range(min_x):
                motion_time_list = []
                motion_expansion_list = []
                for front in my_quart.values():
                    motion_time_list.append(front['time'])
                    motion_expansion_list.append(front['expansion'][i])
                motion_list.append(
                    {
                        'index': i,
                        'x': my_quart['1']['x'][i],
                        'width': my_quart['1']['width'][i],
                        'time': np.array(motion_time_list),
                        'expansion': np.array(motion_expansion_list)
                    }
                )

            motion_dict[my_key] = motion_list
        return motion_dict

    def refresh(self):
        self.expansion_dict = self.PhysicalExpansionQWidget.expansion_dict
        self.motion_dict = self.get_motion_dict()
        self.motion_approximated_dict = self.get_approximation()
        self.on_settings()
        self.changed.emit()

    def get_approximation(self):
        motion_approximated_dict = dict()
        for my_key, my_quart in self.motion_dict.items():
            approximated_list = []
            for motion_data in my_quart:
                t_data_0 = motion_data['time'] * 1e9
                x_data_0 = motion_data['expansion']
                t_data = []
                expansion_data = []

                for k in range(8):
                    if x_data_0[k] <= 0:

                        try:
                            if x_data_0[k + 1] == 0:
                                continue
                        except:
                            continue
                    t_data.append(t_data_0[k])
                    expansion_data.append(x_data_0[k])
                if len(t_data) < 4:
                    continue
                w = np.arange(len(t_data))+ 0.05 * len(t_data)
                w = np.exp(w)
                # w = np.ones(len(t_data))
                w = w / np.sum(w)
                line_poly_coef, res, _, _, _ = np.polyfit(t_data, expansion_data, 1, full=True, w=w)

                perr = np.sqrt(np.sum(res))
                velocity = line_poly_coef[0]
                velocity_error = velocity * perr
                onset_time = -line_poly_coef[1] / velocity
                onset_time_error = perr * onset_time
                approximated_list.append(
                    {
                        'width': motion_data['width'],
                        'x': motion_data['x'],
                        'index': motion_data['index'],
                        'velocity': velocity,  # km/s
                        'velocity_error': velocity_error,  # km/s
                        'onset_time': onset_time,  # ns
                        'onset_time_error': onset_time_error,
                        't_approx': np.arange(onset_time, t_data_0[-1]),
                        'expansion_approx': np.poly1d(line_poly_coef)(np.arange(onset_time, t_data_0[-1]))
                    }
                )
            motion_approximated_dict[my_key] = approximated_list
        return motion_approximated_dict

    def on_settings(self):
        self.cross_1 = int(self.SettingsQWidget.CrossSection1SettingLine.value)
        self.cross_2 = int(self.SettingsQWidget.CrossSection2SettingLine.value)
        self.index_to_plot_list = [self.cross_1, self.cross_2]
        try:
            self.GraphicsQTabWidget.refresh()
        except Exception as ex:
            print(f'GraphicsQTabWidget.set_data {ex}')

    def set_data(self, motion_dict):
        self.motion_dict = motion_dict
        self.motion_approximated_dict = self.get_approximation()
        self.on_settings()

    def save_report(self, folder_name):
        if 'XXRapid_motion' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/XXRapid_motion')
        for mykey, myGraphics in self.GraphicsQTabWidget.GraphicsDict.items():
            myGraphics.figure.savefig(
                f'{folder_name}/XXRapid_motion/{mykey}.png')
