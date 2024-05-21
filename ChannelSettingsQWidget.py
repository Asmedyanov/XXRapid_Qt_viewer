from PyQt5.QtWidgets import QVBoxLayout

from MySettingsQWidget import *


class ChannelSettingsQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, settings_dict=None):
        super().__init__()
        self.QVBoxLayout = QVBoxLayout()
        self.setLayout(self.QVBoxLayout)
        if settings_dict is None:
            self.SettingsDict = dict()
            self.DiagnosticsSettingsQWidget = MySettingsQWidget(
                name='Diagnostics',
                options_list=['Rogowski_coil',
                              'Systron',
                              'XXRapid_trig_out',
                              'Tektronix_VD']
            )
            self.SettingsDict['Diagnostics'] = self.DiagnosticsSettingsQWidget.value
            self.SmoothingSettingsQWidget = MySettingsQWidget(
                name='Smoothing',
                default=5,
                comment='ns'
            )
            self.SettingsDict['Smoothing'] = self.SmoothingSettingsQWidget.value
            self.CoefficientSettingsQWidget = MySettingsQWidget(
                name='Coefficient',
                default=300,
                comment='Unit/Volt'
            )
            self.SettingsDict['Coefficient'] = self.CoefficientSettingsQWidget.value
        else:
            self.SettingsDict = settings_dict
            self.DiagnosticsSettingsQWidget = MySettingsQWidget(
                name='Diagnostics',
                default=self.SettingsDict['Diagnostics'],
                options_list=['Rogowski_coil',
                              'Systron',
                              'XXRapid_trig_out',
                              'Tektronix_VD']
            )
            self.SmoothingSettingsQWidget = MySettingsQWidget(
                name='Smoothing',
                default=self.SettingsDict['Smoothing'],
                comment='ns'
            )
            self.CoefficientSettingsQWidget = MySettingsQWidget(
                name='Coefficient',
                default=self.SettingsDict['Coefficient'],
                comment='Unit/Volt'
            )

        self.Diagnostics = self.DiagnosticsSettingsQWidget.value
        self.DiagnosticsSettingsQWidget.changed.connect(self.OnDiagnosticsSettingsQWidgetChanged)
        self.QVBoxLayout.addWidget(self.DiagnosticsSettingsQWidget)

        self.TauSmooth = self.SmoothingSettingsQWidget.value * 1.0e-9
        self.SmoothingSettingsQWidget.changed.connect(self.OnSmoothingSettingsQWidgetChanged)
        self.QVBoxLayout.addWidget(self.SmoothingSettingsQWidget)

        self.Coefficient = self.CoefficientSettingsQWidget.value
        self.CoefficientSettingsQWidget.changed.connect(self.OnCoefficientSettingsQWidgetChanged)
        self.QVBoxLayout.addWidget(self.CoefficientSettingsQWidget)

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
