from SettingsQWidgets.ChildQTabWidget import *
from .Graphics import *


class CAIExplosionCurrentQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Explosion_current')
        self.explosion_current_dict = self.parent.explosion_current_dict
        self.current_plot_dict = dict()
        for my_key, my_df in self.explosion_current_dict.items():
            self.current_df = my_df
            try:
                self.current_plot_dict[my_key] = Graphics(self)
                self.addTab(self.current_plot_dict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def refresh(self):
        self.explosion_current_dict = self.parent.explosion_current_dict
        for my_key, my_df in self.explosion_current_dict.items():
            self.current_plot_dict[my_key].set_data(my_df)
