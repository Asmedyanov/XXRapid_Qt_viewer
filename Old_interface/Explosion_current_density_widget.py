from Quart_plots_widget import Quart_plots_widget
import pandas as pd


class Explosion_current_density_widget(Quart_plots_widget):
    def __init__(self):
        super().__init__()
        self.explosion_current_density_dict = dict()
        for i in range(4):
            key = f'Quart_{i + 1}'
            self.ax[i].set(xlabel='x, mm', ylabel='j, A/um^2')
            self.plot_by_quarts[key], = self.ax[i].plot([0, 0], [0, 0])

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

    def set_data(self, explosion_current_dict, geometry_dict):
        self.waist = geometry_dict['Waist']
        self.h_foil = geometry_dict['Thickness']
        self.l_foil = geometry_dict['Length']
        self.w_foil = geometry_dict['Width']
        for i in range(4):
            key = f'Quart_{i + 1}'
            x_data = explosion_current_dict[key]['x'].values  # m
            S_data = self.cross_section(x_data * 1.0e3)  # mm^2
            i_data = explosion_current_dict[key]['current'].values  # A
            j_data = i_data / S_data  # A/mm^2
            self.explosion_current_density_dict[key] = pd.DataFrame({
                'x': x_data,
                'j': j_data
            })

            self.plot_by_quarts[key].set_data(x_data * 1.0e3, j_data * 1.0e-6)
            self.ax[i].relim()
            self.ax[i].autoscale_view()
        self.figure.canvas.draw()
        self.changed.emit()
