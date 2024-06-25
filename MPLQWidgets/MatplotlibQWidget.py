from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtGui import QGuiApplication, QImage, QPixmap, QKeyEvent
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import pyqtSignal,QEvent
import io


class MatplotlibQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.layout = QVBoxLayout()
        self.figure = plt.figure()
        self.figure.set_layout_engine(layout='tight')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.png_name = 'MatplotlibQWidget'
        self.changed.connect(self.on_changed)


    def on_key(self, a0):
        print(a0.key)
        if a0.key == 'c':  # You could choose any key binding
            # Save the current figure to a buffer
            buf = io.BytesIO()
            self.figure.savefig(buf, format='png')
            buf.seek(0)

            # Create a QImage from the buffer
            image = QImage()
            image.loadFromData(buf.getvalue(), 'PNG')

            # Convert QImage to QPixmap (suitable for clipboard)
            pixmap = QPixmap.fromImage(image)

            # Copy QPixmap to clipboard
            clipboard = QGuiApplication.clipboard()
            clipboard.setPixmap(pixmap, QGuiApplication.Clipboard)

            # Optionally, emit a signal to indicate the clipboard operation is done
            self.changed.emit()

    def add_figure_to_clipboard(self, event):
        if event.key == 'c':  # You could choose any key binding
            # Save the current figure to a buffer
            buf = io.BytesIO()
            self.figure.savefig(buf, format='png')
            buf.seek(0)

            # Create a QImage from the buffer
            image = QImage()
            image.loadFromData(buf.getvalue(), 'PNG')

            # Convert QImage to QPixmap (suitable for clipboard)
            pixmap = QPixmap.fromImage(image)

            # Copy QPixmap to clipboard
            clipboard = QGuiApplication.clipboard()
            clipboard.setPixmap(pixmap, QGuiApplication.Clipboard)

            # Optionally, emit a signal to indicate the clipboard operation is done
            self.changed.emit()

    def on_changed(self):
        self.figure.canvas.draw()

    def set_data(self, *args, **kwargs):
        pass

    def save_report(self, folder_name='./'):
        self.figure.savefig(f'{folder_name}/{self.png_name}.png')
