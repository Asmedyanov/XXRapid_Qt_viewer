import pandas as pd
from PyQt5.QtWidgets import QTabWidget
from .CAIExplosionCurrentQTabWidget import *
from .ExplosionCurrentDensityQWidget import *


class CAIQTabWidget(QTabWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.current_df = self.parent.WaveformProcessingWidget.WaveformPhysicalValuesQWidget.WaveformCurrentQWidget.current_df_to_plot
        self.current_function = self.parent.WaveformProcessingWidget.WaveformPhysicalValuesQWidget.WaveformPowerQWidget.current_function
        self.TOF_data_dict = self.parent.XXRapidTOFQTabWidget.XXRapidTOFVelocityQTabWidget.get_velocity_dict()
        self.explosion_current_dict = self.get_explosion_current_dict()
        try:
            self.CAIExplosionCurrentQTabWidget = CAIExplosionCurrentQTabWidget(self)
            self.addTab(self.CAIExplosionCurrentQTabWidget, 'Explosion_current')
        except Exception as ex:
            print(ex)
        try:
            self.ExplosionCurrentDensityQWidget = ExplosionCurrentDensityQWidget(self)
            self.addTab(self.ExplosionCurrentDensityQWidget,
                        'Explosion current density')
        except Exception as ex:
            print(ex)

    def get_explosion_current_dict(self):
        explosion_current_dict = dict()
        for my_key, my_df in self.TOF_data_dict.items():
            explosion_current_df = pd.DataFrame()
            explosion_current_df['onset_time'] = my_df['onset_time']
            explosion_current_df['width'] = my_df['width']
            explosion_current_df['current'] = self.current_function(my_df['onset_time'] * 1e-9)
            # explosion_current_df['density'] = explosion_current_df['current'] / explosion_current_df['width'] / 15e-3
            explosion_current_dict[my_key] = explosion_current_df

        return explosion_current_dict
