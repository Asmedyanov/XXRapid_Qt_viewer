import numpy as np

from MatplotlibQWidget import MatplotlibQWidget
import pandas as pd
import os


class J_comsol_widget(MatplotlibQWidget):
    def __init__(self):
        super().__init__()
        self.ax = self.figure.add_subplot(111)
        self.ax.set(
            xlabel='t, ns',
            ylabel='J_max/J_avg',
            title='Skin effect'
        )
        self.plot_dict = dict()

    def set_data(self):
        # df_edge_j = pd.read_csv('Jedge_Jav.csv')
        df_edge_j = pd.read_csv('JmaxJav.csv')
        time_list = df_edge_j.columns[::2]
        width_list = df_edge_j.columns[1::2]
        self.min_len = len(df_edge_j)
        self.min_i = 0
        for i, name in enumerate(width_list):
            t_data = df_edge_j[time_list[i]].values
            jj_data = df_edge_j[name].values
            t_data = t_data[~np.isnan(t_data)]
            jj_data = jj_data[~np.isnan(jj_data)]
            df_to_smooth = pd.DataFrame({
                'time': t_data,
                'ratio': jj_data
            })

            t_conv = 50  # ns
            dt = np.mean(np.gradient(t_data))
            n_conv = int(t_conv * 1e-9 / dt)
            df_to_smooth = df_to_smooth.rolling(n_conv, min_periods=1).mean()
            a_conv = np.ones(n_conv) / float(n_conv)
            t_data = df_to_smooth['time'].values
            jj_data = df_to_smooth['ratio'].values
            deleta_0 = 130e-3  # mm
            w_data = float(name.split(' ')[0])
            # mu_0 = 1.3e-6
            # rho = 8.9e3  # kg/m^3
            # B = mu_0 * current_data / w_data / 1.0e-3 / 2
            delta_1 = 0.5 * 4.7e6  # B / np.sqrt(mu_0 * rho) * 1.0e3  # mm/s
            delta = deleta_0 + t_data * delta_1

            j_ratio_data = w_data / delta / 2 / np.tanh(w_data / delta / 2)

            if jj_data.size < self.min_len:
                self.min_len = jj_data.size
                self.min_i = i

            try:
                self.plot_dict[name].set_data(t_data * 1.0e9, jj_data)
                # self.plot_dict[f'{name}_analytic'].set_data(t_data * 1.0e9, jj_data)
            except:
                self.plot_dict[name], = self.ax.plot(t_data * 1.0e9, jj_data, '.')
                # self.plot_dict[f'{name}_analytic'], = self.ax.plot(t_data * 1.0e9, j_ratio_data)
        ratio_list = []
        time_value_list = []
        width_value_list = []
        possible_width = np.arange(len(width_list))
        for i in range(possible_width.size):
            possible_width[i] = float(width_list[i].split(' ')[0])
        finit_list = []
        for i, name in enumerate(width_list):
            t_data = df_edge_j[time_list[i]].values
            jj_data = df_edge_j[name].values
            t_data = t_data[~np.isnan(t_data)]
            jj_data = jj_data[~np.isnan(jj_data)]
            finit_list.append(pd.DataFrame({
                'time': t_data,
                'ratio': jj_data}
            ))
            for j in range(jj_data.size):
                width_value_list.append(possible_width[i])
                time_value_list.append(t_data[j])
                ratio_list.append(jj_data[j])
        ratio_array = np.array(ratio_list)
        # self.ratio_array = np.where(ratio_array < 1, 1, ratio_array)
        self.ratio_array = ratio_array
        self.width_array = np.array(width_value_list)
        self.time_array = np.array(time_value_list)
        self.possible_width = possible_width
        self.finit_list = finit_list

        self.ax.relim()
        self.figure.canvas.draw()
        self.changed.emit()
