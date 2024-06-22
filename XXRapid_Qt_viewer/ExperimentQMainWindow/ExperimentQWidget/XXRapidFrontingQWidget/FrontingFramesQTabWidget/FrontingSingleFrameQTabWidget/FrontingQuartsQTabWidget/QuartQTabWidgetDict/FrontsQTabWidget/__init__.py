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
        for i in range(self.n_fronts):
            self.current_key = f'Front_{i}'
            try:
                self.FrontQWidgetDict[self.current_key] = FrontQWidget(self)
                self.addTab(self.FrontQWidgetDict[self.current_key], self.current_key)
                self.FrontQWidgetDict[self.current_key].changed.connect(self.on_front_changed)
            except Exception as ex:
                print(ex)

    def refresh(self):
        self.traced_image = self.TracerQWidget.traced_image
        for i in range(self.n_fronts):
            self.current_key = f'Front_{i}'
            self.FrontQWidgetDict[self.current_key].refresh()
        pass

    def on_front_changed(self):
        self.changed.emit()
