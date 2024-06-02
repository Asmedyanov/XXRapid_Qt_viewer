from XXRapid_Qt_viewer.utility.SettingsBoxQWidget import *


class ChannelSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        try:
            default = settings_dict['Diagnostics']
        except:
            default = 'Systron'
        self.DiagnosticsSettingsQWidget = SettingsLineQWidget(
            name='Diagnostics',
            options_list=['Rogowski_coil',
                          'Systron',
                          'XXRapid_trig_out',
                          'Tektronix_VD'],
            default=default
        )
        self.SettingsDict['Diagnostics'] = self.DiagnosticsSettingsQWidget.value

        try:
            default = settings_dict['Smoothing']
        except:
            default = 5.0
        self.SmoothingSettingsQWidget = SettingsLineQWidget(
            name='Smoothing',
            default=default,
            comment='ns',
            limit=[0.5, 1e3],
            step=0.5
        )
        self.SettingsDict['Smoothing'] = self.SmoothingSettingsQWidget.value

        try:
            default = settings_dict['Coefficient']
        except:
            default = 1
        self.CoefficientSettingsQWidget = SettingsLineQWidget(
            name='Coefficient',
            default=default,
            comment='Unit/Volt',
            limit=[-1e6, 1e6],
            step=0.5
        )
        self.SettingsDict['Coefficient'] = self.CoefficientSettingsQWidget.value

        try:
            default = settings_dict['Shift']
        except:
            default = 0
        self.ShiftSettingsQWidget = SettingsLineQWidget(
            name='Shift',
            default=default,
            comment='Unit',
            limit=[-1e6, 1e6],
            step=0.5
        )
        self.SettingsDict['Shift'] = self.ShiftSettingsQWidget.value

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


