from XXRapidOverlappedCameraSettingsQWidget import *
from MatplotlibSingeAxQWidget import *
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import correlate2d


class XXRapidOverlappedCameraQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, camera_data, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.camera_data = camera_data
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.MatplotlibSingeAxQWidget = MatplotlibSingeAxQWidget()
        self.MatplotlibSingeAxQWidget.ax.set(title='Overlapped image', xlabel='x,mm', ylabel='y,mm')
        self.QHBoxLayout.addWidget(self.MatplotlibSingeAxQWidget, stretch=1)
        self.XXRapidOverlappedCameraSettingsQWidget = XXRapidOverlappedCameraSettingsQWidget(settings_dict)
        self.SettingsDict = self.XXRapidOverlappedCameraSettingsQWidget.SettingsDict
        self.QHBoxLayout.addWidget(self.XXRapidOverlappedCameraSettingsQWidget)

        self.XXRapidOverlappedCameraSettingsQWidget.changed.connect(self.OnXXRapidOverlappedCameraSettingsQWidget)

        self.dx = 1.0 / self.XXRapidOverlappedCameraSettingsQWidget.ScaleSettingLine.value
        self.sigma_before = self.XXRapidOverlappedCameraSettingsQWidget.SigmaBeforeLine.value
        self.sigma_shot = self.XXRapidOverlappedCameraSettingsQWidget.SigmaShotLine.value
        self.sigma_overlapped = self.XXRapidOverlappedCameraSettingsQWidget.SigmaOverlappedLine.value
        self.mask_threshold = self.XXRapidOverlappedCameraSettingsQWidget.MaskThresholdSettingLine.value
        self.OverlappedImage = self.getOverlappedImage()

        self.imshow = self.MatplotlibSingeAxQWidget.ax.imshow(self.OverlappedImage, extent=self.get_extent())

    def get_extent(self):
        extent = [-self.OverlappedImage.shape[1] * self.dx // 2,
                  self.OverlappedImage.shape[1] * self.dx // 2,
                  self.OverlappedImage.shape[0] * self.dx // 2,
                  -self.OverlappedImage.shape[0] * self.dx // 2]
        return extent

    def getOverlappedImage(self):
        before_image = gaussian_filter(self.camera_data['before'],
                                       sigma=self.sigma_before)
        # before_image = before_image / before_image.max()
        shot_image = gaussian_filter(self.camera_data['shot'],
                                     sigma=self.sigma_shot)
        # shot_image = shot_image / shot_image.max()
        shadow_image = np.where(shot_image < before_image,  # + before_image.std(),
                                shot_image,
                                before_image)  # + before_image.std())
        mask = np.where(before_image > np.median(before_image[np.nonzero(before_image)]) * self.mask_threshold, 1, 0)
        overlapped_image = np.where(before_image <= 0, 0,
                                          shadow_image / before_image) * mask
        overlapped_image = gaussian_filter(overlapped_image, sigma=self.sigma_overlapped)
        return overlapped_image

    def OnXXRapidOverlappedCameraSettingsQWidget(self):
        self.SettingsDict = self.XXRapidOverlappedCameraSettingsQWidget.SettingsDict
        self.dx = 1.0 / self.XXRapidOverlappedCameraSettingsQWidget.ScaleSettingLine.value
        self.sigma_before = self.XXRapidOverlappedCameraSettingsQWidget.SigmaBeforeLine.value
        self.sigma_shot = self.XXRapidOverlappedCameraSettingsQWidget.SigmaShotLine.value
        self.sigma_overlapped = self.XXRapidOverlappedCameraSettingsQWidget.SigmaOverlappedLine.value
        self.mask_threshold = self.XXRapidOverlappedCameraSettingsQWidget.MaskThresholdSettingLine.value
        self.OverlappedImage = self.getOverlappedImage()
        self.imshow.set_extent(self.get_extent())
        self.imshow.set_data(self.OverlappedImage)
        self.MatplotlibSingeAxQWidget.changed.emit()
        self.changed.emit()
