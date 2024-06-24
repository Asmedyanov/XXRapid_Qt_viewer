from .CAIExplosionCurrentQTabWidget import *
from .ExplosionCurrentDensityQWidget import *
from .CAIResultQTabWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class CAIQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'CAI')
        self.CurrentQWidget = self.parent.WaveformQTabWidget.WaveformProcessingQTabWidget.WaveformPhysicalValuesQWidget.CurrentQWidget
        self.current_df = self.CurrentQWidget.current_df_to_plot
        self.current_function = self.CurrentQWidget.current_function
        self.TOF_data_dict = self.parent.XXRapidTOFQTabWidget.TOFResultQTabWidget.velocity_dict
        self.explosion_current_dict = self.get_explosion_current_dict()
        try:
            self.CAIExplosionCurrentQTabWidget = CAIExplosionCurrentQTabWidget(self)
            self.addTab(self.CAIExplosionCurrentQTabWidget, self.CAIExplosionCurrentQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.ExplosionCurrentDensityQWidget = ExplosionCurrentDensityQWidget(self)
            self.addTab(self.ExplosionCurrentDensityQWidget,
                        self.ExplosionCurrentDensityQWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.CAIResultQTabWidget = CAIResultQTabWidget(self)
            self.addTab(self.CAIResultQTabWidget, 'CAI')
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
