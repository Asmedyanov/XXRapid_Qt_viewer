from Quart_plots_widget import Quart_plots_widget
import numpy as np
import pandas as pd
from scipy.interpolate import interp2d
from J_ratio_function import *


class Action_integral_widget(Quart_plots_widget):
    def __init__(self):
        super().__init__()
        self.explosion_h_dict = dict()
        for i in range(4):
            key = f'Quart_{i + 1}'
            # self.ax[i].set(xlabel='j,$10^8 A/cm^2$', ylabel='h, $10^9 A^2*s/cm^4$')
            self.ax[i].set(xlabel='x, mm', ylabel='j,$10^8 A/cm^2$')
            self.plot_by_quarts[key], = self.ax[i].plot([0, 0], [0, 0], 'o')

    def cross_section(self, z):
        """
        The function to calculate the foil cross-section in direction of the current z
        :param z:
        distance from the butterfly waist in direction of current in mm
        :return:
        cross-section of the foil in square mm
        """
        s = 0.5 * self.waist + (self.w_foil - self.waist) * z / self.l_foil
        return 2 * s * self.h_foil

    def set_data(self, explosion_time_dict,
                 df_current,
                 geometry_dict,
                 ratio_df_list,
                 possible_width
                 ):
        self.waist = geometry_dict['Waist']
        self.h_foil = geometry_dict['Thickness']
        self.l_foil = geometry_dict['Length']
        self.w_foil = geometry_dict['Width']

        def f_current(t):
            ret = np.interp(t, df_current['time'], df_current['value'])
            return ret

        def f_integral(t):
            ret = np.interp(t, df_current['time'], df_current['integral'])
            return ret

        def f_ratio(w, t):
            deleta_0 = 3e-3  # mm
            mu_0 = 1.3e-6
            rho = 8.9e3  # kg/m^3
            B = mu_0 * f_current(t) / w / 1.0e-3 / 2
            delta_1 = B / np.sqrt(mu_0 * rho) * 1.0e3  # mm/s
            delta = deleta_0 + t * delta_1
            ratio = w / delta / 2 / np.tanh(w / delta / 2)
            return ratio

        f_ratio_vect = np.vectorize(f_ratio, excluded='w')

        def j_ratio_local(t, w):
            return j_ratio(t, w, h=self.h_foil, t_0=df_current['time'].max())

        j_ratio_local_vect = np.vectorize(j_ratio_local)

        for i in range(4):
            key = f'Quart_{i + 1}'
            t_data = explosion_time_dict[key]['onset_time'].values
            x_data = explosion_time_dict[key]['x'].values
            current_data = f_current(t_data)
            integral_data = f_integral(t_data)
            S_data = self.cross_section(x_data * 1.0e3)
            w_data = S_data / self.h_foil
            deleta_0 = 3e-3  # mm
            mu_0 = 1.3e-6
            rho = 8.9e3  # kg/m^3
            B = mu_0 * current_data / w_data / 1.0e-3 / 2
            delta_1 = B / np.sqrt(mu_0 * rho)*1.0e3  # mm/s
            delta = deleta_0 + t_data * delta_1

            j_ratio_data = w_data / delta / 2 / np.tanh(w_data / delta / 2)

            j_data = current_data / S_data * j_ratio_data
            h_data = integral_data / S_data ** 2 * j_ratio_data ** 2
            '''j_coef_data = np.zeros(t_data.size)
            h_coef_data = np.zeros(t_data.size)
            ratio_data = np.zeros(t_data.size)
            for j in range(t_data.size):
                ratio = f_ratio(w_data[j], t_data[j])
                ratio_data[j] = ratio
                j_coef_data[j] = j_data[j] * ratio
                index_to_sum = np.argwhere(((df_current['time'].values > 0) & (df_current['time'].values < t_data[j])))[
                               :, 0]
                ratio_list = []
                for k in index_to_sum:
                    ratio_list.append(f_ratio(w_data[j], df_current['time'].values[k]))

                # array_to_sum = f_ratio_vect(w_data[j], df_current['time'].values[index_to_sum])
                array_to_sum = np.array(ratio_list)
                # array_to_sum = np.where(array_to_sum < 1, 1, array_to_sum)
                array_to_sum = np.gradient(df_current['time'].values[
                                               index_to_sum]) * df_current['value2'].values[
                                   index_to_sum] * array_to_sum ** 2
                h_coef_data[j] = np.sum(array_to_sum) / S_data[j] ** 2
            h_data = integral_data / np.square(S_data)'''

            self.explosion_h_dict[key] = pd.DataFrame(
                {
                    'x': x_data,  # m
                    'current': current_data,  # A
                    'j': j_data,  # A/mm^2
                    # 'h': h_data
                }

            )
            self.plot_by_quarts[key].set_data(x_data * 1.0e3, j_data * 1.0e-6)
            # self.plot_by_quarts[key].set_data(j_data * 1.0e-6, h_data * 1.0e-5)
            self.ax[i].relim()
            self.ax[i].autoscale_view()
        self.figure.canvas.draw()
        self.changed.emit()
