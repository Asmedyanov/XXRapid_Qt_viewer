from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal


class XXRapidTOFQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, timing_dict, expansion_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.SettingsDict = settings_dict

        key = 'Physical_expansion'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.XXRapidTOFPhysicalExpansionQTabWidget = XXRapidTOFPhysicalExpansionQWidget(timing_dict,
                                                                                            expansion_dict,
                                                                                            settings)
            self.addTab(self.XXRapidTOFPhysicalExpansionQTabWidget, key)
            self.XXRapidTOFPhysicalExpansionQTabWidget.changed.connect(self.on_XXRapidTOFPhysicalExpansionQTabWidget)
            self.SettingsDict[key] = self.XXRapidTOFPhysicalExpansionQTabWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidTOFPhysicalExpansionQTabWidget {ex}')

        key = 'Motion'
        try:
            settings = settings_dict[key]
        except:
            settings = dict()
        try:
            self.XXRapidTOFMotionQWidget = XXRapidTOFMotionQWidget(
                motion_dict=self.XXRapidTOFPhysicalExpansionQTabWidget.get_motion_dict(), settings_dict=settings)
            self.addTab(self.XXRapidTOFMotionQWidget, key)
            self.XXRapidTOFMotionQWidget.changed.connect(self.on_XXRapidTOFMotionQWidget)
            self.SettingsDict[key] = self.XXRapidTOFMotionQWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidTOFMotionQWidget {ex}')
        key = 'Velocity'
        try:
            settings = settings_dict[key]
        except:
            settings = dict()
        try:
            self.XXRapidTOFVelocityQTabWidget = XXRapidTOFVelocityQTabWidget(
                motion_approximated_dict=self.XXRapidTOFMotionQWidget.get_approximation(), settings_dict=settings)
            self.addTab(self.XXRapidTOFVelocityQTabWidget, key)
            # self.XXRapidTOFMotionQWidget.changed.connect(self.on_XXRapidTOFMotionQWidget)
            self.SettingsDict[key] = self.XXRapidTOFVelocityQTabWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidTOFVelocityQTabWidget {ex}')

    def on_XXRapidTOFPhysicalExpansionQTabWidget(self):
        try:
            self.XXRapidTOFMotionQWidget.set_data(self.XXRapidTOFPhysicalExpansionQTabWidget.get_motion_dict())
        except Exception as ex:
            print(f'self.XXRapidTOFPhysicalExpansionQTabWidget.set_data {ex}')
        # self.changed.emit()

    def set_data(self, timing_dict, expansion_dict):
        try:
            self.XXRapidTOFPhysicalExpansionQTabWidget.set_data(timing_dict, expansion_dict)
        except Exception as ex:
            print(f'self.XXRapidTOFPhysicalExpansionQTabWidget.set_data {ex}')

    def on_XXRapidTOFMotionQWidget(self):
        try:
            self.XXRapidTOFVelocityQTabWidget.set_data(self.XXRapidTOFMotionQWidget.motion_approximated_dict())
        except Exception as ex:
            print(f'self.XXRapidTOFPhysicalExpansionQTabWidget.set_data {ex}')
        self.changed.emit()

    def save_report(self, folder_name):
        if 'XXRapid_TOF' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/XXRapid_TOF')
        try:
            self.XXRapidTOFPhysicalExpansionQTabWidget.save_report(f'{folder_name}/XXRapid_TOF')
        except Exception as ex:
            print(f'XXRapidTOFPhysicalExpansionQTabWidget.save_report {ex}')
        try:
            self.XXRapidTOFMotionQWidget.save_report(f'{folder_name}/XXRapid_TOF')
        except Exception as ex:
            print(f'XXRapidTOFMotionQWidget.save_report {ex}')

        try:
            self.XXRapidTOFVelocityQTabWidget.save_report(f'{folder_name}/XXRapid_TOF')
        except Exception as ex:
            print(f'XXRapidTOFVelocityQTabWidget.save_report {ex}')


