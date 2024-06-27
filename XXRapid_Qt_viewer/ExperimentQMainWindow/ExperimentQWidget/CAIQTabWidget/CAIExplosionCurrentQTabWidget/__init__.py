from SettingsQWidgets.ChildQTabWidget import *
from .Graphics import *


class CAIExplosionCurrentQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Explosion_current')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.explosion_current_dict = self.parent.explosion_current_dict
        self.GraphicsDict = dict()
        for my_key, my_df in self.explosion_current_dict.items():
            self.current_df = my_df
            self.current_key = my_key
            try:
                self.GraphicsDict[my_key] = Graphics(self)
                self.addTab(self.GraphicsDict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def refresh(self):
        self.explosion_current_dict = self.parent.explosion_current_dict
        for my_key, my_df in self.explosion_current_dict.items():
            self.GraphicsDict[my_key].set_data(my_df)

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for graphics in self.GraphicsDict.values():
            try:
                graphics.save_report()
            except Exception as ex:
                print(ex)
