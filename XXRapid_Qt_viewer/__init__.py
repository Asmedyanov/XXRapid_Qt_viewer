from XXRapid_Qt_viewer.ExperimentQMainWindow import *


class MainWindow(ExperimentQMainWindow):
    def __init__(self):
        self.folder_path = 'Default_shot'
        super().__init__()
        self.setWindowTitle("XXRapid_Qt_viewer (Default shot)")
        self.ExperimentQWidgetDict = dict()

        # Add "Open Folder" action to the menu
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder_dialog)
        open_folder_action.setShortcut(QKeySequence("Ctrl+O"))  # Set the shortcut
        self.file_menu.addAction(open_folder_action)

    def closeEvent(self, event):
        for experiment in self.ExperimentQWidgetDict.values():
            experiment.close()
            experiment.deleteLater()
        super().closeEvent(event)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder",
                                                       os.path.expanduser("~"))
        if folder_path:
            print(f"Selected folder: {folder_path}")
        else:
            return

        key = folder_path.split('/')[-1]
        self.folder_path = folder_path
        try:
            self.ExperimentQWidgetDict[key] = ExperimentQMainWindow(self)
            self.ExperimentQWidgetDict[key].show()
        except Exception as ex:
            print(ex)
