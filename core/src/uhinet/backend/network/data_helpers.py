'''
UHINET Network Pix2Pix Data Helpers

@credit: Google (https://www.tensorflow.org/tutorials/generative/pix2pix)
'''
from pathlib import Path
from typing import Tuple, Optional, List

import tensorflow as tf
import logging

from .components import ImageDirection


# TODO : which direction , this used left to right
def load(image_path: Path,
         direction: ImageDirection) -> Tuple[tf.Tensor, tf.Tensor]:
    '''
    @returns: Tuple, (input_image, target_image)
    '''
    if not image_path.exists():
        logging.error(f"Helper - load: Image path {image_path} does not exist")
        raise

    image = tf.io.read_file(str(image_path))
    image = tf.image.decode_jpeg(image)

    w = tf.shape(image)[1]

    w = w // 2
    real_image = image[:, :w, :]
    input_image = image[:, w:, :]

    input_image = tf.cast(input_image, tf.float32)
    target_image = tf.cast(real_image, tf.float32)

    if direction == ImageDirection.AtoB:
        return input_image, target_image
    else:
        return target_image, input_image


def resize(input_image: tf.Tensor,
           real_image: tf.Tensor,
           height: int, width: int) -> Tuple[tf.Tensor, tf.Tensor]:
    input_image = tf.image.resize(
        input_image, [height, width],
        method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    real_image = tf.image.resize(
        real_image, [height, width],
        method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    return input_image, real_image


def random_crop(input_image: tf.Tensor,
                real_image: tf.Tensor,
                height: int,
                width: int) -> Tuple[tf.Tensor, tf.Tensor]:
    stacked_image = tf.stack([input_image, real_image], axis=0)
    cropped_image = tf.image.random_crop(
        stacked_image, size=[2, height, width, 3])

    return cropped_image[0], cropped_image[1]


def normalize(input_image: tf.Tensor,
              real_image: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
    input_image = (input_image / 127.5) - 1
    real_image = (real_image / 127.5) - 1

    return input_image, real_image


@tf.function()
def random_jitter(input_image: tf.Tensor,
                  real_image: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
    # Random jittering as described in the paper is to
    # 1. Resize an image to bigger height and width
    # 2. Randomnly crop to the original size
    # 3. Randomnly flip the image horizontally
    # resizing to 286 x 286 x 3
    input_image, real_image = resize(input_image, real_image, 286, 286)

    # randomly cropping to 256 x 256 x 3
    input_image, real_image = random_crop(input_image, real_image)

    if tf.random.uniform(()) > 0.5:
        # random mirroring
        input_image = tf.image.flip_left_right(input_image)
        real_image = tf.image.flip_left_right(real_image)

    return input_image, real_image


def load_image_train(image_path: Path) -> Tuple[tf.Tensor, tf.Tensor]:
    if not image_path.exists():
        logging.error(
            f"Helper - load_image_train: Image path {image_path} "
            + "does not exist")
        raise
    input_image, real_image = load(str(image_path))
    input_image, real_image = random_jitter(input_image, real_image)
    input_image, real_image = normalize(input_image, real_image)

    return input_image, real_image


def load_image_test(image_path: Path,
                    img_width: int,
                    img_height: int) -> Tuple[tf.Tensor, tf.Tensor]:
    if not image_path.exists():
        logging.error(
            f"Helper - load_image_test: Image path {image_path} "
            + "does not exist")
        raise
    input_image, real_image = load(str(image_path))
    input_image, real_image = resize(input_image, real_image,
                                     img_height, img_width)
    input_image, real_image = normalize(input_image, real_image)

    return input_image, real_image
