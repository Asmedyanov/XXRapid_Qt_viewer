import numpy as np

from Matplotlib_qtwidget import Matplotlib_qtwidget
import pandas as pd
import os


class J_comsol_widget(Matplotlib_qtwidget):
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
        df_edge_j = pd.read_csv('Jedge_Jav.csv')
        time_list = df_edge_j.columns[::2]
        width_list = df_edge_j.columns[1::2]
        self.min_len = len(df_edge_j)
        self.min_i = 0
        for i, name in enumerate(width_list):
            t_data = df_edge_j[time_list[i]].values
            jj_data = df_edge_j[name].values
            t_data = t_data[~np.isnan(t_data)]
            jj_data = jj_data[~np.isnan(jj_data)]

            if jj_data.size < self.min_len:
                self.min_len = jj_data.size
                self.min_i = i

            try:
                self.plot_dict[name].set_data(t_data * 1.0e9, jj_data)
            except:
                self.plot_dict[name], = self.ax.plot(t_data * 1.0e9, jj_data)
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
