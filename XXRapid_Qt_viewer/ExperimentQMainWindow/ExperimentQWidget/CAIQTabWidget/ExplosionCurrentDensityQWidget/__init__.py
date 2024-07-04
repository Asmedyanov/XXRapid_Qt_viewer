import pandas as pd

from .Settings import *
from SettingsQWidgets import SettingsQWidget2
from .ExplosionCurrentDensityQTabWidget import *


class ExplosionCurrentDensityQWidget(SettingsQWidget2):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Explosion_current_density'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.FoilQWidget = self.parent.FoilQWidget
        settings = Settings(self)
        self.thickness = settings.ThicknessSettingLine.value
        self.current_density_dict = self.get_current_density_dict()

        Explosion_current_density_tab = ExplosionCurrentDensityQTabWidget(self)
        super().__init__(main_widget=Explosion_current_density_tab, settings_box=settings)

    def on_settings_box(self):
        self.thickness = self.SettingsBox.ThicknessSettingLine.value
        self.current_density_dict = self.get_current_density_dict()
        self.MainWidget.refresh()
        super().on_settings_box()

    def get_current_density_dict(self):
        current_density_dict = dict()
        for my_key, my_df in self.parent.explosion_current_dict.items():
            current_density_df = pd.DataFrame(
                {
                    'width': my_df['width'],  # mm
                    'onset_time': my_df['onset_time'],
                    'cross_section': my_df['width'] * self.thickness * 1e-3 * 1e-6,  # m^2
                    'current_density': my_df['current'] / (my_df['width'] * self.thickness * 1e-3 * 1e-6)  # A/m^2
                }
            )
            current_density_dict[my_key] = current_density_df

        return current_density_dict

    def save_report(self):
        os.makedirs(self.report_path,exist_ok=True)
        try:
            self.MainWidget.save_report()
        except Exception as ex:
            print(ex)
