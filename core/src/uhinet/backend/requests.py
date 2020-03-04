from typing import Tuple
from pathlib import Path

import io

import tensorflow as tf
import numpy as np
import matplotlib
import logging
import cv2

from TFPix2Pix.predictor import Predictor
from geopandas import GeoDataFrame

from ..frontend.components import GISLayer, Polygon, Season
from .data.helpers import conform_coordinates_to_spatial_resolution
from .data.image_formatting import alter_area, diff_images, \
    square_resize
from .data.map_from_geopandas import ax_from_frame, array_from_ax
from .data.components import ImageSize, LatLon, HeightColumn, \
    EnergyColumn, BBox
from .data.sentinel_hub import SentinelHubAccessor
from .file_manager import save_pyplot_image


class Requests():
    def __init__(self,
                 instance_id: str,
                 winter_weights_file: Path,
                 spring_weights_file: Path,
                 summer_weights_file: Path,
                 fall_weights_file: Path,
                 flask_static_dir: Path,
                 height_shp_file: Path,
                 energy_shp_file: Path) -> None:
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
        self.flask_static_dir = flask_static_dir
        self.height_frame = GeoDataFrame.from_file(str(height_shp_file))
        self.height_frame = self.height_frame.sort_values(by=str('HEIGHT'))
        self.height_fig, self.height_ax = ax_from_frame(
            frame=self.height_frame,
            size=ImageSize(width=512, height=512),
            column=HeightColumn.HEIGHT,
            sort_by=HeightColumn.HEIGHT)
        # self.energy_frame = GeoDataFrame.from_file(str(height_shp_file))
        # self.energy_frame = self.energy_frame.sort_values(by=str('ENERGY'))

    def __str__(self) -> str:
        return 'Requests'

    def predict(self,
                polygon: Polygon,
                season: Season) -> Tuple[GISLayer, GISLayer, GISLayer]:
        center_lat = np.mean([coord.lat for coord in polygon.coordinates])
        center_lon = np.mean([coord.lon for coord in polygon.coordinates])
        new_coords = conform_coordinates_to_spatial_resolution(
            spatial_resolution=5,
            image_size=ImageSize(width=512, height=512),
            center=LatLon(lat=center_lat,
                          lon=center_lon))
        images = []
        for layer in ['RGB', 'LST']:
            images.append(self.accessor.get_landsat_image(
                layer=layer,
                date='latest',
                image_size=ImageSize(width=512, height=512),
                cloud_cov_perc=0.1,
                bbox=new_coords))
        before_rgb, before_lst = images
        before_rgb = before_rgb[0]
        before_lst = before_lst[0]
        matplotlib.use('agg')
        # TODO fix this
        if len(before_rgb) == 0:
            logging.critical(
                'Requests: no RGB image found for those coordinates')
            raise
        after_rgb = alter_area(image=before_rgb,
                               polygon=polygon.coordinates,
                               window=new_coords,
                               building_type=polygon.building_type,
                               season=season)
        before_rgb_tensor = tf.expand_dims((tf.image.resize(
            images=tf.convert_to_tensor(
                value=square_resize(before_rgb, 512, cv2.INTER_AREA),
                dtype=tf.float32),
            size=[256, 256],
            method=tf.image.ResizeMethod.NEAREST_NEIGHBOR) / 127.5) - 1,
            axis=0)
        before_lst_tensor = tf.expand_dims((tf.image.resize(
            images=tf.convert_to_tensor(
                value=square_resize(before_lst, 512, cv2.INTER_AREA),
                dtype=tf.float32),
            size=[256, 256],
            method=tf.image.ResizeMethod.NEAREST_NEIGHBOR) / 127.5) - 1,
            axis=0)
        after_rgb_tensor = tf.expand_dims((tf.image.resize(
            images=tf.convert_to_tensor(
                value=square_resize(after_rgb, 512, cv2.INTER_AREA),
                dtype=tf.float32),
            size=[256, 256],
            method=tf.image.ResizeMethod.NEAREST_NEIGHBOR) / 127.5) - 1,
            axis=0)
        before_height = array_from_ax(self.height_fig, self.height_ax,
                                      new_coords)
        # before_energy = self.generate_energy_map(bbox=new_coords)
        before_predicted_lst = self.predictors[season].predict(
            before_rgb_tensor)
        after_predicted_lst = self.predictors[season].predict(after_rgb_tensor)

        diff, val = diff_images(
            reference=before_predicted_lst, other=after_predicted_lst)

        save_pyplot_image(
            image_name=str(self.flask_static_dir / 'before_lst.png'),
            image=before_predicted_lst)
        save_pyplot_image(
            str(self.flask_static_dir / 'after_lst.png'),
            image=after_predicted_lst)
        save_pyplot_image(
            image_name=str(self.flask_static_dir / 'diff.png'),
            image=diff,
            cmap='coolwarm')
        save_pyplot_image(
            image_name=str(self.flask_static_dir / 'before_rgb.png'),
            image=before_rgb)
        save_pyplot_image(
            image_name=str(self.flask_static_dir / 'after_rgb.png'),
            image=after_rgb)
        save_pyplot_image(
            image_name=str(self.flask_static_dir / 'before_height.png'),
            image=before_height)
        # save_pyplot_image(
        #     image_name=str(self.flask_static_dir / 'before_energy.png'),
        #     image=before_energy)
        before_lst = GISLayer(image=Path('before_lst.png'),
                              coordinates=new_coords)
        after_lst = GISLayer(image=Path('after_lst.png'),
                             coordinates=new_coords)
        diff = GISLayer(image=Path('diff.png'),
                        coordinates=new_coords)
        return (before_lst, after_lst, diff)
