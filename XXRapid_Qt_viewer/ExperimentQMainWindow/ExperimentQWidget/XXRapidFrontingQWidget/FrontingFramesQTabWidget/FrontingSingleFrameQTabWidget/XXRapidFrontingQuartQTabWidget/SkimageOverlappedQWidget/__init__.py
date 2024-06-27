from MPLQWidgets.MatplotlibSingeAxQWidget import *
import numpy as np
from scipy.ndimage import gaussian_filter
from .SettingsQWidget import *
from MPLQWidgets.SettingsMPLQWidget import *
from scipy.ndimage import binary_fill_holes
from skimage import filters


class SkimageOverlappedQWidget(SettingsMPLQWidget):
    def __init__(self, camera_data, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        self.camera_data = camera_data
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=SettingsQWidget(self, settings_dict)
        )
        self.sigma_before = self.SettingsBox.SigmaBeforeLine.value
        self.sigma_shot = self.SettingsBox.SigmaShotLine.value
        self.before_threshold = self.SettingsBox.BeforeThresholdSettingLine.value
        self.shutter_1_threshold = self.SettingsBox.Shutter1ThresholdSettingLine.value
        self.shutter_2_threshold = self.SettingsBox.Shutter2ThresholdSettingLine.value
        self.OverlappedImage = self.getOverlappedImage()
        self.imshow = self.MPLQWidget.ax.imshow(self.OverlappedImage)

    def mouse_event_press(self, event):
        self.x_1, self.y_1 = int(event.xdata), int(event.ydata)

    def mouse_event_release(self, event):
        x_2, y_2 = int(event.xdata), int(event.ydata)
        self.SettingsBox.set_line(self.x_1, self.y_1, x_2, y_2)
        self.on_settings_box()

    def set_data(self, camera_data):
        self.camera_data = camera_data
        self.on_settings_box()

    def getOverlappedImage(self):
        fill_before = self.get_fill_before()
        fill_shutter_1 = self.get_fill_shutter_1()
        fill_shutter_2 = self.get_fill_shutter_2()
        fill_overlapped = fill_before*0.3 + fill_shutter_1*0.3 + fill_shutter_2*0.3
        return fill_overlapped

    def get_fill_before(self):
        before_image = filters.gaussian(self.camera_data['before'],
                                        sigma=self.sigma_before)
        thresh = np.where(before_image > 1e-2 * np.max(before_image[np.nonzero(before_image)]) * self.before_threshold,
                          1,
                          0)  # before_image > thresh_value
        fill = binary_fill_holes(thresh)
        return fill

    def get_fill_shutter_1(self):
        shutter_image = filters.gaussian(self.camera_data['shot'],
                                         sigma=self.sigma_shot)
        thresh = np.where(
            shutter_image > 1e-2 * np.max(shutter_image[np.nonzero(shutter_image)]) * self.shutter_1_threshold,
            1,0)
        fill = binary_fill_holes(thresh)
        return fill
    def get_fill_shutter_2(self):
        shutter_image = filters.gaussian(self.camera_data['shot'],
                                         sigma=self.sigma_shot)
        thresh = np.where(
            shutter_image > 1e-2 * np.max(shutter_image[np.nonzero(shutter_image)]) * self.shutter_2_threshold,
            1,0)
        fill = binary_fill_holes(thresh)
        return fill

    # def set_geometry_settings(self, x_min, x_max, y_min, y_max):

    def on_settings_box(self):
        self.SettingsDict = self.SettingsBox.SettingsDict
        self.sigma_before = self.SettingsBox.SigmaBeforeLine.value
        self.sigma_shot = self.SettingsBox.SigmaShotLine.value
        self.before_threshold = self.SettingsBox.BeforeThresholdSettingLine.value
        self.shutter_1_threshold = self.SettingsBox.Shutter1ThresholdSettingLine.value
        self.shutter_2_threshold = self.SettingsBox.Shutter2ThresholdSettingLine.value

        self.OverlappedImage = self.getOverlappedImage()
        extent = [0,
                  self.OverlappedImage.shape[1],
                  self.OverlappedImage.shape[0],
                  0]
        self.imshow.set_extent(extent)
        self.imshow.set_data(self.OverlappedImage)
        super().on_settings_box()
