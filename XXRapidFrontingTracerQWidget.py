from MatplotlibSingeAxQWidget import *
import numpy as np
from scipy.ndimage import gaussian_filter
from XXRapidFrontingTracerSettingsQWidget import *


class XXRapidFrontingTracerQWidget(QWidget):
    chandeg = pyqtSignal()

    def __init__(self, camera_data, settings_dict=None):
        super().__init__()
        self.camera_data = camera_data
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.MatplotlibSingeAxQWidget = MatplotlibSingeAxQWidget()
        self.QHBoxLayout.addWidget(self.MatplotlibSingeAxQWidget)
        self.XXRapidFrontingTracerSettingsQWidget = XXRapidFrontingTracerSettingsQWidget(settings_dict)
        self.QHBoxLayout.addWidget(self.XXRapidFrontingTracerSettingsQWidget)
        self.SettingsDict = self.XXRapidFrontingTracerSettingsQWidget.SettingsDict
        self.sigma_before = self.XXRapidFrontingTracerSettingsQWidget.SigmaBeforeLine.value
        self.sigma_shot = self.XXRapidFrontingTracerSettingsQWidget.SigmaShotLine.value
        self.sigma_overlapped = self.XXRapidFrontingTracerSettingsQWidget.SigmaOverlappedLine.value
        self.mask_threshold = self.XXRapidFrontingTracerSettingsQWidget.MaskThresholdSettingLine.value
        self.OverlappedImage = self.getOverlappedImage()
        self.imshow = self.MatplotlibSingeAxQWidget.ax.imshow(self.OverlappedImage)

    def set_data(self, camera_data):
        self.camera_data = camera_data

    def getOverlappedImage(self):
        before_image = gaussian_filter(self.camera_data['before'], sigma=self.sigma_before)
        shot_image = gaussian_filter(self.camera_data['shot'], sigma=self.sigma_shot)
        shadow_image = np.where(shot_image < before_image + before_image.std(),
                                shot_image,
                                before_image + before_image.std())
        mask = np.where(before_image > np.median(before_image) * self.mask_threshold, 1, 0)
        overlapped_image = np.where(before_image <= 0, 0,
                                    shadow_image / before_image) * mask
        overlapped_image = gaussian_filter(overlapped_image, sigma=self.sigma_overlapped)
        return overlapped_image
