from MPLQWidgets.MatplotlibSingeAxQWidget import *
from .Settings import *
from MPLQWidgets.SettingsMPLQWidget import *


class FrontingSeparatorQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Separator'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.report_path = self.parent.report_path
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=Settings(self)
        )
        self.camera_data = self.parent.camera_data
        self.rotation = self.SettingsBox.RotationSettingLine.value
        self.image_before = self.get_image(self.camera_data['before'])
        self.image_shot = self.get_image(self.camera_data['shot'])
        self.imshow = self.MPLQWidget.ax.imshow(self.image_before, extent=self.get_extent())
        self.x_center = int(self.SettingsBox.XCenterSettingLine.value)
        self.y_center = int(self.SettingsBox.YCenterSettingLine.value)
        self.quarts_dict = self.get_quarts_dict()
        self.x_center_line = self.MPLQWidget.ax.axvline(self.x_center, c='r')
        self.y_center_line = self.MPLQWidget.ax.axhline(self.y_center, c='r')
        self.cid_1 = self.MPLQWidget.figure.canvas.mpl_connect('button_press_event', self.on_mouse_click)

    def on_mouse_click(self, event):
        if event.dblclick:
            x_center, y_center = int(event.xdata), int(event.ydata)
            self.SettingsBox.set_center(x_center, y_center)

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

    def on_settings_box(self):
        self.rotation = self.SettingsBox.RotationSettingLine.value
        self.image_before = self.get_image(self.camera_data['before'])
        self.image_shot = self.get_image(self.camera_data['shot'])

        self.x_center = int(self.SettingsBox.XCenterSettingLine.value)
        self.y_center = int(self.SettingsBox.YCenterSettingLine.value)
        self.x_center_line.set_xdata(self.x_center)
        self.y_center_line.set_ydata(self.y_center)
        self.imshow.set_data(self.image_before)
        self.imshow.set_extent(self.get_extent())
        self.quarts_dict = self.get_quarts_dict()
        super().on_settings_box()

    def save_report(self):
        self.MPLQWidget.figure.savefig(f'{self.report_path}/{self.settings_key}.png')
