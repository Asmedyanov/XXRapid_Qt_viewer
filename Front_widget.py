from Matplotlib_qtwidget import Matplotlib_qtwidget
import numpy as np
from PyQt5.QtCore import pyqtSignal
from scipy.optimize import curve_fit
from Approx_functions import *


class Front_widget(Matplotlib_qtwidget):
    line_signal = pyqtSignal()

    def __init__(self, parent, approx='my'):
        super().__init__()
        self.parent = parent
        self.approx = approx
        # Create a Matplotlib figure and axis
        gs = self.figure.add_gridspec(ncols=3)
        self.ax = gs.subplots()
        for ax in self.ax:
            ax.grid(linestyle='dotted')
        self.ax[0].set_title('Window and red points')
        self.ax[1].set_title('Profiles and level')
        self.ax[2].set_title('Approximation overlap')
        # Create a canvas to embed the Matplotlib plot
        self.intensity_level = 0.5

        self.cid_1 = self.figure.canvas.mpl_connect('button_press_event', self.mouse_event_press)

    def mouse_event_press(self, event):
        if event.inaxes.get_title() == 'Window and red points':
            self.On_window_and_points_click(event)
        if event.inaxes.get_title() == 'Profiles and level':
            self.On_profiles_and_level_click(event)

    def On_profiles_and_level_click(self, event):
        self.intensity_level = event.ydata
        self.intensity_level_line.set_data([0, self.image_hight], [self.intensity_level, self.intensity_level])
        self.update_red_points()
        self.update_approx()
        self.figure.canvas.draw()
        self.changed.emit()

    def On_window_and_points_click(self, event):
        self.profile_x = int(event.xdata)
        self.Front_line.set_data([self.profile_x, self.profile_x], [0, self.image_hight])
        intensity_profile = self.image_array[:, self.profile_x]
        intensity_gradient = np.gradient(intensity_profile)
        intensity_gradient = np.where(intensity_gradient < 0, -intensity_gradient, 0)
        intensity_gradient /= intensity_gradient.max()
        self.Intensity_line.set_data(np.arange(intensity_profile.size), intensity_profile)
        self.Intensity_gradient_line.set_data(np.arange(intensity_gradient.size), intensity_gradient)


        self.figure.canvas.draw()

    def set_data(self, array_1, base_dict=None):
        self.base_dict = base_dict
        self.image_array = array_1
        try:
            print(f'shape before{self.image_plot_1.get_array().shape()}')
            self.image_plot_1.set_data(self.image_array)
            print(self.image_plot_1.get_array().shape())

        except:
            self.image_plot_1 = self.ax[0].imshow(self.image_array, cmap='gray')
        try:
            print(f'shape before{self.image_plot_2.get_array().shape()}')
            self.image_plot_2.set_data(self.image_array)
            print(self.image_plot_2.get_array().shape())
        except:
            self.image_plot_2 = self.ax[2].imshow(self.image_array, cmap='gray')
        self.image_width = self.image_array.shape[1]
        self.image_hight = self.image_array.shape[0]
        self.profile_x = self.image_width // 8
        if base_dict is None:
            self.intensity_level = 0.5
        else:
            self.intensity_level = float(base_dict['intensity_level'])

        intensity_profile = self.image_array[:, self.profile_x]
        intensity_gradient = np.gradient(intensity_profile)
        intensity_gradient = np.where(intensity_gradient < 0, -intensity_gradient, 0)
        intensity_gradient /= intensity_gradient.max()
        try:
            self.Front_line.set_data([self.profile_x, self.profile_x], [0, self.image_hight])

        except:
            self.Front_line, = self.ax[0].plot([self.profile_x, self.profile_x], [0, self.image_hight], 'o-r')
        try:
            self.Intensity_line.set_data(np.arange(intensity_profile.size), intensity_profile)
            self.Intensity_gradient_line.set_data(np.arange(intensity_gradient.size), intensity_gradient)
        except:
            self.Intensity_line, = self.ax[1].plot(np.arange(intensity_profile.size), intensity_profile)
            self.Intensity_gradient_line, = self.ax[1].plot(np.arange(intensity_gradient.size), intensity_gradient)
            pass
        try:
            self.intensity_level_line.set_data([0, self.image_hight], [self.intensity_level, self.intensity_level])

        except:
            self.intensity_level_line, = self.ax[1].plot([0, self.image_hight],
                                                         [self.intensity_level, self.intensity_level], 'o-r')
        self.update_red_points()

        self.update_approx()
        self.ax[1].relim()
        self.ax[1].autoscale_view()
        self.figure.canvas.draw()

    def update_red_points(self):
        red_points_x = []
        red_points_y = []
        for i in range(self.image_width):
            white_points = np.argwhere(self.image_array[:, i] > self.intensity_level)[:, 0]
            if white_points.size > 5:
                red_points_x.append(i)
                red_points_y.append(white_points[-1])
        line_poly_coef = np.polyfit(red_points_x, red_points_y, 1)
        line_poly_func = np.poly1d(line_poly_coef)
        red_points_x_filtered = []
        red_points_y_filtered = []
        for i in range(len(red_points_x)):
            if np.abs(line_poly_func(red_points_x[i]) - red_points_y[i]) < 30:
                red_points_x_filtered.append(red_points_x[i])
                red_points_y_filtered.append(red_points_y[i])
        self.red_points_x = np.array(red_points_x_filtered)
        self.red_points_y = np.array(red_points_y_filtered)
        try:
            self.red_points_plot.set_data(self.red_points_x, self.red_points_y)
        except:
            self.red_points_plot, = self.ax[0].plot(self.red_points_x, self.red_points_y, 'or')

    def update_approx(self):
        x_data = self.red_points_x
        y_data = self.red_points_y
        x_approx = np.arange(self.red_points_x[-1])
        if self.approx == 'line':
            line_poly_coef = np.polyfit(x_data, y_data, 1)
            self.parent.a, self.parent.b = line_poly_coef
            line_poly_func = np.poly1d(line_poly_coef)
            poly_y_data = line_poly_func(x_approx)
        if self.approx == 'my':
            bounds = ([-self.image_hight, -self.image_width, 0, 0],
                      [0, 0, self.image_hight, self.image_width])

            def f_free_style_local(t, db_v, x0, x_p, dxt):
                return f_free_style_full(t, self.parent.a, self.parent.b, db_v, x0, x_p, dxt)

            popt, pcov = curve_fit(f_free_style_local, x_data, y_data, bounds=bounds)
            self.db_v, self.x0, self.x_p, self.dxt = popt
            poly_y_data = f_free_style_local(x_approx, self.db_v, self.x0, self.x_p, self.dxt)
        try:
            self.approx_plot.set_data(x_approx, poly_y_data)
        except:
            self.approx_plot, = self.ax[2].plot(x_approx, poly_y_data)

    def get_data_dict(self):
        ret = None
        try:
            ret = {
                'intensity_level': self.intensity_level,
            }
            if self.approx == 'line':
                ret['a'] = self.parent.a
                ret['b'] = self.parent.b
            if self.approx == 'my':
                ret['db_v'] = self.db_v
                ret['x0'] = self.x0
                ret['x_p'] = self.x_p
                ret['dxt'] = self.dxt
        except:
            pass
        return ret
