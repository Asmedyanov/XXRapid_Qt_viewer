from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog
from .ExperimentQWidget import *
from PyQt5.QtGui import QKeySequence


class ExperimentQMainWindow(QMainWindow):
    def __init__(self, folder_path='Default_shot', default=False):
        super().__init__()
        self.folder_path = folder_path
        self.title = folder_path.split('/')[-1]
        self.setWindowTitle(f'Experiment {self.title}')
        # Create a menu bar
        self.statusBar = self.statusBar()
        self.menu_bar = self.menuBar()

        self.ExperimentQWidget = ExperimentQWidget(self, folder_path, default)
        self.setCentralWidget(self.ExperimentQWidget)
        self.file_menu = self.menu_bar.addMenu("File")

        save_settings_action = QAction("Save settings", self)
        save_settings_action.triggered.connect(self.on_save_settings)
        save_settings_action.setShortcut(QKeySequence("Ctrl+Shift+S"))  # Set the shortcut
        self.file_menu.addAction(save_settings_action)

        default_settings_action = QAction("Default settings", self)
        default_settings_action.triggered.connect(self.on_default_settings)
        default_settings_action.setShortcut(QKeySequence("Ctrl+Shift+D"))  # Set the shortcut
        self.file_menu.addAction(default_settings_action)

        save_trace_action = QAction("Save trace", self)
        save_trace_action.triggered.connect(self.on_save_trace)
        save_trace_action.setShortcut(QKeySequence("Ctrl+Shift+T"))  # Set the shortcut
        self.file_menu.addAction(save_trace_action)

    def on_default_settings(self):
        self.ExperimentQWidget.set_default_settings()
        self.statusBar.showMessage(f'Settings are default')

    def on_save_settings(self):
        self.ExperimentQWidget.SaveSettings()
        self.statusBar.showMessage(f'Settings are saved')

    def on_save_trace(self):
        self.ExperimentQWidget.SaveTrace()
        self.statusBar.showMessage(f'Trace is saved')

    def closeEvent(self, event):
        self.ExperimentQWidget.SaveTrace()
        self.ExperimentQWidget.SaveSettings()
