from PyQt5.QtWidgets import QWidget, QHBoxLayout
import numpy as np
from .SettingsQWidget import *
from .GraphicsQTabWidget import *
import os


class XXRapidTOFMotionQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, motion_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.SettingsDict = settings_dict
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.SettingsQWidget = SettingsQWidget(settings_dict)
        self.SettingsDict = self.SettingsQWidget.SettingsDict
        self.cross_1 = int(self.SettingsQWidget.CrossSection1SettingLine.value)
        self.cross_2 = int(self.SettingsQWidget.CrossSection2SettingLine.value)
        self.motion_dict = motion_dict
        self.motion_approximated_dict = self.get_approximation()
        self.GraphicsQTabWidget = GraphicsQTabWidget(motion_dict,
                                                     self.motion_approximated_dict, [self.cross_1, self.cross_2])

        self.QHBoxLayout.addWidget(self.GraphicsQTabWidget, stretch=1)

        self.QHBoxLayout.addWidget(self.SettingsQWidget)
        self.SettingsQWidget.changed.connect(self.OnSettingsQWidget)

    def get_approximation(self):
        motion_approximated_dict = dict()
        for my_key, my_quart in self.motion_dict.items():
            approximated_list = []
            for motion_data in my_quart:
                t_data_0 = motion_data['time']
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
                w = np.arange(len(t_data)) + 0.5 * len(t_data)
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
                        'velocity': velocity,
                        'velocity_error': velocity_error,
                        'onset_time': onset_time,
                        'onset_time_error': onset_time_error,
                        't_approx': np.arange(onset_time, t_data_0[-1]),
                        'expansion_approx': np.poly1d(line_poly_coef)(np.arange(onset_time, t_data_0[-1]))
                    }
                )
            motion_approximated_dict[my_key] = approximated_list
        return motion_approximated_dict

    def OnSettingsQWidget(self):
        self.SettingsDict = self.SettingsQWidget.SettingsDict
        self.cross_1 = int(self.SettingsQWidget.CrossSection1SettingLine.value)
        self.cross_2 = int(self.SettingsQWidget.CrossSection2SettingLine.value)

        try:
            self.GraphicsQTabWidget.set_data(self.motion_dict, self.motion_approximated_dict,
                                             [self.cross_1, self.cross_2])
        except Exception as ex:
            print(f'GraphicsQTabWidget.set_data {ex}')

    def set_data(self, motion_dict):
        self.motion_dict = motion_dict
        self.motion_approximated_dict = self.get_approximation()
        self.OnSettingsQWidget()

    def save_report(self, folder_name):
        if 'XXRapid_motion' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/XXRapid_motion')
        for mykey, myGraphics in self.GraphicsQTabWidget.GraphicsDict.items():
            myGraphics.figure.savefig(
                f'{folder_name}/XXRapid_motion/{mykey}.png')
