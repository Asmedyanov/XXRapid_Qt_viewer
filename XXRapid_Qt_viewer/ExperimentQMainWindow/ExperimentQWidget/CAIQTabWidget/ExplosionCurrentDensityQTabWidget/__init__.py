from SettingsQWidgets.ChildQTabWidget import *


class ExplosionCurrentDensityQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Explosion_Current_Density')
        self.ExplosionCurrentQTabWidget = self.parent.CAIExplosionCurrentQTabWidget
        self.ExplosionCurrentQTabWidget.changed.connect(self.refresh)
        self.FoilQWidget = self.parent.FoilQWidget
        self.FoilQWidget.changed.connect(self.refresh)
        self.explosion_current_density_dict = self.get_explosion_current_density_dict()
        self.Graphics_dict = dict()
        for my_key, my_df in self.explosion_current_density_dict.items():
            self.current_key = my_key
            self.current_df = my_df
            try:
                self.Graphics_dict[my_key] = Graphics(self)
                self.addTab(self.Graphics_dict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def get_explosion_current_density_dict(self):
        explosion_current_density_dict = dict()
        explosion_current_dict = self.ExplosionCurrentQTabWidget.explosion_current_dict
        for my_key, my_df in explosion_current_dict.items():
            df = my_df[['x', 'width', 'onset_time']].copy()
            df['current_density'] = my_df['current'] / self.FoilQWidget.cross_section_function(my_df['x'])
            explosion_current_density_dict[my_key] = df
        return explosion_current_dict

    def refresh(self):
        self.explosion_current_density_dict = self.get_explosion_current_density_dict()
        for my_key, my_df in self.explosion_current_density_dict.values():
            self.current_df = my_df
            self.current_key = my_key
            try:
                self.Graphics_dict[my_key].refresh()
            except Exception as ex:
                print(ex)
        self.changed.emit()
