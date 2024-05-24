from PyQt5.QtWidgets import QVBoxLayout

from SettingsLineQWidget import *


class ChannelSettingsQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, settings_dict=None):
        super().__init__()
        self.QVBoxLayout = QVBoxLayout()
        self.setLayout(self.QVBoxLayout)
        if settings_dict is None:
            self.SettingsDict = dict()
            self.DiagnosticsSettingsQWidget = SettingsLineQWidget(
                name='Diagnostics',
                options_list=['Rogowski_coil',
                              'Systron',
                              'XXRapid_trig_out',
                              'Tektronix_VD']
            )
            self.SettingsDict['Diagnostics'] = self.DiagnosticsSettingsQWidget.value
            self.SmoothingSettingsQWidget = SettingsLineQWidget(
                name='Smoothing',
                default=5,
                comment='ns',
                limit=[0.5, 1e3],
                step=0.5
            )
            self.SettingsDict['Smoothing'] = self.SmoothingSettingsQWidget.value
            self.ShiftSettingsQWidget = SettingsLineQWidget(
                name='Shift',
                default=0,
                comment='Unit',
                limit=[-1e6, 1e6],
                step=0.5
            )
            self.SettingsDict['Shift'] = self.ShiftSettingsQWidget.value
            self.CoefficientSettingsQWidget = SettingsLineQWidget(
                name='Coefficient',
                default=1,
                comment='Unit/Volt',
                limit=[-1e6, 1e6],
                step=0.5
            )
            self.SettingsDict['Coefficient'] = self.CoefficientSettingsQWidget.value
        else:
            self.SettingsDict = settings_dict
            self.DiagnosticsSettingsQWidget = SettingsLineQWidget(
                name='Diagnostics',
                default=self.SettingsDict['Diagnostics'],
                options_list=['Rogowski_coil',
                              'Systron',
                              'XXRapid_trig_out',
                              'Tektronix_VD']
            )
            self.SmoothingSettingsQWidget = SettingsLineQWidget(
                name='Smoothing',
                default=self.SettingsDict['Smoothing'],
                comment='ns',
                limit=[0.5, 1e3],
                step=0.5
            )
            self.ShiftSettingsQWidget = SettingsLineQWidget(
                name='Shift',
                default=self.SettingsDict['Shift'],
                comment='Unit',
                limit=[-1e6, 1e6],
                step=0.5

            )
            self.CoefficientSettingsQWidget = SettingsLineQWidget(
                name='Coefficient',
                default=self.SettingsDict['Coefficient'],
                comment='Unit/Volt',
                limit=[-1e6, 1e6],
                step=0.5
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
