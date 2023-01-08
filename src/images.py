# Author: Seunghyun Kim

import cv2
import numpy as np


class SourceSizeGraterThanTargetSizeError(Exception):
    def __init__(self):
        msg = "Width and height of the target_size must be " \
            + "greater than that of the input_size."
        super().__init__(msg)


def fit_input_size_to_stride(input_size, stride):
    """ Fit the input_size to multiple of the stride.
    Args:
        input_size(list-like, [int, int]): width, height
        stride(int):
    Returns:
        output_size(tuple, (int, int)): width, height
    """
    def fit(x):
        if x % stride:
            x = x - (x % stride) + stride
        return x

    w, h = input_size
    output_size = fit(w), fit(h)
    return output_size


def calc_scale_factors_between(source_size, target_size):
    """ Get scale factors for scaling the source_size to the target_size.
    Args:
        source_size(list-like, [int, int]): width, height
        target_size(list-like, [int, int]): width, height
    Returns:
        scale_factors(tuple, (float, float)):
    """
    w1, h1 = source_size
    w2, h2 = target_size

    rw = w2 / w1  # ratio
    rh = h2 / h1

    scale_factors = rw, rh
    return scale_factors


def calc_gaps_between(source_size, target_size):
    """ Get gaps between source_size and target_size.
    Args:
        source_size(list-like, [int, int]): width, height
        target_size(list-like, [int, int]): width, height
    Returns:
        gaps(dict): {'top':top, 'bottom':bottom, 'left':left, 'right':right}
    Raise:
        SourceSizeGraterThanTargetSizeError
    """
    w1, h1 = source_size
    w2, h2 = target_size
    if w1 > w2 or h1 > h2:
        raise SourceSizeGraterThanTargetSizeError

    half_w = (w2 - w1) / 2
    half_h = (h2 - h1) / 2

    top = int(round(half_h - 0.1)) 
    bottom = int(round(half_h + 0.1))
    left = int(round(half_w - 0.1))
    right = int(round(half_w + 0.1))

    gaps = {'top':top, 'bottom':bottom, 'left':left, 'right':right}
    return gaps


def add_borders_to(img, thickness, rgb_color=(0,0,0)):
    """ Add borders to the image.
    Args:
        img(numpy.ndarray): image matrix
        thickness(list-like, [int, int, int, int]): top, bottom, left, right
        rgb_color(list-like, [int, int, int]):
    Returns:
        bordered_img(numpy.ndarray): bordered image matrix
    """
    border_type = cv2.BORDER_CONSTANT
    top, bottom, left, right = thickness

    bordered_img = cv2.copyMakeBorder(
        img, top, bottom, left, right,
        border_type, value=rgb_color)
    return bordered_img


def resize(img, scale_factors):
    """ Resize the image using scale_factors.
    Args:
        img(numpy.ndarray): image matrix
        scale_factors(list-like, [float, float]):
    Returns:
        resized_img(numpy.ndarray):
    """
    source_size = np.array(img.shape[:2][::-1])
    target_size = np.round(source_size * scale_factors).astype(int)

    resized_img = cv2.resize(img, target_size)
    return resized_img


def resize_keeping_aspect_ratio(img, target_size, stride=None):
    # NEED REFACTORING!
    """ Resize the image to the target_size keeping aspect ratio.
    Args:
        img(numpy.ndarray): image matrix
        target_size(list-like, [int, int]): width, height
        stride(int): option for deep learning
    Returns:
        resized_img(numpy.ndarray): resized image matrix
        resize_info(dict):
    """
    if stride is not None:
        target_size = fit_input_size_to_stride(target_size, stride)

    # resize img
    source_size = img.shape[:2][::-1]  # (w, h)
    scale_factors = calc_scale_factors_between(source_size, target_size)
    scale_factors = (min(scale_factors),) * 2
    resized_img = resize(img, scale_factors)

    # add letterbox(or pillarbox) for keeping aspect ratio
    resized_size = resized_img.shape[:2][::-1]
    gaps = calc_gaps_between(resized_size, target_size)
    bordered_resized_img = add_borders_to(
        resized_img,
        [gaps['top'], gaps['bottom'], gaps['left'], gaps['right']])

    resize_info = {
        "scale_factors": scale_factors,
        "diff_origin": (gaps['left'], gaps['top'])}

    return bordered_resized_img, resize_info


def get_empty_img(shape, brightness):
    """ Return an empty image.
    Args:
        shape(list-like, [int, int, int]): height, width, channel
        width(int):
        height(int):
        channel(int): 1(gray) or 3(rgb)
        brightness(int): 0 ~ 255
    Returns:
        (numpy.ndarray):
    """
    _, _, c = shape
    if not (c == 1 or c == 3):
        msg = "channel is not 1 or 3."
        raise ValueError(msg)
    if not (0 <= brightness and brightness < 256):
        msg = "brightness must be: 0 <= value < 256"
        raise ValueError(msg)
    return np.ones(shape, dtype=np.uint8) * brightness
