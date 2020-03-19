from typing import Tuple
from pathlib import Path

import datetime
import io

import tensorflow as tf
import numpy as np
import matplotlib
import logging
import cv2

# from TFPix2Pix.predictor import Predictor
from geopandas import GeoDataFrame
from PIL import Image
import torch

from ..frontend.components import GISLayer, Polygon, Season, BuildingType
from .data.helpers import conform_coordinates_to_spatial_resolution
from .data.image_formatting import alter_area, diff_images, \
    square_resize
from .data.map_from_geopandas import ax_from_frame, array_from_ax
from .data.components import ImageSize, LatLon, HeightColumn, \
    EnergyColumn, BBox
from .data.sentinel_hub import SentinelHubAccessor
from .file_manager import save_pyplot_image

from .pytorch_pix2pix.options.test_options import TestOptions
from .pytorch_pix2pix.models import create_model
from .pytorch_pix2pix.data import base_dataset
from .pytorch_pix2pix.util.util import tensor2im


def get_latest_summer():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    if month < 8:
        year -= 1
    return [f"{year}-06-01", f"{year}-08-31"]


class Predictor():
    def __init__(self,
                 opts,
                 input_shape=Tuple[int, int, int]):
        self.model = create_model(opts)
        self.model.setup(opts)
        self.model.eval()
        self.transform = base_dataset.get_transform(opts, grayscale=False)

    def predict(self, input_image: np.ndarray):
        data = {'A': torch.unsqueeze(torch.tensor(self.transform(
            Image.fromarray(input_image).convert('RGB'))), axis=0),
            'B': torch.unsqueeze(torch.tensor(self.transform(
                Image.fromarray(input_image).convert('RGB'))), axis=0),
            'A_paths': Path(''),
            'B_paths': Path('')}
        self.model.set_input(data)
        self.model.test()
        image = self.model.get_current_visuals()
        return tensor2im(image['fake_B'])


