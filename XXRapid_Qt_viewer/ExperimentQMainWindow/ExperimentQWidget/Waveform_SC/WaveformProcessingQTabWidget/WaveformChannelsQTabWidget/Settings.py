from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'Diagnostics'
        default = self.test_key(key, 'Systron')  # Systron donner starting pulse generator
        self.DiagnosticsSettingsQWidget = SettingsLineQWidget(
            name=key,
            options_list=['Rogowski_coil',
                          'Systron',
                          'XXRapid_trig_out',
                          'Tektronix_VD'],
            default=default
        )
        self.SettingsDict[key] = self.DiagnosticsSettingsQWidget.value

        key = 'Smoothing'
        default = self.test_key(key, 5)  # ns
        self.SmoothingSettingsQWidget = SettingsLineQWidget(
            name=key,
            default=default,
            comment='ns',
            limit=[0, 1e3],
            step=1
        )
        self.SettingsDict[key] = self.SmoothingSettingsQWidget.value

        key = 'Coefficient'
        default = self.test_key(key, 5)
        self.CoefficientSettingsQWidget = SettingsLineQWidget(
            name=key,
            default=default,
            comment='Unit/Volt',
            limit=[-1e6, 1e6],
            step=0.5
        )
        self.SettingsDict[key] = self.CoefficientSettingsQWidget.value

        key = 'Shift'
        default = self.test_key(key, 0.0)
        self.ShiftSettingsQWidget = SettingsLineQWidget(
            name=key,
            default=default,
            comment='Unit',
            limit=[-1e6, 1e6],
            step=0.5
        )
        self.SettingsDict[key] = self.ShiftSettingsQWidget.value

        key = 'Delay'
        default = self.test_key(key, 0)
        self.DelaySettingsQWidget = SettingsLineQWidget(
            name=key,
            default=default,
            comment='ns',
            limit=[-1e9, 1e9],
            step=1
        )
        self.SettingsDict[key] = self.DelaySettingsQWidget.value

        self.Diagnostics = self.DiagnosticsSettingsQWidget.value
        self.DiagnosticsSettingsQWidget.changed.connect(self.on_settings_line_changed)
        self.QVBoxLayout.addWidget(self.DiagnosticsSettingsQWidget)

        self.TauSmooth = self.SmoothingSettingsQWidget.value * 1.0e-9
        self.SmoothingSettingsQWidget.changed.connect(self.on_settings_line_changed)
        self.QVBoxLayout.addWidget(self.SmoothingSettingsQWidget)

        self.Coefficient = self.CoefficientSettingsQWidget.value
        self.CoefficientSettingsQWidget.changed.connect(self.on_settings_line_changed)
        self.QVBoxLayout.addWidget(self.CoefficientSettingsQWidget)

        self.Shift = self.ShiftSettingsQWidget.value
        self.ShiftSettingsQWidget.changed.connect(self.on_settings_line_changed)
        self.QVBoxLayout.addWidget(self.ShiftSettingsQWidget)

        self.Delay = self.DelaySettingsQWidget.value * 1e-9
        self.DelaySettingsQWidget.changed.connect(self.on_settings_line_changed)
        self.QVBoxLayout.addWidget(self.DelaySettingsQWidget)

    def on_settings_line_changed(self):
        self.SettingsDict['Diagnostics'] = self.DiagnosticsSettingsQWidget.value
        self.SettingsDict['Smoothing'] = self.SmoothingSettingsQWidget.value
        self.SettingsDict['Coefficient'] = self.CoefficientSettingsQWidget.value
        self.SettingsDict['Shift'] = self.ShiftSettingsQWidget.value
        self.SettingsDict['Delay'] = self.DelaySettingsQWidget.value
        self.Diagnostics = self.DiagnosticsSettingsQWidget.value
        self.TauSmooth = self.SmoothingSettingsQWidget.value * 1.0e-9
        self.Coefficient = self.CoefficientSettingsQWidget.value
        self.Shift = self.ShiftSettingsQWidget.value
        self.Delay = self.DelaySettingsQWidget.value * 1e-9
        super().on_settings_line_changed()
