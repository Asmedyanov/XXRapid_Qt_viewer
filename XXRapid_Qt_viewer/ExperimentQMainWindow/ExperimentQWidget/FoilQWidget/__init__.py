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
        self.foil_length, self.foil_width, self.waist, self.points_x, self.points_y = self.get_points()
        self.thickness = self.settings.ThicknessSettingLine.value
        self.surface = self.get_surface()
        self.volume = self.get_volume()
        self.mass = self.get_mass()
        super().__init__(settings_box=self.settings, MPLQWidget=Graphics(self))

    def get_surface(self):
        """

        :return:
        surface area in mm^2
        """
        s = self.foil_length * (self.waist + self.foil_width) / 2
        return s

    def get_volume(self):
        """

        :return:
        volume of the foil in cm^3
        """
        v = self.surface * self.thickness * 1e-3  # mm^3

        return v * 1e-3

    def get_mass(self):
        """

        :return:
        mass of the foil in grams
        """
        m = self.volume * self.settings.DensitySettingLine.value
        return m

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

        return length, width, waist, x_array, y_array

    def on_settings_box(self):
        self.foil_length, self.foil_width, self.waist, self.points_x, self.points_y = self.get_points()
        self.thickness = self.settings.ThicknessSettingLine.value
        self.MPLQWidget.refresh()
        super().on_settings_box()

    def width_function(self, x):
        """
        foil width
        :param x: coordinate along the current direction, mm
        :return: width of the foil in the direction perpendicular to the current direction, mm
        """
        w = 2 * (0.5 * self.waist + x * (self.foil_width - self.waist) / self.foil_length)
        return w

    def cross_section_function(self, x):
        """
                foil width
                :param x: coordinate along the current direction, mm
                :return: cross_section of the foil in the direction perpendicular to the current direction, mm^2
                """
        a = self.width_function(x) * self.thickness * 1e-3
        return a
