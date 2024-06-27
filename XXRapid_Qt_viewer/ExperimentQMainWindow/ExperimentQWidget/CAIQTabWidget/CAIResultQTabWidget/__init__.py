import os

import pandas as pd
from PyQt5.QtWidgets import QTabWidget
import numpy as np
from .Graphics import *


class CAIResultQTabWidget(QTabWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Experimental_CAI_result'
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        super().__init__()
        self.current_df = self.parent.current_df.copy()
        self.full_cai_df = self.get_full_cai_df()
        self.current_density_dict = self.parent.ExplosionCurrentDensityQWidget.current_density_dict
        self.cai_dict = self.get_cai_dict()
        self.GraphicsDict = dict()
        try:
            self.comsol_dict = self.parent.parent.ComsolSimulationQTabWidget.ComsolCurrentQTabWidget.CAI_dict
        except Exception as ex:
            print(ex)
        for my_key, my_df in self.cai_dict.items():
            self.current_df = my_df
            self.current_key = my_key
            try:
                self.current_comsol = self.comsol_dict[my_key]
            except Exception as ex:
                print(ex)
            try:
                self.GraphicsDict[my_key] = Graphics(self)
                self.addTab(self.GraphicsDict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def update(self):
        self.current_df = self.parent.current_df.copy()
        self.full_cai_df = self.get_full_cai_df()
        self.current_density_dict = self.parent.ExplosionCurrentDensityQWidget.current_density_dict
        self.cai_dict = self.get_cai_dict()
        for my_key, my_df in self.cai_dict.items():
            self.GraphicsDict[my_key].set_data(my_df)

    def get_full_cai_df(self):
        i2dt = self.current_df['Units'].values ** 2 * np.gradient(self.current_df['time'].values)
        full_cai_array = i2dt.copy()
        for i in range(1, full_cai_array.size):
            full_cai_array[i] += full_cai_array[i - 1]
        full_cai_df = pd.DataFrame({
            'time': self.current_df['time'].values,
            'cai': full_cai_array
        })
        return full_cai_df

    def cai_function(self, time):
        ret = np.interp(time, self.full_cai_df['time'], self.full_cai_df['cai'])
        return ret

    def get_cai_dict(self):
        cai_dict = dict()
        for my_key, my_df in self.current_density_dict.items():
            cai_df = pd.DataFrame({
                'width': my_df['width'],
                'current_density': my_df['current_density'],
                'onset_time': my_df['onset_time'],
                'cai': self.cai_function(my_df['onset_time'] * 1e-9) / (my_df['cross_section'] * 1e4) ** 2
            })
            cai_dict[my_key] = cai_df

        return cai_dict

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for graphics in self.GraphicsDict.values():
            try:
                graphics.save_report()
            except Exception as ex:
                print(ex)
