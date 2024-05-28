from XXRapid_Qt_viewer.Experiment.ExperimentQMainWindow import *


class MainWindow(ExperimentQMainWindow):
    def __init__(self):
        super().__init__(default=True)
        self.setWindowTitle("XXRapid_Qt_viewer (Default shot)")
        self.ExperimentQWidgetDict = dict()

        # Add "Open Folder" action to the menu
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder_dialog)
        open_folder_action.setShortcut(QKeySequence("Ctrl+O"))  # Set the shortcut
        self.file_menu.addAction(open_folder_action)

    def closeEvent(self, event):
        super().closeEvent(event)
        for experiment in self.ExperimentQWidgetDict.values():
            experiment.close()
        pass

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder",
                                                       os.path.expanduser("~"))
        if folder_path:
            print(f"Selected folder: {folder_path}")
        else:
            return

        key = folder_path.split('/')[-1]
        self.ExperimentQWidgetDict[key] = ExperimentQMainWindow(folder_path)
        self.ExperimentQWidgetDict[key].show()
