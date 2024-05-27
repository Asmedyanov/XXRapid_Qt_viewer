from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from MatplotlibSingeAxQWidget import *
from XXRapidFrontingSeparatorSettingsQWidget import *
import numpy as np


class XXRapidFrontingSeparatorQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data, settings_dict=None):
        super().__init__()
        self.QHBoxLayout = QHBoxLayout()
        self.SettingsDict = dict()
        self.setLayout(self.QHBoxLayout)
        self.camera_data = camera_data
        self.MatplotlibSingeAxQWidget = MatplotlibSingeAxQWidget()
        self.QHBoxLayout.addWidget(self.MatplotlibSingeAxQWidget)
        self.XXRapidFrontingSeparatorSettingsQWidget = XXRapidFrontingSeparatorSettingsQWidget(settings_dict)
        self.QHBoxLayout.addWidget(self.XXRapidFrontingSeparatorSettingsQWidget)
        self.XXRapidFrontingSeparatorSettingsQWidget.changed.connect(self.OnXXRapidFrontingSeparatorSettingsQWidget)
        self.rotation = self.XXRapidFrontingSeparatorSettingsQWidget.RotationSettingLine.value
        self.image_before = self.get_image(self.camera_data['before'])
        self.image_shot = self.get_image(self.camera_data['shot'])
        self.imshow = self.MatplotlibSingeAxQWidget.ax.imshow(self.image_before, extent=self.get_extent())
        self.x_center = int(self.XXRapidFrontingSeparatorSettingsQWidget.XCenterSettingLine.value)
        self.y_center = int(self.XXRapidFrontingSeparatorSettingsQWidget.YCenterSettingLine.value)
        self.quarts_dict = self.get_quarts_dict()
        self.x_center_line = self.MatplotlibSingeAxQWidget.ax.axvline(self.x_center, c='r')
        self.y_center_line = self.MatplotlibSingeAxQWidget.ax.axhline(self.y_center, c='r')
        self.cid_1 = self.MatplotlibSingeAxQWidget.figure.canvas.mpl_connect('button_press_event', self.On_mouse_click)

    def On_mouse_click(self, event):
        if event.dblclick:
            x_center, y_center = int(event.xdata), int(event.ydata)
            self.XXRapidFrontingSeparatorSettingsQWidget.set_center(x_center, y_center)

    def get_extent(self):
        extent = [0,
                  self.image_before.shape[1],
                  self.image_before.shape[0],
                  0]
        return extent

    def get_image(self, image):
        if self.rotation == '90':
            return np.transpose(image)
        return image

    def get_quarts_dict(self):
        quarts_dict = {
            'Quart_1': {'before': self.image_before[:self.y_center, self.x_center:],
                        'shot': self.image_shot[:self.y_center, self.x_center:]},
            'Quart_2': {'before': np.flip(self.image_before[:self.y_center, :self.x_center], axis=1),
                        'shot': np.flip(self.image_shot[:self.y_center, :self.x_center], axis=1)},
            'Quart_3': {'before': np.flip(
                np.flip(self.image_before[self.y_center:, :self.x_center], axis=0), axis=1),
                'shot': np.flip(np.flip(self.image_shot[self.y_center:, :self.x_center], axis=0), axis=1)},
            'Quart_4': {'before': np.flip(self.image_before[self.y_center:, self.x_center:], axis=0),
                        'shot': np.flip(self.image_shot[self.y_center:, self.x_center:], axis=0)},
        }
        return quarts_dict

    def OnXXRapidFrontingSeparatorSettingsQWidget(self):
        self.rotation = self.XXRapidFrontingSeparatorSettingsQWidget.RotationSettingLine.value
        self.image_before = self.get_image(self.camera_data['before'])
        self.image_shot = self.get_image(self.camera_data['shot'])

        self.x_center = int(self.XXRapidFrontingSeparatorSettingsQWidget.XCenterSettingLine.value)
        self.y_center = int(self.XXRapidFrontingSeparatorSettingsQWidget.YCenterSettingLine.value)
        self.x_center_line.set_xdata(self.x_center)
        self.y_center_line.set_ydata(self.y_center)
        self.imshow.set_data(self.image_before)
        self.imshow.set_extent(self.get_extent())

        self.MatplotlibSingeAxQWidget.changed.emit()
        self.SettingsDict = self.XXRapidFrontingSeparatorSettingsQWidget.SettingsDict
        self.quarts_dict = self.get_quarts_dict()
        self.changed.emit()
