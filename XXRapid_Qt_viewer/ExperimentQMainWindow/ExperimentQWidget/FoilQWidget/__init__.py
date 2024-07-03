from MPLQWidgets.SettingsMPLQWidget import *
from .Settings import *
from .Graphics import *


class FoilQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Foil'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.settings = Settings(self)
        self.points_x, self.points_y = self.get_points()
        super().__init__(settings_box=self.settings, MPLQWidget=Graphics(self))

    def get_points(self):
        length = self.settings.LengthSettingLine.value
        width = self.settings.WidthSettingLine.value
        waist = self.settings.WaistSettingLine.value
        x_list = [
            waist,
            width,
            -width,
            -waist,
            -width,
            width,
            waist

        ]

        y_list = [
            0,
            length,
            length,
            0,
            -length,
            -length,
            0

        ]
        x_array = np.array(x_list) / 2
        y_array = np.array(y_list) / 2

        return x_array, y_array

    def on_settings_box(self):
        self.points_x, self.points_y = self.get_points()
        self.MPLQWidget.refresh()
        super().on_settings_box()
