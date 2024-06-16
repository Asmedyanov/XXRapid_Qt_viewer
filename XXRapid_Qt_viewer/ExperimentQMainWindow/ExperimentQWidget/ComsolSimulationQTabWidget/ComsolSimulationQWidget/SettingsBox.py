from SettingsQWidgets.SettingsBoxQWidget import *


class SettingsBox(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        key = 'Quart'
        default = self.test_key(key, '1')
        self.Quart_line = SettingsLineQWidget(
            name=key,
            default=default,
            options_list=['1', '2', '3', '4']
        )
        self.QVBoxLayout.addWidget(self.Quart_line)
        self.SettingsDict[key] = self.Quart_line.value
        self.Quart_line.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        self.SettingsDict['Quart'] = self.Quart_line.value
        super().on_settings_line_changed()
