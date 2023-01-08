import os
import json

import cv2
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QDockWidget, QTreeView, QFileSystemModel
from PySide6.QtWidgets import QListWidget, QLabel, QListWidgetItem
from PySide6.QtCore import Slot, Signal, Qt, QModelIndex
from PySide6.QtGui import QImage, QPixmap

class Dock(QDockWidget):
    def __init__(self, title:str):
        super().__init__()
        self._cntr = QWidget()
        self._cntr_lyt = QVBoxLayout(self._cntr)
        self._cntr_lyt.setContentsMargins(0, 0, 0, 0)
        self._cntr_lyt.setSpacing(2)
        self.setWindowTitle(title)
        self.setWidget(self._cntr)
        self.setFeatures(QDockWidget.DockWidgetFloatable
                        |QDockWidget.DockWidgetMovable)


class FileSystemTreeDock(Dock):
    item_clicked_sig = Signal(str)

    def __init__(self, title:str):
        super().__init__(title)
        self._model = QFileSystemModel()
        self._tree = QTreeView()
        self._tree.setModel(self._model)
        self._tree.setHeaderHidden(True)
        self._tree.clicked.connect(self.item_clicked)
        self._cntr_lyt.addWidget(self._tree)

    @Slot(str)
    def show_tree(self, root_dir:str):
        self._model.setRootPath(root_dir)
        self._tree.hideColumn(1) # size
        self._tree.hideColumn(2) # type
        self._tree.hideColumn(3) # modified date
        self._tree.setRootIndex(self._model.index(root_dir))
    
    @Slot(QModelIndex)
    def item_clicked(self, index:QModelIndex):
        file_path = self._model.filePath(index)
        self.item_clicked_sig.emit(file_path)


class FrameViewerDock(Dock):
    def __init__(self, title:str):
        super().__init__(title)
        self._list = QListWidget()
        self._list.setFlow(QListWidget.LeftToRight)
        self._cntr_lyt.addWidget(self._list)

    @Slot(str)
    def show_video(self, path:str):
        cap = cv2.VideoCapture(path)
        while(True):
            ret, frame = cap.read()
            if not ret:
                break
            item = FrameItem(1, frame)
            list_item = QListWidgetItem(self._list)
            list_item.setSizeHint(item.sizeHint())
            self._list.addItem(list_item)
            self._list.setItemWidget(list_item, item)
        cap.release()


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
        self._cntr_lyt = QVBoxLayout()
        self._cntr_lyt.addWidget(self._img)
        self.setLayout(self._cntr_lyt)
