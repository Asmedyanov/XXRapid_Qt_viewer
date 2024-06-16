from SettingsQWidgets.SettingsBoxQWidget import *


class SettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        key = 'Cross_section_1'
        default = self.test_key(key, 3)

        self.CrossSection1SettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=1
        )
        self.QVBoxLayout.addWidget(self.CrossSection1SettingLine)
        self.CrossSection1SettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Cross_section_2'
        default = self.test_key(key, 10)

        self.CrossSection2SettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=1
        )
        self.QVBoxLayout.addWidget(self.CrossSection2SettingLine)
        self.CrossSection2SettingLine.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        self.SettingsDict['Cross_section_1'] = self.CrossSection1SettingLine.value
        self.SettingsDict['Cross_section_2'] = self.CrossSection2SettingLine.value
        super().on_settings_line_changed()
