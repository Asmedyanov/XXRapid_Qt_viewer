import pandas as pd

from SettingsQWidgets import *
from .ExplosionCurrentDensityQTabWidget import *


class ExplosionCurrentDensityQWidget(SettingsQWidget2):
    def __init__(self, parent):
        self.parent = parent
        self.current_density_dict = self.get_current_density_dict()
        Explosion_current_density_tab = ExplosionCurrentDensityQTabWidget(self)
        super().__init__(main_widget=Explosion_current_density_tab, settings_box=SettingsBoxQWidget())

    def get_current_density_dict(self):
        current_density_dict = dict()
        for my_key, my_df in self.parent.explosion_current_dict.items():
            current_density_df = pd.DataFrame(
                {
                    'width': my_df['width'],  # mm
                    'onset_time': my_df['onset_time'],
                    'cross_section': my_df['width'] * 1e-3 * 15e-6,  # m^2
                    'current_density': my_df['current'] / (my_df['width'] * 1e-3 * 15e-6)  # A/m^2
                }
            )
            current_density_dict[my_key] = current_density_df

        return current_density_dict
