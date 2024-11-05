import sys
import os
import xml.etree.ElementTree as ET
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QFileSystemModel, QTextEdit,
    QSplitter, QTableWidget, QTableWidgetItem, QMdiArea, QMdiSubWindow,
    QLabel, QVBoxLayout, QMenu, QAction, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsTextItem, QGraphicsLineItem
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPen, QColor
import qdarkstyle
import random


class MindMapNode(QGraphicsEllipseItem):
    def __init__(self, x, y, tag, value=None):
        super().__init__(-30, -15, 60, 30)
        self.setPos(x, y)
        self.setBrush(QColor(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
        self.setPen(QPen(QColor(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))))

        self.text_item = QGraphicsTextItem(tag, self)
        self.text_item.setDefaultTextColor(Qt.black)
        self.text_item.setPos(-25, -10)

        if value:
            self.comment_item = QGraphicsTextItem(f'({value})', self)
            self.comment_item.setDefaultTextColor(Qt.darkGray)
            self.comment_item.setPos(-25, 10)


class FileViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Viewer")
        self.setGeometry(100, 100, 1200, 600)

        self.splitter = QSplitter(Qt.Horizontal)

        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.tree.clicked.connect(self.on_tree_clicked)
        self.tree.setFixedWidth(250)

        self.model = QFileSystemModel()
        self.root_path = os.path.abspath("./Default_shot")
        self.model.setRootPath(self.root_path)

        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.root_path))

        self.mdi_area = QMdiArea()
        self.mdi_area.setViewMode(QMdiArea.TabbedView)
        self.mdi_area.setTabsClosable(True)
        self.mdi_area.setTabsMovable(True)
        self.mdi_area.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())  # Apply dark style to MDI area
        self.mdi_area.subWindowActivated.connect(self.update_window_menu)

        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.mdi_area)

        self.setCentralWidget(self.splitter)

        # Create menu actions
        self.create_actions()
        self.create_menu()

    def create_actions(self):
        self.cascade_action = QAction("Cascade", self)
        self.cascade_action.triggered.connect(self.mdi_area.cascadeSubWindows)

        self.tile_action = QAction("Tile", self)
        self.tile_action.triggered.connect(self.mdi_area.tileSubWindows)

        self.close_all_tabs_action = QAction("Close All Tabs", self)
        self.close_all_tabs_action.triggered.connect(self.close_all_tabs)

        self.close_other_tabs_action = QAction("Close Other Tabs", self)
        self.close_other_tabs_action.triggered.connect(self.close_other_tabs)

    def create_menu(self):
        self.menu_bar = self.menuBar()
        self.view_menu = self.menu_bar.addMenu("View")
        self.view_menu.addAction(self.cascade_action)
        self.view_menu.addAction(self.tile_action)
        self.view_menu.addAction(self.close_all_tabs_action)
        self.view_menu.addAction(self.close_other_tabs_action)

    def update_window_menu(self):
        active_subwindow = self.mdi_area.activeSubWindow()

    def on_tree_clicked(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.open_file(file_path)

    def open_file(self, file_path):
        # Use full file path as the tab name to handle files with the same name in different directories
        tab_name = file_path

        # Check if the file is already open in a tab
        for sub_window in self.mdi_area.subWindowList():
            if sub_window.windowTitle() == tab_name:
                self.mdi_area.setActiveSubWindow(sub_window)
                return

        if file_path.endswith(".txt"):
            self.open_text_file(file_path)
        elif file_path.endswith(".csv"):
            self.open_csv_file(file_path)
        elif file_path.endswith(".xml"):
            self.open_xml_file(file_path)
        elif file_path.endswith((".png", ".jpg", ".bmp")):
            self.open_image_file(file_path)
        else:
            # Ignore unsupported file types
            return

    def open_text_file(self, file_path, unsupported=False):
        with open(file_path, 'r') as file:
            content = file.read()
            text_edit = QTextEdit()
            text_edit.setText(content)
            tab_name = file_path if not unsupported else f"Unsupported: {file_path}"

            sub_window = QMdiSubWindow()
            sub_window.setWidget(text_edit)
            sub_window.setWindowTitle(tab_name)
            sub_window.setAttribute(Qt.WA_DeleteOnClose)

            self.mdi_area.addSubWindow(sub_window)
            sub_window.show()
            self.mdi_area.setActiveSubWindow(sub_window)

    def open_csv_file(self, file_path):
        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            data = list(reader)

        table_widget = QTableWidget()
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(item))

        tab_name = file_path

        sub_window = QMdiSubWindow()
        sub_window.setWidget(table_widget)
        sub_window.setWindowTitle(tab_name)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)

        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
        self.mdi_area.setActiveSubWindow(sub_window)

    def open_xml_file(self, file_path):
        scene = QGraphicsScene()
        view = QGraphicsView(scene)

        tree = ET.parse(file_path)
        root = tree.getroot()
        self.build_mind_map(scene, root, 0, 0, None)

        tab_name = file_path

        sub_window = QMdiSubWindow()
        sub_window.setWidget(view)
        sub_window.setWindowTitle(tab_name)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)

        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
        self.mdi_area.setActiveSubWindow(sub_window)

    def build_mind_map(self, scene, element, x, y, parent_item):
        value = element.text.strip() if element.text else None
        node = MindMapNode(x, y, element.tag, value)
        scene.addItem(node)
        if parent_item:
            line = QGraphicsLineItem(parent_item.pos().x(), parent_item.pos().y(), node.pos().x(), node.pos().y())
            line.setPen(QPen(QColor(150, 150, 150)))
            scene.addItem(line)

        child_x = x - (len(element) - 1) * 150 / 2
        child_y = y + 150

        for child in element:
            self.build_mind_map(scene, child, child_x, child_y, node)
            child_x += 150

    def open_image_file(self, file_path):
        label = QLabel()
        pixmap = QPixmap(file_path)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        tab_name = file_path

        sub_window = QMdiSubWindow()
        sub_window.setWidget(label)
        sub_window.setWindowTitle(tab_name)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)

        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
        self.mdi_area.setActiveSubWindow(sub_window)

    def close_all_tabs(self):
        for sub_window in self.mdi_area.subWindowList():
            sub_window.close()

    def close_other_tabs(self):
        active_subwindow = self.mdi_area.activeSubWindow()
        if not active_subwindow:
            return

        for sub_window in self.mdi_area.subWindowList():
            if sub_window != active_subwindow:
                sub_window.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set dark mode using qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # Define the custom root name
    app.setApplicationDisplayName("Default_shot")

    viewer = FileViewer()
    viewer.show()
    sys.exit(app.exec_())
