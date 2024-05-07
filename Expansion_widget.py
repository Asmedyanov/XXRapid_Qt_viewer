from Quart_plots_widget import Quart_plots_widget
import numpy as np
import Approx_functions


class Expansion_widget(Quart_plots_widget):
    def __init__(self):
        super().__init__()

        t = np.arange(0, 2 * np.pi, 0.1)
        for i in [1, 2, 3, 4]:
            self.ax[i - 1].set(xlabel=f'x, mm', ylabel=f'y, mm')
            for j in range(8):
                self.plot_by_quarts[f'Quart_{i}'].append(
                    self.ax[i - 1].plot((j + 1) * np.cos(t), (j + 1) * np.sin(t))[0]
                )

    def set_data(self, base_dict, dx):
        self.dx = dx
        self.base_dict = base_dict
        self.Expansion_by_quarts_dict = dict()
        for i in [1, 2, 3, 4]:
            key_i = f'Quart_{i}'
            Expansion_by_quart = []
            for j in [1, 2, 3, 4]:
                key_j = f'Frame_{j}'
                x_1 = int(self.base_dict[key_j][key_i][f'Tracer']['x_1'])
                x_2 = int(self.base_dict[key_j][key_i][f'Tracer']['x_2'])
                x_data = np.arange(max([x_1, x_2]))
                a = float(self.base_dict[key_j][key_i]['fronts'][f'Front_1']['a'])
                b = float(self.base_dict[key_j][key_i]['fronts'][f'Front_1']['b'])
                y_data_before = a * x_data + b
                for k in [2, 3]:
                    db_v = float(self.base_dict[key_j][key_i]['fronts'][f'Front_{k}']['db_v'])
                    dxt = float(self.base_dict[key_j][key_i]['fronts'][f'Front_{k}']['dxt'])
                    x0 = float(self.base_dict[key_j][key_i]['fronts'][f'Front_{k}']['x0'])
                    x_p = float(self.base_dict[key_j][key_i]['fronts'][f'Front_{k}']['x_p'])
                    y_data_shot = Approx_functions.f_free_style_full(x_data, a, b, db_v, x0, x_p, dxt)
                    expansion = np.abs(y_data_before - y_data_shot) * dx
                    Expansion_by_quart.append({
                        'x': x_data * dx,
                        'expansion': expansion})
            for j in range(len(Expansion_by_quart)):
                self.plot_by_quarts[key_i][j].set_data(Expansion_by_quart[j]['x'], Expansion_by_quart[j]['expansion'])
            self.ax[i - 1].relim()
            self.ax[i - 1].autoscale_view()
            self.Expansion_by_quarts_dict[key_i] = Expansion_by_quart
        self.figure.canvas.draw()
        self.Resort_Expansion()
        self.changed.emit()

    def Resort_Expansion(self):
        self.update_max_cross_section()
        expansion_by_cross_section_dict = dict()
        for my_key, Expansion_by_quart in self.Expansion_by_quarts_dict.items():
            expansion_by_cross_section_array = np.zeros((self.max_cross_section_dict[my_key], 8))
            for i in range(self.max_cross_section_dict[my_key]):
                for j in range(8):
                    expansion_by_cross_section_array[i, j] = Expansion_by_quart[j]['expansion'][i]
            expansion_by_cross_section_array = np.sort(expansion_by_cross_section_array, axis=1)
            expansion_by_cross_section_dict[my_key] = expansion_by_cross_section_array
        self.expansion_by_cross_section_dict = expansion_by_cross_section_dict

    def update_max_cross_section(self):
        max_cross_section_dict = dict()
        for my_key, Expansion_by_quart in self.Expansion_by_quarts_dict.items():
            x_max = Expansion_by_quart[0]['x'].size
            for i in range(8):
                x_max_temp = Expansion_by_quart[i]['x'].size
                if x_max_temp < x_max:
                    x_max = x_max_temp
            max_cross_section_dict[my_key] = x_max
        self.max_cross_section_dict = max_cross_section_dict