class Requests():
    def __init__(self,
                 instance_id: str,
                 flask_static_dir: Path,) -> None:
        # height_shp_file: Path,
        # energy_shp_file: Path) -> None:
        opts = TestOptions().parse()
        opts.num_threads = 0
        opts.batch_size = 1
        opts.serial_batches = True
        opts.no_flip = True
        opts.display_id = -1
        opts.name = 'uhinet_pix2pix'
        opts.model = 'pix2pix'
        opts.checkpoints_dir = 'data/checkpoints'
        self.predictor = Predictor(opts=opts,
                                   input_shape=(256, 256, 3))

        self.accessor = SentinelHubAccessor(instance_id=instance_id)
        self.flask_static_dir = flask_static_dir
        # self.height_frame = GeoDataFrame.from_file(str(height_shp_file))
        # self.height_frame = self.height_frame.sort_values(by=str('HEIGHT'))
        # self.height_fig, self.height_ax = ax_from_frame(
        #     frame=self.height_frame,
        #     size=ImageSize(width=512, height=512),
        #     column=HeightColumn.HEIGHT_MSL,
        #     sort_by=HeightColumn.HEIGHT_MSL,
        #     cmap='Greens')
        # self.height_norm = matplotlib.colors.Normalize(
        #     vmin=self.height_frame['HEIGHT_MSL'].min(),
        #     vmax=self.height_frame['HEIGHT_MSL'].max())
        # self.height_color = matplotlib.cm.get_cmap('Greens')
        self.count = 0
        # self.energy_frame = GeoDataFrame.from_file(str(height_shp_file))
        # self.energy_frame = self.energy_frame.sort_values(by=str('ENERGY'))

    def __str__(self) -> str:
        return 'Requests'

    def predict(self,
                polygon: Polygon,
                season: Season,
                height: float,
                energy: float) -> Tuple[GISLayer, GISLayer, GISLayer]:
        if polygon.building_type == BuildingType.GREEN_SPACE or \
                polygon.building_type == BuildingType.PARKING_LOT:
            height = 0
        center_lat = np.mean([coord.lat for coord in polygon.coordinates])
        center_lon = np.mean([coord.lon for coord in polygon.coordinates])
        new_coords = conform_coordinates_to_spatial_resolution(
            spatial_resolution=5,
            image_size=ImageSize(width=512, height=512),
            center=LatLon(lat=center_lat,
                          lon=center_lon))
        images = []
        print(get_latest_summer())
        for layer in ['RGB', 'LST']:
            images.append(self.accessor.get_landsat_image(
                layer=layer,
                date=get_latest_summer(),
                image_size=ImageSize(width=512, height=512),
                cloud_cov_perc=0.1,
                bbox=new_coords))
        before_rgb, before_lst = images
        if len(before_rgb) == 0:
            logging.critical(
                'Requests: no RGB image found for those coordinates')
            raise
        before_rgb = before_rgb[0]
        before_lst = before_lst[0]
        matplotlib.use('agg')
        # TODO fix this
        after_rgb = alter_area(image=before_rgb,
                               polygon=polygon.coordinates,
                               window=new_coords,
                               building_type=polygon.building_type,
                               season=season)
        # before_rgb_tensor = tf.expand_dims((tf.image.resize(
        #     images=tf.convert_to_tensor(
        #         value=square_resize(before_rgb, 512, cv2.INTER_AREA),
        #         dtype=tf.float32),
        #     size=[256, 256],
        #     method=tf.image.ResizeMethod.NEAREST_NEIGHBOR) / 127.5) - 1,
        #     axis=0)
        before_rgb_tensor = cv2.resize(
            before_rgb, (512, 512), interpolation=cv2.INTER_NEAREST)
        # before_lst_tensor = tf.expand_dims((tf.image.resize(
        #     images=tf.convert_to_tensor(
        #         value=square_resize(before_lst, 512, cv2.INTER_AREA),
        #         dtype=tf.float32),
        #     size=[256, 256],
        #     method=tf.image.ResizeMethod.NEAREST_NEIGHBOR) / 127.5) - 1,
        #     axis=0)
        # after_rgb_tensor = tf.expand_dims((tf.image.resize(
        #     images=tf.convert_to_tensor(
        #         value=square_resize(after_rgb, 512, cv2.INTER_AREA),
        #         dtype=tf.float32),
        #     size=[256, 256],
        #     method=tf.image.ResizeMethod.NEAREST_NEIGHBOR) / 127.5) - 1,
        #     axis=0)
        after_rgb_tensor = cv2.resize(
            after_rgb, (512, 512), interpolation=cv2.INTER_NEAREST)
        # before_height=array_from_ax(self.height_fig, self.height_ax,
        #                               new_coords)
        # save_pyplot_image(
        #     image_name = str(self.flask_static_dir /
        #                    f'{self.count}_before_height.png'),
        #     image = before_height)
        # self.height_ax.add_patch(
        #     matplotlib.pyplot.Polygon(
        #         [(c.lon, c.lat) for c in polygon.coordinates],
        #         fill=True, edgecolor=None,
        #         color=self.height_color(self.height_norm(height))))
        # after_height=array_from_ax(self.height_fig, self.height_ax,
        #                              new_coords)
        # before_energy = self.generate_energy_map(bbox=new_coords)
        before_predicted_lst = self.predictor.predict(
            before_rgb_tensor)
        after_predicted_lst = self.predictor.predict(after_rgb_tensor)

        diff, val = diff_images(
            reference=before_predicted_lst, other=after_predicted_lst)

        save_pyplot_image(
            image_name=str(self.flask_static_dir /
                           f'{self.count}_before_lst.png'),
            image=before_predicted_lst)
        save_pyplot_image(
            str(self.flask_static_dir / f'{self.count}_after_lst.png'),
            image=after_predicted_lst)
        save_pyplot_image(
            image_name=str(self.flask_static_dir / f'{self.count}_diff.png'),
            image=diff if polygon.building_type == BuildingType.GREEN_SPACE else -diff,
            cmap='bwr',
            vmin=0,
            vmax=255)
        save_pyplot_image(
            image_name=str(self.flask_static_dir /
                           f'{self.count}_before_rgb.png'),
            image=before_rgb)
        save_pyplot_image(
            image_name=str(self.flask_static_dir /
                           f'{self.count}_after_rgb.png'),
            image=after_rgb)
        # save_pyplot_image(
        #     image_name = str(self.flask_static_dir /
        #                    f'{self.count}_after_height.png'),
        #     image = after_height)
        # save_pyplot_image(
        #     image_name=str(self.flask_static_dir / 'before_energy.png'),
        #     image=before_energy)
        before_lst = GISLayer(image=Path(f'{self.count}_before_lst.png'),
                              coordinates=new_coords)
        after_lst = GISLayer(image=Path(f'{self.count}_after_lst.png'),
                             coordinates=new_coords)
        diff = GISLayer(image=Path(f'{self.count}_diff.png'),
                        coordinates=new_coords)
        self.count += 1
        return (before_lst, after_lst, diff)
