import os

from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
import numpy as np
from .Settings import *
from .GraphicsQTabWidget import *
from SettingsQWidgets.ChildQWidget import *


class PhysicalExpansionQWidget(ChildQWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Physical_expansion')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.XXRapidFrontingQWidget = self.parent.XXRapidFrontingQWidget
        self.XXRapidFrontingQWidget.changed.connect(self.refresh)
        self.WaveformTimingQWidget = self.parent.WaveformTimingQWidget
        # self.WaveformTimingQWidget.changed.connect(self.refresh)
        self.expansion_pixel_dict = self.XXRapidFrontingQWidget.XXRapidFrontingFramesQTabWidget.expansion_dict.copy()
        self.timing_dict = self.WaveformTimingQWidget.t_shutter_dict.copy()
        self.t_start = self.WaveformTimingQWidget.t_start
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.SettingsQWidget = Settings(self)
        self.dx = 1.0 / self.SettingsQWidget.ScaleSettingLine.value
        self.expansion_dict = self.get_expansion_dict()
        self.GraphicsQTabWidget = GraphicsQTabWidget(self)
        self.QHBoxLayout.addWidget(self.GraphicsQTabWidget, stretch=1)

        self.QHBoxLayout.addWidget(self.SettingsQWidget)
        self.SettingsQWidget.changed.connect(self.OnSettingsQWidget)

    def refresh(self):
        self.expansion_pixel_dict = self.XXRapidFrontingQWidget.XXRapidFrontingFramesQTabWidget.expansion_dict.copy()
        self.timing_dict = self.WaveformTimingQWidget.t_shutter_dict.copy()
        self.t_start = self.WaveformTimingQWidget.t_start
        self.OnSettingsQWidget()

    def get_expansion_dict(self):
        expansion_dict = dict()
        for my_key, my_expansion_dict in self.expansion_pixel_dict.items():
            my_dict = dict()
            for shutter_key, my_expansion in my_expansion_dict.items():
                my_dict[shutter_key] = {
                    'trust': my_expansion['trust'],
                    'time': self.timing_dict[f'Shutter_{shutter_key}'] - self.t_start,
                    'x': self.dx * np.array(my_expansion['x']),
                    'width': self.get_foil_width(self.dx * np.array(my_expansion['x'])),
                    'expansion': self.dx * np.array(my_expansion['expansion'])
                }
            expansion_dict[my_key] = dict(sorted(my_dict.items()))
        return expansion_dict

    def get_foil_width(self, x):
        w_max = self.SettingsQWidget.WidthSettingLine.value
        w_min = self.SettingsQWidget.WaistSettingLine.value
        length = self.SettingsQWidget.LengthSettingLine.value
        w = 2 * (0.5 * w_min + x * (w_max - w_min) / length)
        return w

    def OnSettingsQWidget(self):
        self.dx = 1.0 / self.SettingsQWidget.ScaleSettingLine.value
        self.expansion_dict = self.get_expansion_dict()
        try:
            self.GraphicsQTabWidget.refresh()
        except Exception as ex:
            print(ex)
        self.changed.emit()

    def save_report(self):
        try:
            self.GraphicsQTabWidget.save_report()
        except Exception as ex:
            print(ex)

    def save_origin_pro(self, op):
        for quart_key, quart_data in self.expansion_dict.items():
            name_workbook = f'{self.settings_key}_{quart_key}'
            workbook = op.new_book(lname=name_workbook)
            graphic = op.new_graph(lname=name_workbook)
            for shutter_key, shutter_data in quart_data.items():
                name_sheet = f'{name_workbook}_{shutter_key}'
                sheet = workbook.add_sheet(name=name_sheet)
                sheet.from_dict({
                    'x': shutter_data['x'],
                    'width': shutter_data['width'],
                    'expansion': shutter_data['expansion']
                })

                plot = graphic[0].add_plot(sheet, colx=1, coly=2)

            graphic[0].rescale()
