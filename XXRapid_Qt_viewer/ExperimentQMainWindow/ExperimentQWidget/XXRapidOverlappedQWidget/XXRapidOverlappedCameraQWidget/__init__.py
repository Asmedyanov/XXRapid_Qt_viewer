from .Settings import *
from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *
import numpy as np
from scipy.ndimage import binary_fill_holes, binary_hit_or_miss
from skimage import filters, morphology, segmentation
import skimage


class XXRapidOverlappedCameraQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = self.parent.current_key
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=Settings(self)
        )
        self.camera_data = self.parent.current_camera_data
        # self.MPLQWidget.ax.set(title=f'{self.settings_key}, mm')
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
        thresh = np.where(before_image > 1e-2 * np.max(before_image[np.nonzero(before_image)]) * self.mask_threshold, 1,
                          0)  # before_image > thresh_value
        fill = binary_fill_holes(thresh)#, structure=np.zeros((int(self.sigma_before*2), int(self.sigma_before*2))))
        # fill = binary_hit_or_miss(thresh)
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

    def save_report(self):
        fig_w, fig_h = self.MPLQWidget.figure.get_size_inches()
        new_w = 3.0  # inch
        new_h = fig_h * new_w / fig_w
        self.MPLQWidget.figure.set_size_inches(new_w, new_h)
        self.MPLQWidget.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')
        #self.imshow.imsave(f'{self.parent.report_path}/{self.settings_key}_im.png')
