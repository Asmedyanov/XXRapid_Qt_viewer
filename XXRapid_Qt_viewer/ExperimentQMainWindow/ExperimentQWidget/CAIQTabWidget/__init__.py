from .CAIExplosionCurrentQTabWidget import *
from .ExplosionCurrentDensityQTabWidget import *
from .CAIResultQTabWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class CAIQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'CAI')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.CurrentQWidget = self.parent.WaveformQTabWidget.WaveformProcessingQTabWidget.WaveformPhysicalValuesQWidget.CurrentQWidget
        self.FoilQWidget = self.parent.FoilQWidget
        self.current_df = self.CurrentQWidget.current_df_to_plot
        self.current_function = self.CurrentQWidget.current_function
        self.TOF_data_dict = self.parent.XXRapidTOFQTabWidget.TOFResultQTabWidget.velocity_smoothed_dict
        self.explosion_current_dict = self.get_explosion_current_dict()
        try:
            self.CAIExplosionCurrentQTabWidget = CAIExplosionCurrentQTabWidget(self)
            self.addTab(self.CAIExplosionCurrentQTabWidget, self.CAIExplosionCurrentQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.ExplosionCurrentDensityQWidget = ExplosionCurrentDensityQTabWidget(self)
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
            explosion_current_df = my_df[['x','width','onset_time']].copy()
            explosion_current_df['current'] = self.current_function(my_df['onset_time'] * 1e-9)
            explosion_current_dict[my_key] = explosion_current_df

        return explosion_current_dict

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        try:
            self.CAIExplosionCurrentQTabWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.ExplosionCurrentDensityQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.CAIResultQTabWidget.save_report()
        except Exception as ex:
            print(ex)

    def save_origin_pro(self, op):
        try:
            self.CAIResultQTabWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)


