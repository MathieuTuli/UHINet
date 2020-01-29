from typing import List, Tuple

import numpy as np
import cv2

from ...frontend.components import Polygon, Season


def concatenate_horizontal(images: List[np.ndarray],
                           interpolation=cv2.INTER_CUBIC) -> np.ndarray:
    h_min = min(im.shape[0] for im in images)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]),
                                      h_min), interpolation=interpolation)
                      for im in images]
    # return cv2.hconcat([image_a, image_b])
    return cv2.hconcat(im_list_resize)


def square_resize(
        img: np.ndarray,
        size: int,
        cv2_interpolation: int = cv2.INTER_AREA) -> np.ndarray:
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


def alter_area(image: np.ndarray,
               polygon: Polygon,
               season: Season) -> np.ndarray:
    return image


def diff_images(reference: np.ndarray,
                other: np.ndarray) -> Tuple[np.ndarray, float]:
    diff = reference - other
    comp = np.isclose(a=other, b=reference, rtol=0.1, atol=1e-08)
    return (diff, np.sum(comp))


def stitch(images: List[np.ndarray]) -> np.ndarray:
    return images
