import numpy as np
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QImage

from src.images import resize_keeping_aspect_ratio


class ImageNotNumpyArrayError(Exception):
    def __init__(self):
        msg = "The background image must be an " \
            + "instance of numpy.ndarray."
        super().__init__(msg)


def get_qimg_from(img):
    """ Convert the image to a QImage instance.
    Args:
        img(np.ndarray):
    Returns:
        qimg(PySide6.QtGui.QImage):
    """
    h, w, c = img.shape
    form = QImage.Format_RGB888
    qimg = QImage(img.data, w, h, w*c, form)
    return qimg


class DefaultGraphicsView(QGraphicsView):

    def __init__(self, *args):
        super().__init__(*args)
        self._background_img = None
        self._background_img_scaling_info = None
        self.setScene(QGraphicsScene())
        self.update_view()

    def set_background(self, img):
        if not isinstance(img, np.ndarray):
            raise ImageNotNumpyArrayError
        self._background_img = img

    def update_view(self):
        if self._background_img is not None:
            img = self.__scale_background()
            img = get_qimg_from(img)
            self.setBackgroundBrush(img)  # draw
        self.__adjust_scene_area()

    def resizeEvent(self, event):
        # @override
        self.update_view()
        return super().resizeEvent(event)

    def __scale_background(self):
        bw, bh = self._background_img.shape[:2][::-1]
        vw, vh = self.__get_view_size()
        if bw != vw or bh != vh:
            img, info = resize_keeping_aspect_ratio(
                self._background_img, target_size=(vw, vh))
            self._background_img_scaling_info = info
            return img

    def __adjust_scene_area(self):
        w, h = self.__get_view_size()
        self.scene().setSceneRect(0, 0, w-2, h-2)

    def __get_view_size(self):
        w = self.size().width()
        h = self.size().height()
        return w, h
