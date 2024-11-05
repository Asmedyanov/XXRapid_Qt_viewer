import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QAction, QTreeView,
    QVBoxLayout, QWidget, QSplitter, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QSettings, QModelIndex, QDir
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class MultiRootFileSystemModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(['Name'])
        self.roots = []

    def add_root_path(self, path):
        if path not in self.roots:
            self.roots.append(path)
            self.append_row_for_path(path)

    def remove_root_path(self, path):
        if path in self.roots:
            self.roots.remove(path)
            root_item = self.find_root_item(path)
            if root_item:
                self.removeRow(root_item.row())

    def find_root_item(self, path):
        for i in range(self.rowCount()):
            item = self.item(i)
            if item.data(Qt.UserRole) == path:
                return item
        return None

    def append_row_for_path(self, path, parent_item=None):
        if not parent_item:
            parent_item = self.invisibleRootItem()

        dir_item = QStandardItem(os.path.basename(path))
        dir_item.setData(path, Qt.UserRole)
        parent_item.appendRow(dir_item)

        if os.path.isdir(path):
            for item in os.listdir(path):
                self.append_row_for_path(os.path.join(path, item), dir_item)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class WorkspaceManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workspace Manager")
        self.setGeometry(100, 100, 800, 600)

        self.settings = QSettings("YourCompany", "WorkspaceManager")
        self.default_workspace = self.settings.value("default_workspace", None)
        self.recent_workspaces = self.settings.value("recent_workspaces", [])

        self.initUI()

        if not self.default_workspace:
            self.prompt_for_default_workspace()
        else:
            self.add_workspace(self.default_workspace)

    def initUI(self):
        self.create_menu()
        self.create_main_layout()

    def create_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_workspace_action = QAction("New Workspace", self)
        new_workspace_action.triggered.connect(self.create_new_workspace)
        file_menu.addAction(new_workspace_action)

        open_workspace_action = QAction("Open Workspace", self)
        open_workspace_action.triggered.connect(self.open_workspace)
        file_menu.addAction(open_workspace_action)

        close_workspace_action = QAction("Close Workspace", self)
        close_workspace_action.triggered.connect(self.close_workspace)
        file_menu.addAction(close_workspace_action)

        # Recent workspaces submenu
        self.recent_menu = file_menu.addMenu("Recent Workspaces")
        self.update_recent_workspaces_menu()

        add_file_action = QAction("Add File to Workspace", self)
        add_file_action.triggered.connect(self.add_file_to_workspace)
        file_menu.addAction(add_file_action)

    def create_main_layout(self):
        main_layout = QVBoxLayout()

        splitter = QSplitter(Qt.Horizontal)

        # Workspace Tree View
        self.tree_view = QTreeView()
        self.tree_model = MultiRootFileSystemModel()
        self.tree_view.setModel(self.tree_model)
        self.tree_view.clicked.connect(self.on_tree_view_clicked)
        splitter.addWidget(self.tree_view)

        # File Viewer
        self.file_viewer = QTextEdit()
        splitter.addWidget(self.file_viewer)

        splitter.setSizes([200, 600])

        main_layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def prompt_for_default_workspace(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Default Workspace Directory")
        if folder:
            self.default_workspace = folder
            self.settings.setValue("default_workspace", folder)
            self.add_workspace(folder)
        else:
            QMessageBox.warning(self, "No Default Workspace",
                                "A default workspace must be selected to use the application.")
            self.close()

    def create_new_workspace(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Workspace Directory")
        if folder:
            self.add_workspace(folder)

    def open_workspace(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Workspace Directory")
        if folder:
            self.add_workspace(folder)

    def add_workspace(self, folder):
        self.tree_model.add_root_path(folder)
        if folder not in self.recent_workspaces:
            self.recent_workspaces.insert(0, folder)
            self.recent_workspaces = self.recent_workspaces[:5]  # Keep only 5 recent workspaces
            self.settings.setValue("recent_workspaces", self.recent_workspaces)
            self.update_recent_workspaces_menu()

    def update_recent_workspaces_menu(self):
        self.recent_menu.clear()
        for workspace in self.recent_workspaces:
            action = QAction(workspace, self)
            action.triggered.connect(lambda checked, folder=workspace: self.add_workspace(folder))
            self.recent_menu.addAction(action)

    def add_file_to_workspace(self):
        current_index = self.tree_view.currentIndex()
        if current_index.isValid():
            dir_path = self.tree_model.itemFromIndex(current_index).data(Qt.UserRole)
            if os.path.isdir(dir_path):
                file, _ = QFileDialog.getOpenFileName(self, "Add File to Workspace")
                if file:
                    os.system(f'cp {file} {dir_path}')
                    self.tree_model.append_row_for_path(os.path.join(dir_path, os.path.basename(file)))

    def close_workspace(self):
        current_index = self.tree_view.currentIndex()
        if current_index.isValid():
            dir_path = self.tree_model.itemFromIndex(current_index).data(Qt.UserRole)
            self.tree_model.remove_root_path(dir_path)

    def on_tree_view_clicked(self, index):
        file_path = self.tree_model.itemFromIndex(index).data(Qt.UserRole)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                self.file_viewer.setText(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WorkspaceManager()
    window.show()
    sys.exit(app.exec_())
