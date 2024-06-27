from MPLQWidgets.MatplotlibSingeAxQWidget import *
import numpy as np
from .Settings import *
from .Graphics import *
from MPLQWidgets.SettingsMPLQWidget import *
from scipy.ndimage import binary_fill_holes
from skimage import filters


class TracerQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Tracer'
        self.report_path = self.parent.report_path
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.camera_data = self.parent.camera_data
        super().__init__(
            MPLQWidget=Graphics(),
            settings_box=Settings(self)
        )

        self.sigma_before = self.SettingsBox.SigmaBeforeLine.value
        self.sigma_shot = self.SettingsBox.SigmaShotLine.value
        self.sigma_overlapped = self.SettingsBox.SigmaOverlappedLine.value
        self.mask_threshold = self.SettingsBox.MaskThresholdSettingLine.value
        self.x_min = self.SettingsBox.XMinLine.value
        self.y_min = self.SettingsBox.YMinLine.value
        self.x_max = self.SettingsBox.XMaxLine.value
        self.y_max = self.SettingsBox.YMaxLine.value
        self.OverlappedImage = self.get_overlapped_image()
        self.imshow = self.MPLQWidget.ax.imshow(self.OverlappedImage)
        self.TraceLine, = self.MPLQWidget.ax.plot(
            [self.x_min, self.x_max],
            [self.y_min, self.y_max],
            '-or'
        )
        self.cid_1 = self.MPLQWidget.figure.canvas.mpl_connect('button_press_event',
                                                               self.mouse_event_press)
        self.cid_2 = self.MPLQWidget.figure.canvas.mpl_connect('button_release_event',
                                                               self.mouse_event_release)
        self.traced_image = self.get_traced_image()

    def refresh(self):
        self.camera_data = self.parent.camera_data
        self.on_settings_box()

    def mouse_event_press(self, event):
        self.x_1, self.y_1 = int(event.xdata), int(event.ydata)

    def mouse_event_release(self, event):
        x_2, y_2 = int(event.xdata), int(event.ydata)
        self.SettingsBox.set_line(self.x_1, self.y_1, x_2, y_2)
        self.on_settings_box()

    def get_overlapped_image(self):
        before_image = filters.gaussian(self.camera_data['before'],
                                        sigma=self.sigma_before)
        thresh = np.where(before_image > 1e-2 * np.max(before_image[np.nonzero(before_image)]) * self.mask_threshold, 1,
                          0)  # before_image > thresh_value
        fill = binary_fill_holes(thresh)
        shot_image = filters.gaussian(self.camera_data['shot'],
                                      sigma=self.sigma_shot)
        shadow_image = np.where(shot_image < before_image,  # + before_image.std(),
                                shot_image,
                                before_image)  # + before_image.std())

        overlapped_image = np.where(before_image <= 0, 0,
                                    shadow_image / before_image) * fill
        overlapped_image = filters.gaussian(overlapped_image, sigma=self.sigma_overlapped)
        return overlapped_image

    def on_settings_box(self):
        self.SettingsDict = self.SettingsBox.SettingsDict
        self.sigma_before = self.SettingsBox.SigmaBeforeLine.value
        self.sigma_shot = self.SettingsBox.SigmaShotLine.value
        self.sigma_overlapped = self.SettingsBox.SigmaOverlappedLine.value
        self.mask_threshold = self.SettingsBox.MaskThresholdSettingLine.value
        self.x_min = self.SettingsBox.XMinLine.value
        self.y_min = self.SettingsBox.YMinLine.value
        self.x_max = self.SettingsBox.XMaxLine.value
        self.y_max = self.SettingsBox.YMaxLine.value
        self.TraceLine.set_data(
            [self.x_min, self.x_max],
            [self.y_min, self.y_max],
        )
        self.OverlappedImage = self.get_overlapped_image()
        extent = [0,
                  self.OverlappedImage.shape[1],
                  self.OverlappedImage.shape[0],
                  0]
        self.imshow.set_extent(extent)
        self.imshow.set_data(self.OverlappedImage)
        self.traced_image = self.get_traced_image()
        super().on_settings_box()

    def get_traced_image(self):
        min_x_index = int(min(self.x_min, self.x_max))
        max_x_index = int(max(self.x_min, self.x_max))
        min_y_index = int(min(self.y_min, self.y_max))
        max_y_index = int(max(self.y_min, self.y_max))
        traced_image = self.OverlappedImage[min_y_index:max_y_index, min_x_index:max_x_index]
        return traced_image

    def save_report(self):
        self.MPLQWidget.figure.savefig(f'{self.report_path}/{self.settings_key}.png')
