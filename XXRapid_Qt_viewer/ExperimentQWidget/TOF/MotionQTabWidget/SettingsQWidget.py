from XXRapid_Qt_viewer.utility.SettingsBoxQWidget import *


class SettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        key = 'Cross_section_1'
        try:
            default = settings_dict[key]
        except:
            default = 3

        self.CrossSection1SettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=1
        )
        self.QVBoxLayout.addWidget(self.CrossSection1SettingLine)
        self.CrossSection1SettingLine.changed.connect(self.OnSettingsLineChanged)

        key = 'Cross_section_2'
        try:
            default = settings_dict[key]
        except:
            default = 10

        self.CrossSection2SettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=1
        )
        self.QVBoxLayout.addWidget(self.CrossSection2SettingLine)
        self.CrossSection2SettingLine.changed.connect(self.OnSettingsLineChanged)

    def OnSettingsLineChanged(self):
        super().OnSettingsLineChanged()
        self.SettingsDict['Cross_section_1'] = self.CrossSection1SettingLine.value
        self.SettingsDict['Cross_section_2'] = self.CrossSection2SettingLine.value
        self.changed.emit()
