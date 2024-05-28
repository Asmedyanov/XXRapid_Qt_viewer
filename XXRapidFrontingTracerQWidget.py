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
        self.XXRapidFrontingTracerSettingsQWidget.changed.connect(self.OnXXRapidFrontingTracerSettingsQWidget)
        self.QHBoxLayout.addWidget(self.XXRapidFrontingTracerSettingsQWidget)
        self.SettingsDict = self.XXRapidFrontingTracerSettingsQWidget.SettingsDict
        self.sigma_before = self.XXRapidFrontingTracerSettingsQWidget.SigmaBeforeLine.value
        self.sigma_shot = self.XXRapidFrontingTracerSettingsQWidget.SigmaShotLine.value
        self.sigma_overlapped = self.XXRapidFrontingTracerSettingsQWidget.SigmaOverlappedLine.value
        self.mask_threshold = self.XXRapidFrontingTracerSettingsQWidget.MaskThresholdSettingLine.value
        self.x_min = self.XXRapidFrontingTracerSettingsQWidget.XMinLine.value
        self.y_min = self.XXRapidFrontingTracerSettingsQWidget.YMinLine.value
        self.x_max = self.XXRapidFrontingTracerSettingsQWidget.XMaxLine.value
        self.y_max = self.XXRapidFrontingTracerSettingsQWidget.YMaxLine.value
        self.OverlappedImage = self.getOverlappedImage()
        self.imshow = self.MatplotlibSingeAxQWidget.ax.imshow(self.OverlappedImage)
        self.TraceLine, = self.MatplotlibSingeAxQWidget.ax.plot(
            [self.x_min, self.x_max],
            [self.y_min, self.y_max],
            '-or'
        )
        self.cid_1 = self.MatplotlibSingeAxQWidget.figure.canvas.mpl_connect('button_press_event',
                                                                             self.mouse_event_press)
        self.cid_2 = self.MatplotlibSingeAxQWidget.figure.canvas.mpl_connect('button_release_event',
                                                                             self.mouse_event_release)
        self.traced_image = self.get_traced_image()

    def mouse_event_press(self, event):
        self.x_1, self.y_1 = int(event.xdata), int(event.ydata)

    def mouse_event_release(self, event):
        x_2, y_2 = int(event.xdata), int(event.ydata)
        self.XXRapidFrontingTracerSettingsQWidget.SetLine(self.x_1, self.y_1, x_2, y_2)
        self.OnXXRapidFrontingTracerSettingsQWidget()

    def set_data(self, camera_data):
        self.camera_data = camera_data
        self.OnXXRapidFrontingTracerSettingsQWidget()

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

    # def set_geometry_settings(self, x_min, x_max, y_min, y_max):

    def OnXXRapidFrontingTracerSettingsQWidget(self):
        self.SettingsDict = self.XXRapidFrontingTracerSettingsQWidget.SettingsDict
        self.sigma_before = self.XXRapidFrontingTracerSettingsQWidget.SigmaBeforeLine.value
        self.sigma_shot = self.XXRapidFrontingTracerSettingsQWidget.SigmaShotLine.value
        self.sigma_overlapped = self.XXRapidFrontingTracerSettingsQWidget.SigmaOverlappedLine.value
        self.mask_threshold = self.XXRapidFrontingTracerSettingsQWidget.MaskThresholdSettingLine.value
        self.x_min = self.XXRapidFrontingTracerSettingsQWidget.XMinLine.value
        self.y_min = self.XXRapidFrontingTracerSettingsQWidget.YMinLine.value
        self.x_max = self.XXRapidFrontingTracerSettingsQWidget.XMaxLine.value
        self.y_max = self.XXRapidFrontingTracerSettingsQWidget.YMaxLine.value
        self.TraceLine.set_data(
            [self.x_min, self.x_max],
            [self.y_min, self.y_max],
        )
        self.OverlappedImage = self.getOverlappedImage()
        extent = [0,
                  self.OverlappedImage.shape[1],
                  self.OverlappedImage.shape[0],
                  0]
        self.imshow.set_extent(extent)
        self.imshow.set_data(self.OverlappedImage)
        self.MatplotlibSingeAxQWidget.changed.emit()
        self.traced_image = self.get_traced_image()
        self.chandeg.emit()

    def get_traced_image(self):
        min_x_index = int(min(self.x_min, self.x_max))
        max_x_index = int(max(self.x_min, self.x_max))
        min_y_index = int(min(self.y_min, self.y_max))
        max_y_index = int(max(self.y_min, self.y_max))
        traced_image = self.OverlappedImage[min_y_index:max_y_index, min_x_index:max_x_index]
        return traced_image
