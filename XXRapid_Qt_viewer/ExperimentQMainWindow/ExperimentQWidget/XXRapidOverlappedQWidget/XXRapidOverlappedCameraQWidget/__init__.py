from .XXRapidOverlappedCameraSettingsQWidget import *
from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *
import numpy as np
from scipy.ndimage import binary_fill_holes
from skimage import filters, morphology, segmentation
import skimage


class XXRapidOverlappedCameraQWidget(SettingsMPLQWidget):
    def __init__(self, camera_data, settings_dict=None):
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=XXRapidOverlappedCameraSettingsQWidget(settings_dict)
        )
        self.camera_data = camera_data
        self.MPLQWidget.ax.set(title='Overlapped image', xlabel='x,mm', ylabel='y,mm')
        self.dx = 1.0 / self.SettingsBox.ScaleSettingLine.value
        self.sigma_before = self.SettingsBox.SigmaBeforeLine.value
        self.sigma_shot = self.SettingsBox.SigmaShotLine.value
        self.sigma_overlapped = self.SettingsBox.SigmaOverlappedLine.value
        self.mask_threshold = self.SettingsBox.MaskThresholdSettingLine.value
        self.OverlappedImage = self.getOverlappedImage()

        self.imshow = self.MPLQWidget.ax.imshow(self.OverlappedImage, extent=self.get_extent())

    def get_extent(self):
        extent = [-self.OverlappedImage.shape[1] * self.dx // 2,
                  self.OverlappedImage.shape[1] * self.dx // 2,
                  self.OverlappedImage.shape[0] * self.dx // 2,
                  -self.OverlappedImage.shape[0] * self.dx // 2]
        return extent

    def getOverlappedImage(self):
        before_image = filters.gaussian(self.camera_data['before'],
                                        sigma=self.sigma_before)
        thresh_value = filters.threshold_otsu(before_image)
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
        self.dx = 1.0 / self.SettingsBox.ScaleSettingLine.value
        self.sigma_before = self.SettingsBox.SigmaBeforeLine.value
        self.sigma_shot = self.SettingsBox.SigmaShotLine.value
        self.sigma_overlapped = self.SettingsBox.SigmaOverlappedLine.value
        self.mask_threshold = self.SettingsBox.MaskThresholdSettingLine.value
        self.OverlappedImage = self.getOverlappedImage()
        self.imshow.set_extent(self.get_extent())
        self.imshow.set_data(self.OverlappedImage)
        super().on_settings_box()
