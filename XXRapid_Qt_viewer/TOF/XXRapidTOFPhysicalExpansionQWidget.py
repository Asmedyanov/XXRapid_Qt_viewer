from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from XXRapid_Qt_viewer.TOF.PhysicalExpansionQTabWidget.GraphicsQTabWidget import *
from XXRapid_Qt_viewer.TOF.PhysicalExpansionQTabWidget.SettingsQWidget import *
import numpy as np


class XXRapidTOFPhysicalExpansionQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, timing_dict, expansion_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.SettingsDict = settings_dict
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.SettingsQWidget = SettingsQWidget(settings_dict)
        self.SettingsDict = self.SettingsQWidget.SettingsDict
        self.dx = 1.0 / self.SettingsQWidget.ScaleSettingLine.value
        self.expansion_pixel_dict = expansion_dict.copy()
        self.timing_dict = timing_dict.copy()
        self.expansion_dict = self.get_expansion_dict()

        self.GraphicsQTabWidget = GraphicsQTabWidget(timing_dict, self.expansion_dict)
        self.QHBoxLayout.addWidget(self.GraphicsQTabWidget, stretch=1)

        self.QHBoxLayout.addWidget(self.SettingsQWidget)
        self.SettingsQWidget.changed.connect(self.OnSettingsQWidget)

    def get_expansion_dict(self):
        expansion_dict = dict()
        for quart_key in self.expansion_pixel_dict.keys():
            front_list = []
            for i in range(len(self.expansion_pixel_dict[quart_key])):
                vector_dict = dict()
                for vector_key in self.expansion_pixel_dict[quart_key][i].keys():
                    if vector_key != 'shutter':
                        vector_dict[vector_key] = self.expansion_pixel_dict[quart_key][i][
                                                      vector_key] * self.dx
                shutter = self.expansion_pixel_dict[quart_key][i]['shutter']
                if shutter != 0:
                    time = self.timing_dict[f'Shutter_{shutter}']['Time']
                    time -= self.timing_dict[f'Pulse_start']['Time']
                else:
                    time = 0
                vector_dict['Time'] = time
                vector_dict['Width'] = self.get_foil_width(vector_dict['x'])
                front_list.append(vector_dict)
            front_list_sorted = sorted(front_list, key=lambda x: x['Time'])
            expansion_dict[quart_key] = front_list_sorted
        return expansion_dict

    def get_foil_width(self, x):
        w_max = self.SettingsQWidget.WidthSettingLine.value
        w_min = self.SettingsQWidget.WaistSettingLine.value
        l = self.SettingsQWidget.LengthSettingLine.value
        w = 2 * (0.5 * w_min + x * (w_max - w_min) / l)
        return w

    def get_motion_dict(self):
        motion_dict = dict()
        for my_key, my_quart in self.expansion_dict.items():
            x_values = [item['x'] for item in my_quart]
            min_x = min(len(x) for x in x_values)
            motion_list = []
            for i in range(min_x):
                motion_time_list = []
                motion_expansion_list = []
                for front in my_quart:
                    motion_time_list.append(front['Time'])
                    motion_expansion_list.append(front['expansion'][i])
                motion_list.append(
                    {
                        'index': i,
                        'x': my_quart[0]['x'][i],
                        'width': my_quart[0]['Width'][i],
                        'time': np.array(motion_time_list),
                        'expansion': np.array(motion_expansion_list)
                    }
                )

            motion_dict[my_key] = motion_list
        return motion_dict

    def OnSettingsQWidget(self):
        self.SettingsDict = self.SettingsQWidget.SettingsDict

        self.dx = 1.0 / self.SettingsQWidget.ScaleSettingLine.value
        self.expansion_dict = self.get_expansion_dict()
        try:
            self.GraphicsQTabWidget.set_data(self.timing_dict, self.expansion_dict)
        except Exception as ex:
            print(f'GraphicsQTabWidget.set_data {ex}')
        self.changed.emit()

    def set_data(self, timing_dict, expansion_dict):
        self.expansion_pixel_dict = expansion_dict.copy()
        self.timing_dict = timing_dict.copy()
        self.OnSettingsQWidget()
