from MatplotlibSingeAxQWidget import *

from XXRapidFrontingFrontSettingsQWidget import *
import numpy as np
from Approx_functions import f_free_style_full
from scipy.optimize import curve_fit


class XXRapidFrontingFrontQWidget(QWidget):
    chandeg = pyqtSignal()

    def __init__(self, parent, traced_image, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.parent = parent
        self.traced_image = traced_image
        self.QHBoxLayout = QHBoxLayout()
        self.setLayout(self.QHBoxLayout)
        self.MatplotlibSingeAxQWidget = MatplotlibSingeAxQWidget()
        self.QHBoxLayout.addWidget(self.MatplotlibSingeAxQWidget,stretch=1)
        self.XXRapidFrontingFrontSettingsQWidget = XXRapidFrontingFrontSettingsQWidget(settings_dict)
        self.XXRapidFrontingFrontSettingsQWidget.changed.connect(self.OnXXRapidFrontingFrontSettingsQWidget)
        self.SettingsDict = self.XXRapidFrontingFrontSettingsQWidget.SettingsDict
        self.QHBoxLayout.addWidget(self.XXRapidFrontingFrontSettingsQWidget)

        self.approximation_type = self.XXRapidFrontingFrontSettingsQWidget.ApproximationSettingLine.value
        self.threshold = self.XXRapidFrontingFrontSettingsQWidget.ThresholdSettingLine.value
        self.raw_point_x, self.raw_point_y = self.get_raw_points()
        try:
            self.x_approx, self.y_approx = self.get_approx_points()
        except:
            self.x_approx, self.y_approx = self.raw_point_x, self.raw_point_y
        self.raw_points_scatter, = self.MatplotlibSingeAxQWidget.ax.plot(
            self.raw_point_x, self.raw_point_y,
            '.r')
        self.approx_points_line, = self.MatplotlibSingeAxQWidget.ax.plot(
            self.x_approx, self.y_approx)

        self.imshow = self.MatplotlibSingeAxQWidget.ax.imshow(self.traced_image, extent=self.get_extent())

    def get_approx_points(self):
        x_approx = np.arange(self.traced_image.shape[1])
        if self.approximation_type == 'line':
            line_poly_coef = np.polyfit(self.raw_point_x, self.raw_point_y, 1)
            self.parent.a, self.parent.b = line_poly_coef
            line_poly_func = np.poly1d(line_poly_coef)
            y_approx = line_poly_func(x_approx)
        elif self.approximation_type == 'curve':
            bounds = ([-self.traced_image.shape[0], -self.traced_image.shape[1], 0, 0],
                      [0, 0, self.traced_image.shape[0], self.traced_image.shape[1]])

            def f_free_style_local(t, db_v, x0, x_p, dxt):
                return f_free_style_full(t, self.parent.a, self.parent.b, db_v, x0, x_p, dxt)

            popt, pcov = curve_fit(f_free_style_local, self.raw_point_x, self.raw_point_y, bounds=bounds)
            db_v, x0, x_p, dxt = popt
            y_approx = f_free_style_local(x_approx, db_v, x0, x_p, dxt)
        return x_approx, y_approx

    def get_raw_points(self):
        raw_point_x_list = []
        raw_point_y_list = []
        for i in range(self.traced_image.shape[1]):
            line = self.traced_image[:, i]
            try:
                index = np.argwhere(line > 1.0e-2 * self.threshold * line.max()).max()
                raw_point_x_list.append(i)
                raw_point_y_list.append(index)
            except:
                pass
        return np.array(raw_point_x_list), np.array(raw_point_y_list)

    def get_extent(self):
        extent = [0,
                  self.traced_image.shape[1],
                  self.traced_image.shape[0],
                  0]
        return extent

    def set_data(self, traced_image):
        self.traced_image = traced_image
        self.imshow.set_data(self.traced_image)

        self.OnXXRapidFrontingFrontSettingsQWidget()

    def OnXXRapidFrontingFrontSettingsQWidget(self):
        self.SettingsDict = self.XXRapidFrontingFrontSettingsQWidget.SettingsDict
        self.approximation_type = self.XXRapidFrontingFrontSettingsQWidget.ApproximationSettingLine.value
        self.threshold = self.XXRapidFrontingFrontSettingsQWidget.ThresholdSettingLine.value
        self.raw_point_x, self.raw_point_y = self.get_raw_points()
        try:
            self.x_approx, self.y_approx = self.get_approx_points()
        except:
            self.x_approx, self.y_approx = self.raw_point_x, self.raw_point_y
        self.raw_points_scatter.set_data(
            self.raw_point_x, self.raw_point_y)
        self.approx_points_line.set_data(self.x_approx, self.y_approx)

        self.imshow.set_data(self.traced_image)
        self.imshow.set_extent(self.get_extent())
        self.MatplotlibSingeAxQWidget.changed.emit()
        self.chandeg.emit()

    def get_front_dict(self):
        ret_dict = {
            'x': self.x_approx,
            'y': self.y_approx,
        }
        return ret_dict
