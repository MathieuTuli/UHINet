from typing import List, Tuple

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2

from .components import BBox, LatLon
from ..file_manager import save_pyplot_image
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
    window = polygon.viewing_window
    shape = image.shape
    lat_ratio = (window.bottom_right.lat - window.top_left.lat) / shape[0]  # h
    lon_ratio = (window.bottom_right.lon - window.top_left.lon) / shape[1]  # w
    new_polygon = np.array([[int(coord.lon * lon_ratio),
                             int(coord.lat * lat_ratio)]
                            for coord in polygon.coordinates])
    replace_with = cv2.imread(
        f"data/alter-images/{str(season)}_{str(polygon.building_type)}")

    # create mask
    # width = np.max(new_polygon[:, 0]) - np.min(new_polygon[:, 0])
    # height = np.max(new_polygon[:, 1]) - np.min(new_polygon[:, 1])
    # import math
    # num_concat_w = math.ceil(width / replace_with.shape[1])
    # num_concat_h = math.ceil(height / replace_with.shape[0])
    num_concat_w = math.ceil(image.shape[1] / replace_with.shape[1])
    num_concat_h = math.ceil(image.shape[0] / replace_with.shape[0])
    replace_with = cv2.hconcat([replace_with] * num_concat_w)
    replace_with = cv2.resize(cv2.vconcat(
        [replace_with] * num_concat_h), image.shape)
    mask = np.zeros(replace_with.shape[:2], np.uint8)
    cv2.fillPoly(mask, new_polygon, (255, 255, 255))
    replace_with = cv2.bitwise_and(replace_with, replace_with, mask=mask)
    for row in image.shape[0]:
        for col in image.shape[1]:
            for channel in image.shape[2]:
                if replace_with[row, col, channel] != 0:
                    image[row, col, channel] = replace_with[row, col, channel]
    return image


def diff_images(reference: np.ndarray,
                other: np.ndarray) -> Tuple[np.ndarray, float]:
    '''
    @credit: http://www.pmavridis.com/misc/heatmaps/
    '''
    # diff = reference - other
    # comp = np.isclose(a=other, b=reference, rtol=0.1, atol=1e-08)
    # return (diff, np.sum(comp))
    fig, ax = plt.subplots()
    error_r = np.fabs(np.subtract(
        reference[:, :, 0].astype(np.int16),
        other[:, :, 0].astype(np.int16))).astype(np.float16)
    error_g = np.fabs(np.subtract(
        reference[:, :, 1].astype(np.int16),
        other[:, :, 1].astype(np.int16))).astype(np.float16)
    error_b = np.fabs(np.subtract(
        reference[:, :, 2].astype(np.int16),
        other[:, :, 2].astype(np.int16))).astype(np.float16)
    int_error_r = np.fabs(np.subtract(
        reference[:, :, 0],
        other[:, :, 0]))
    int_error_g = np.fabs(np.subtract(
        reference[:, :, 1],
        other[:, :, 1]))
    int_error_b = np.fabs(np.subtract(
        reference[:, :, 2],
        other[:, :, 2]))

    # Calculate the maximum error for each pixel
    lum_img = np.maximum(np.maximum(int_error_r, int_error_g), int_error_b)

    # Uncomment the next line to turn the colors upside-down
    # lum_img = np.negative(lum_img)

    error = error_r + error_g + error_b
    shape = error.shape
    error /= (shape[0] * shape[1])
    error = np.sum(error)
    return (lum_img.astype(np.uint8), error / 255 / 3)
    # img_plot = plt.imshow(lum_img)

    # # Choose a color palette
    # img_plot.set_cmap('jet')
    # # imgplot.set_cmap('Spectral')

    # plt.colorbar()
    # plt.axis('off')
    # plt.show()


def stitch(images: List[np.ndarray]) -> np.ndarray:
    return images


if __name__ == "__main__":
    ref = mpimg.imread(
        '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/cloud_free_testings/images/102-targets.png')
    other = mpimg.imread(
        '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/cloud_free_testings/images/102-outputs.png')
    plt.imshow(ref)
    plt.show()
    plt.imshow(other)
    plt.show()
    diff = diff_images(ref, other)
    save_pyplot_image('test.png', diff, cmap='jet', colorbar=False)
