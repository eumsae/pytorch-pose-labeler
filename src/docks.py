import os
import json

import cv2
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox
from PySide6.QtWidgets import QDockWidget, QTreeView, QFileSystemModel, QLineEdit
from PySide6.QtWidgets import QListWidget, QLabel, QListWidgetItem, QSlider, QSpinBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Slot, Signal, Qt, QModelIndex
from PySide6.QtGui import QImage, QPixmap


class Dock(QDockWidget):
    def __init__(self, title:str):
        super().__init__()
        #self._container_layout.setContentsMargins(0, 0, 0, 0)
        #self._container_layout.setSpacing(2)
        self.setWindowTitle(title)
        self.setFeatures(QDockWidget.DockWidgetFloatable
                        |QDockWidget.DockWidgetMovable)


class FileSystemTreeDock(Dock):
    file_system_tree_item_clicked = Signal(str)

    def __init__(self, title:str):
        super().__init__(title)
        self._ui()
        self._event()

    def _ui(self):
        self.setLayout(QVBoxLayout())
        self._model = QFileSystemModel()
        self._tree = QTreeView()
        self._tree.setModel(self._model)
        self._tree.setHeaderHidden(True)
        self.layout().addWidget(self._tree)

    def _event(self):
        self._tree.clicked.connect(self._item_clicked)

    @Slot(str)
    def show_tree(self, root_dir:str):
        self._model.setRootPath(root_dir)
        self._tree.hideColumn(1) # size
        self._tree.hideColumn(2) # type
        self._tree.hideColumn(3) # modified date
        self._tree.setRootIndex(self._model.index(root_dir))

    @Slot(QModelIndex)
    def _item_clicked(self, index:QModelIndex):
        self.file_system_tree_item_clicked.emit(self._model.filePath(index))


class PreviewThumbnailsDock(Dock):
    preview_thumbnail_row_changed = Signal(int)

    def __init__(self, title:str):
        super().__init__(title)
        self._ui()
        self._event()
    
    def _ui(self):
        self.setLayout(QHBoxLayout())
        self._list = QListWidget()
        self._list.setFlow(QListWidget.LeftToRight)
        self.layout().addWidget(self._list)

    def _event(self):
        self._list.currentRowChanged.connect(self._row_changed)

    @Slot()
    def show_thumbnails(self):
        pass

    @Slot(int)
    def _row_changed(self, row:int):
        self.preview_thumbnail_row_changed.emit(row)

    
    """
    @Slot(int)
    def row_changed(self, row):
        if row == -1:
            return
        item = self._list.item(row)
        widget = self._list.itemWidget(item)
        print(widget._idx)

    @Slot(str)
    def show_video_info(self, path:str):
        self._path = path
        cap = cv2.VideoCapture(path)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        tof = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
        print(os.path.dirname(path), w, h, tof, fps)
        cap.release()

    @Slot(str)
    def show_frames(self):
        if self._path is None:
            return
        cap = cv2.VideoCapture(self._path)
        tof = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(round(cap.get(cv2.CAP_PROP_FPS)))

        step = int(fps // 10)
        indices = list(range(0, tof, step))
        for i in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            _, frame = cap.read()
            item = FrameItem(i, frame)
            list_item = QListWidgetItem(self._list)
            list_item.setSizeHint(item.sizeHint())
            self._list.addItem(list_item)
            self._list.setItemWidget(list_item, item)
        cap.release()
    """




class FrameItem(QWidget):
    def get_qimg(cls, img:np.ndarray):
        h, w, c = img.shape
        qimg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
        return qimg

    def __init__(self, idx:int, img:np.ndarray):
        super().__init__()
        self._idx = idx
        self._img = QLabel()

        img = cv2.resize(img, dsize=(192, 108))
        img = self.get_qimg(img)
        img = QPixmap.fromImage(img)

        self._img.setPixmap(img)
        self._container_layout = QVBoxLayout()
        self._container_layout.addWidget(self._img)
        self.setLayout(self._container_layout)
