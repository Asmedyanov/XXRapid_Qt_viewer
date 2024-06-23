from SettingsQWidgets.ChildQTabWidget import *
from .FrontQWidget import *


class FrontsQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Fronts')
        self.n_fronts = 3
        self.FrontQWidgetDict = dict()
        self.TracerQWidget = self.parent.TracerQWidget
        self.TracerQWidget.changed.connect(self.refresh)
        self.traced_image = self.TracerQWidget.traced_image
        self.expansion_dict = self.parent.expansion_dict
        for i in range(self.n_fronts):
            self.current_key = f'Front_{i}'
            try:
                self.FrontQWidgetDict[self.current_key] = FrontQWidget(self)
                self.addTab(self.FrontQWidgetDict[self.current_key], self.current_key)
                if i != 0:
                    self.FrontQWidgetDict[self.current_key].changed.connect(self.on_front_changed)
            except Exception as ex:
                print(ex)
        try:
            self.FrontQWidgetDict['Front_0'].changed.connect(self.on_front_0_changed)
        except Exception as ex:
            print(ex)

    def on_front_0_changed(self):
        for i in range(1, self.n_fronts):
            self.current_key = f'Front_{i}'
            self.FrontQWidgetDict[self.current_key].refresh()

    def refresh(self):
        self.traced_image = self.TracerQWidget.traced_image
        for i in range(self.n_fronts):
            self.current_key = f'Front_{i}'
            self.FrontQWidgetDict[self.current_key].refresh()

    def on_front_changed(self):
        self.changed.emit()
