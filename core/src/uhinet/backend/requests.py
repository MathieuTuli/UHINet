from typing import Tuple
from pathlib import Path

import tensorflow as tf
import matplotlib
import logging
import cv2

from TFPix2Pix.predictor import Predictor
from ..frontend.components import GISLayer, Polygon, Orientation, Season
from .data.helpers import conform_coordinates_to_spatial_resolution
from .data.image_formatting import alter_area, diff_images, \
    concatenate_horizontal, square_resize
from .data.components import BBox, ImageSize, LatLon
from .data.sentinel_hub import SentinelHubAccessor
from .file_manager import save_pyplot_image


class Requests():
    def __init__(self,
                 instance_id: str,
                 winter_weights_file: Path,
                 spring_weights_file: Path,
                 summer_weights_file: Path,
                 fall_weights_file: Path) -> None:
        self.predictors = {
            Season.WINTER: Predictor(weights=winter_weights_file,
                                     input_shape=(256, 256, 3)),
            Season.SPRING: Predictor(weights=spring_weights_file,
                                     input_shape=(256, 256, 3)),
            Season.SUMMER: Predictor(weights=summer_weights_file,
                                     input_shape=(256, 256, 3)),
            Season.FALL: Predictor(weights=fall_weights_file,
                                   input_shape=(256, 256, 3))}

        self.accessor = SentinelHubAccessor(instance_id=instance_id)

    def __str__(self) -> str:
        return 'Requests'

    def predict(self,
                polygon: Polygon,
                season: Season,
                flask_static_dir: Path) -> Tuple[GISLayer, GISLayer, GISLayer]:
        ceter_lat = 0
        ceter_lon = 0
        for coord in polygon.coordinates:
            ceter_lat += coord.lat
            ceter_lon += coord.lon
        ceter_lat /= len(polygon.coordinates)
        ceter_lon /= len(polygon.coordinates)
        new_coords = conform_coordinates_to_spatial_resolution(
            spatial_resolution=5,
            image_size=ImageSize(width=512, height=512),
            center=LatLon(lat=ceter_lat,
                          lon=ceter_lon))
        images = []
        for layer in ['RGB', 'LST']:
            images.append(self.accessor.get_landsat_image(
                layer=layer,
                date='latest',
                image_size=ImageSize(width=512, height=512),
                cloud_cov_perc=0.1,
                bbox=new_coords))
        before_rgb, before_lst = images
        matplotlib.use('agg')
        # TODO fix this
        if len(before_rgb) == 0:
            logging.critical(
                'Requests: no RGB image found for those coordinates')
            raise
        before_rgb = tf.expand_dims((tf.image.resize(
            images=tf.convert_to_tensor(
                value=square_resize(before_rgb[0], 512, cv2.INTER_AREA),
                dtype=tf.float32),
            size=[256, 256],
            method=tf.image.ResizeMethod.NEAREST_NEIGHBOR) / 127.5) - 1,
            axis=0)
        before_lst = tf.expand_dims((tf.image.resize(
            images=tf.convert_to_tensor(
                value=square_resize(before_lst[0], 512, cv2.INTER_AREA),
                dtype=tf.float32),
            size=[256, 256],
            method=tf.image.ResizeMethod.NEAREST_NEIGHBOR) / 127.5) - 1,
            axis=0)
        after_rgb = alter_area(image=before_rgb,
                               polygon=polygon,
                               season=season)
        # test_image = concatenate_horizontal([before_rgb, before_lst])
        # save_to = flask_static_dir / 'test_image.png'
        # save_pyplot_image(str(save_to), test_image)
        before_predicted_lst = self.predictors[season].predict(before_rgb)
        # save_to = flask_static_dir / 'after_rgb.png'
        # save_pyplot_image(str(save_to), after_rgb)
        after_predicted_lst = self.predictors[season].predict(after_rgb)

        # TODO dtype from predictor create black images
        diff, val = diff_images(
            reference=before_predicted_lst, other=after_predicted_lst)

        save_pyplot_image(str(flask_static_dir / 'before.png'),
                          before_predicted_lst)
        save_pyplot_image(str(flask_static_dir / 'after.png'),
                          after_predicted_lst)
        save_pyplot_image(str(flask_static_dir / 'diff.png'), diff,
                          cmap='coolwarm')
        before_lst = GISLayer(image=Path('before.png'),
                              coordinates=new_coords)
        after_lst = GISLayer(image=Path('after.png'),
                             coordinates=new_coords)
        diff = GISLayer(image=Path('diff.png'),
                        coordinates=new_coords)
        return (before_lst, after_lst, diff)
