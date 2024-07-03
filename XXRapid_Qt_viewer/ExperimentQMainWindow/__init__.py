from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog
from .ExperimentQWidget import *
from PyQt5.QtGui import QKeySequence
import shutil
import os


class ExperimentQMainWindow(QMainWindow):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
        if self.parent is not None:
            self.folder_path = self.parent.folder_path
        self.title = self.folder_path.split('/')[-1]
        self.auto_refresh = False
        title = f'Experiment {self.title}'
        if self.auto_refresh:
            title = f'{title} (auto refresh)'
        self.setWindowTitle(title)
        # Create a menu bar
        self.statusBar = self.statusBar()
        self.menu_bar = self.menuBar()

        self.ExperimentQWidget = ExperimentQWidget(self)
        self.setCentralWidget(self.ExperimentQWidget)
        self.file_menu = self.menu_bar.addMenu("File")
        self.settings_menu = self.menu_bar.addMenu("Settings")
        self.refresh_menu = self.menu_bar.addMenu("Refresh")

        save_settings_action = QAction("Save settings", self)
        save_settings_action.triggered.connect(self.on_save_settings)
        save_settings_action.setShortcut(QKeySequence("Ctrl+Shift+S"))  # Set the shortcut
        self.settings_menu.addAction(save_settings_action)

        default_settings_action = QAction("Default settings", self)
        default_settings_action.triggered.connect(self.on_default_settings)
        default_settings_action.setShortcut(QKeySequence("Ctrl+Shift+D"))  # Set the shortcut
        self.settings_menu.addAction(default_settings_action)

        import_settings_action = QAction("Import settings", self)
        import_settings_action.triggered.connect(self.on_import_settings)
        import_settings_action.setShortcut(QKeySequence("Ctrl+Shift+I"))  # Set the shortcut
        self.settings_menu.addAction(import_settings_action)

        save_trace_action = QAction("Save trace", self)
        save_trace_action.triggered.connect(self.on_save_trace)
        save_trace_action.setShortcut(QKeySequence("Ctrl+Shift+T"))  # Set the shortcut
        self.file_menu.addAction(save_trace_action)

        save_origin_pro_action = QAction("Save Origin Pro", self)
        save_origin_pro_action.triggered.connect(self.on_save_origin_pro)
        save_origin_pro_action.setShortcut(QKeySequence("Ctrl+Shift+O"))  # Set the shortcut
        self.file_menu.addAction(save_origin_pro_action)

        rebuild_action = QAction("Rebuild", self)
        rebuild_action.triggered.connect(self.on_rebuild)
        rebuild_action.setShortcut(QKeySequence("F5"))  # Set the shortcut
        self.refresh_menu.addAction(rebuild_action)

        auto_refresh_action = QAction("Auto Refresh", self)
        auto_refresh_action.triggered.connect(self.on_auto_refresh)
        auto_refresh_action.setShortcut(QKeySequence("Ctrl+F5"))  # Set the shortcut
        self.refresh_menu.addAction(auto_refresh_action)

    def on_save_origin_pro(self):
        try:
            self.ExperimentQWidget.save_origin_pro()
        except Exception as ex:
            print(ex)
        self.statusBar.showMessage(f'Origin file is saved')

    def on_import_settings(self):
        folder_path = QFileDialog.getOpenFileName(self, "Select SettingsFile.xml",
                                                  os.path.expanduser("~"))[0]
        try:
            filename = folder_path.split('/')[-1]
        except Exception as ex:
            print(ex)
            return
        if filename == 'SettingsFile.xml':
            current = f'{self.folder_path}/QtTraceFolder/SettingsFile.xml'
            shutil.copy(folder_path, current)
            self.remake()
            self.statusBar.showMessage(f'Settings are imported')
        else:
            self.statusBar.showMessage(f'Settings ARE NOT imported')

    def on_auto_refresh(self):
        self.auto_refresh = not self.auto_refresh
        self.on_rebuild()
        title = f'Experiment {self.title}'
        if self.auto_refresh:
            title = f'{title} (auto refresh)'
            self.statusBar.showMessage(f'Auto Refresh is ON')
        else:
            title = f'{title} (manual refresh)'
            self.statusBar.showMessage(f'Auto Refresh is OFF')
        self.setWindowTitle(title)

    def on_rebuild(self):
        self.ExperimentQWidget.save_settings()
        self.remake()
        self.statusBar.showMessage(f'Rebuild')

    def remake(self):
        self.layout().removeWidget(self.ExperimentQWidget)
        self.ExperimentQWidget.deleteLater()
        self.ExperimentQWidget = ExperimentQWidget(self)
        self.setCentralWidget(self.ExperimentQWidget)

    def on_default_settings(self):
        default = 'Default_shot/QtTraceFolder/SettingsFile.xml'
        current = f'{self.folder_path}/QtTraceFolder/SettingsFile.xml'
        shutil.copy(default, current)
        self.remake()
        self.statusBar.showMessage(f'Settings are default')

    def on_save_settings(self):
        self.ExperimentQWidget.save_settings()
        self.statusBar.showMessage(f'Settings are saved')

    def on_save_trace(self):
        self.on_rebuild()
        self.ExperimentQWidget.save_report()
        self.statusBar.showMessage(f'Trace is saved')

    def closeEvent(self, event):
        self.ExperimentQWidget.save_report()
        self.ExperimentQWidget.save_settings()
