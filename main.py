import os
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QVBoxLayout, QWidget, QFileDialog
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QAction

from src.docks import FileSystemTreeDock, FrameViewerDock


class MainWindow(QMainWindow):
    open_dir_sig = Signal(str)

    def __init__(self, title:str):
        super().__init__()
        # --- Base UI ---
        style = "background-color: rgb(170, 170, 170)"
        self.cntr = QWidget()
        self.cntr.setStyleSheet(style)
        self.cntr_lyt = QVBoxLayout(self.cntr)
        self.cntr_lyt.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle(title)
        self.resize(1280, 768)
        self.setCentralWidget(self.cntr)

        # --- MenuBar ---
        file_menu = self.menuBar().addMenu("File")
        open_dir = QAction("Open Folder ...", self)
        open_dir.triggered.connect(self.open_dir_triggered)
        file_menu.addAction(open_dir)

        # --- Dock Widgets ---
        self.fs_dock = FileSystemTreeDock("Explorer")
        self.open_dir_sig.connect(self.fs_dock.show_tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.fs_dock)

        self.fv_dock = FrameViewerDock("Untitled")
        self.fs_dock.item_clicked_sig.connect(self.fv_dock.show_video)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.fv_dock)

    @Slot()
    def open_dir_triggered(self):
        root_dir = QFileDialog.getExistingDirectory(
            self, "Select a Directory", '.')
        self.open_dir_sig.emit(root_dir)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow("Labeler")
    window.show()
    sys.exit(app.exec())
