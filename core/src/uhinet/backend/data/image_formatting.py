from typing import List, Tuple

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
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
    '''
    @credit: http://www.pmavridis.com/misc/heatmaps/
    '''
    # diff = reference - other
    # comp = np.isclose(a=other, b=reference, rtol=0.1, atol=1e-08)
    # return (diff, np.sum(comp))
    error_r = np.fabs(np.subtract(reference[:, :, 0], other[:, :, 0]))
    error_g = np.fabs(np.subtract(reference[:, :, 1], other[:, :, 1]))
    error_b = np.fabs(np.subtract(reference[:, :, 2], other[:, :, 2]))

    # Calculate the maximum error for each pixel
    lum_img = np.maximum(np.maximum(error_r, error_g), error_b)

    # Uncomment the next line to turn the colors upside-down
    lum_img = np.negative(lum_img)

    imgplot = plt.imshow(lum_img)

    # Choose a color palette
    imgplot.set_cmap('jet')
    # imgplot.set_cmap('Spectral')

    plt.colorbar()
    plt.axis('off')

    plt.show()


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
    diff, val = diff_images(ref, other)
