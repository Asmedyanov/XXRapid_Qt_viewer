from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'Start'
        default = self.test_key(key, 0)  # ns
        self.StartLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 1e9],
            step=1,
            comment='ns'
        )
        self.StartLine.changed.connect(self.on_settings_line_changed)
        self.QVBoxLayout.addWidget(self.StartLine)
        self.SettingsDict[key] = self.StartLine.value

        key = 'N_shutters'
        default = self.test_key(key, 8)
        self.n_shutters_line = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 1e1],
            step=1,
        )
        self.n_shutters_line.changed.connect(self.on_settings_line_changed)
        self.QVBoxLayout.addWidget(self.n_shutters_line)
        self.SettingsDict[key] = self.n_shutters_line.value

        self.shutters_line_dict = self.get_shutters_line_dict()

    def get_shutters_line_dict(self):
        shutters_line_dict = dict()
        n_shutters = self.n_shutters_line.value
        for i in range(n_shutters):
            key = f'Shutter_{i + 1}'
            default = self.test_key(key, 0)  # ns
            shutters_line_dict[key] = SettingsLineQWidget(
                name=key,
                default=default,
                limit=[0, 1e9],
                step=1,
                comment='ns'
            )
            self.QVBoxLayout.addWidget(shutters_line_dict[key])
            shutters_line_dict[key].changed.connect(self.on_settings_line_changed)
            self.SettingsDict[key] = shutters_line_dict[key].value
        return shutters_line_dict

    def refresh(self):
        self.SettingsDict['Start'] = self.StartLine.value
        self.SettingsDict['N_shutters'] = self.n_shutters_line.value
        for my_key, my_line in self.shutters_line_dict.items():
            self.SettingsDict[my_key] = my_line.value
        super().refresh()

    def on_settings_line_changed(self):
        self.refresh()
        super().on_settings_line_changed()
