import numpy as np
import cv2


def square_resize(img: np.ndarray, size: int, cv2_interpolation):
    '''
    @ credit: Alexey Antonenko
        https://stackoverflow.com/users/4949040/alexey-antonenko
        https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
    '''
    h, w = img.shape[:2]
    c = None if len(img.shape) < 3 else img.shape[2]
    if h == w:
        return cv2.resize(img, (size, size), cv2_interpolation)
    if h > w:
        dif = h
    else:
        dif = w
    x_pos = int((dif - w)/2.)
    y_pos = int((dif - h)/2.)
    if c is None:
        mask = np.zeros((dif, dif), dtype=img.dtype)
        mask[y_pos:y_pos+h, x_pos:x_pos+w] = img[:h, :w]
    else:
        mask = np.zeros((dif, dif, c), dtype=img.dtype)
        mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = img[:h, :w, :]
    return cv2.resize(mask, (size, size), cv2_interpolation)


def clip(width: int, height: int, channels: int):
    ...


def pad(width: int, height: int, channels: int, pad_value: float):
    ...
