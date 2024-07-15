from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame_dict = dict()
        self.n_frame = 4
        for i in range(self.n_frame):
            key = f'Camera_{i + 1}'
            default = self.test_key(key, 0.0)  # pix/mm
            self.frame_dict[key] = SettingsLineQWidget(
                name=key,
                default=default,
                limit=[-90, 90],
                step=0.1,
                comment='degrees'
            )
            self.QVBoxLayout.addWidget(self.frame_dict[key])
            self.SettingsDict[key] = self.frame_dict[key].value
            self.frame_dict[key].changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        for my_key, my_widget in self.frame_dict.items():
            self.SettingsDict[my_key] = my_widget.value
        super().on_settings_line_changed()
