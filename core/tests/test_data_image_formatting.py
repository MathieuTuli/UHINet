from pathlib import Path

import cv2

from uhinet.backend.data.image_formatting import concatenate_horizontal, \
    square_resize, clip, pad
from uhinet.backend.data.components import LatLon, ImageSize
from support import fail_if


def test_concatenate_horizontal():
    images_dir = Path.cwd() / 'tests/images'
    fail_if(not images_dir.exists())
    image_left = cv2.imread(str(images_dir / '1_2_RGB_img_0.png'))
    image_right = cv2.imread(str(images_dir / '1_2_LST_img_0.png'))
    fail_if(image_left is None)
    fail_if(image_right is None)
    h1, w1, c1 = image_left.shape
    h2, w2, c2 = image_right.shape
    fail_if(h1 != h2 or w1 != w2 or c1 != c2)

    img = concatenate_horizontal([image_left, image_right])
    h, w, c = img.shape
    fail_if(h != h1 or h != h2)
    fail_if(w != w1 + w2)
    fail_if(c != c1 or c != c2)


def test_square_resize():
    images_dir = Path.cwd() / 'tests/images'
    fail_if(not images_dir.exists())
    image = cv2.imread(str(images_dir / '1_2_RGB_img_0.png'))
    fail_if(image is None)
    size = 50
    img = square_resize(image, size)
    h, w, c = img.shape
    fail_if(h != size or w != size or c != image.shape[2])


def test_clip():
    clip(0, 0, 0)


def test_pad():
    pad(0, 0, 0, 0)
