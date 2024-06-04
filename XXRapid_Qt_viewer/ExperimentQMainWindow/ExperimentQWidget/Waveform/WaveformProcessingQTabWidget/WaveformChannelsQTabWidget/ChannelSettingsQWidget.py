from SettingsQWidgets.SettingsBoxQWidget import *


class ChannelSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        default = 'Systron'  # Systron donner starting pulse generator
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
        if key in settings_dict.keys():
            default = int(float(settings_dict[key]))
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
        if key in settings_dict.keys():
            default = float(settings_dict[key])
        self.CoefficientSettingsQWidget = SettingsLineQWidget(
            name=key,
            default=default,
            comment='Unit/Volt',
            limit=[-1e6, 1e6],
            step=0.5
        )
        self.SettingsDict[key] = self.CoefficientSettingsQWidget.value

        default = 0.0
        key = 'Shift'
        if key in settings_dict.keys():
            default = float(settings_dict[key])
        self.ShiftSettingsQWidget = SettingsLineQWidget(
            name=key,
            default=default,
            comment='Unit',
            limit=[-1e6, 1e6],
            step=0.5
        )
        self.SettingsDict[key] = self.ShiftSettingsQWidget.value

        self.Diagnostics = self.DiagnosticsSettingsQWidget.value
        self.DiagnosticsSettingsQWidget.changed.connect(self.OnDiagnosticsSettingsQWidgetChanged)
        self.QVBoxLayout.addWidget(self.DiagnosticsSettingsQWidget)

        self.TauSmooth = self.SmoothingSettingsQWidget.value * 1.0e-9
        self.SmoothingSettingsQWidget.changed.connect(self.OnSmoothingSettingsQWidgetChanged)
        self.QVBoxLayout.addWidget(self.SmoothingSettingsQWidget)

        self.Coefficient = self.CoefficientSettingsQWidget.value
        self.CoefficientSettingsQWidget.changed.connect(self.OnCoefficientSettingsQWidgetChanged)
        self.QVBoxLayout.addWidget(self.CoefficientSettingsQWidget)

        self.Shift = self.ShiftSettingsQWidget.value
        self.ShiftSettingsQWidget.changed.connect(self.OnShiftSettingsQWidgetChanged)
        self.QVBoxLayout.addWidget(self.ShiftSettingsQWidget)

    def OnShiftSettingsQWidgetChanged(self):
        self.Shift = self.ShiftSettingsQWidget.value
        self.SettingsDict['Shift'] = self.ShiftSettingsQWidget.value
        self.changed.emit()

    def OnDiagnosticsSettingsQWidgetChanged(self):
        self.Diagnostics = self.DiagnosticsSettingsQWidget.value
        self.SettingsDict['Diagnostics'] = self.DiagnosticsSettingsQWidget.value
        self.changed.emit()

    def OnSmoothingSettingsQWidgetChanged(self):
        self.TauSmooth = self.SmoothingSettingsQWidget.value * 1.0e-9
        self.SettingsDict['Smoothing'] = self.SmoothingSettingsQWidget.value
        self.changed.emit()

    def OnCoefficientSettingsQWidgetChanged(self):
        self.Coefficient = self.CoefficientSettingsQWidget.value
        self.SettingsDict['Coefficient'] = self.CoefficientSettingsQWidget.value
        self.changed.emit()

    def set_settings(self, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        self.SettingsDict = settings_dict
        try:
            default = settings_dict['Diagnostics']
        except:
            default = 'Systron'
        self.DiagnosticsSettingsQWidget.QComboBox.setCurrentText(default)
        self.SettingsDict['Diagnostics'] = self.DiagnosticsSettingsQWidget.value
