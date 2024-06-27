from SettingsQWidgets.ChildQTabWidget import *
from .TracerQWidget import *
from .FrontsQTabWidget import *

'''from .XXRapidFrontingTracerQWidget import *
from .XXRapidFrontingFrontQWidget import *
from .SkimageOverlappedQWidget import *'''


class QuartQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, parent.current_key)
        self.camera_data = self.parent.current_camera_data
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        if self.settings_key not in self.parent.expansion_dict.keys():
            self.parent.expansion_dict[self.settings_key] = dict()
        self.expansion_dict = self.parent.expansion_dict[self.settings_key]
        try:
            self.TracerQWidget = TracerQWidget(self)
            self.addTab(self.TracerQWidget, self.TracerQWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.FrontsQTabWidget = FrontsQTabWidget(self)
            self.addTab(self.FrontsQTabWidget, self.FrontsQTabWidget.settings_key)
            self.FrontsQTabWidget.changed.connect(self.on_fronts_changed)
        except Exception as ex:
            print(ex)

    def on_fronts_changed(self):
        self.changed.emit()

    def refresh(self):
        self.camera_data = self.parent.current_camera_data
        self.TracerQWidget.refresh()

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        try:
            self.TracerQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.FrontsQTabWidget.save_report()
        except Exception as ex:
            print(ex)
