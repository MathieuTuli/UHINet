from typing import Tuple
from pathlib import Path

import logging

from TFPix2Pix import Predictor
from ..frontend.components import GISLayer, Polygon, Orientation, Season
from .data.image_formatting import alter_area, diff_images
from .data.components import BBox, ImageSize, LatLon
from .data.sentinel_hub import SentinelHubAccessor


class Requests():
    def __init__(self,
                 instance_id: Path,
                 weights_file: Path) -> None:
        self.predictor = Predictor()
        self.accessor = SentinelHubAccessor()

    def __str__(self) -> str:
        return 'Requests'

    def predict(self,
                polygon: Polygon,
                season: Season) -> Tuple[GISLayer, GISLayer, GISLayer]:
        vw = polygon.viewing_window
        before_rgb = self.accessor.get_landsat_image(
                layer='RGB',
                date='latest',
                image_size=ImageSize(width=None, height=None),
                cloud_cov_perc=0.1,
                bbox=BBox(top_left=LatLon(lat=vw.top_left.lat,
                                          lon=vw.top_left.lon),
                          bottom_right=LatLon(lat=vw.bottom_right.lat,
                                              lon=vw.bottom_right.lon)))
        if before_rgb is None:
            logging.critical(
                    'Requests: no RGB image found for those coordinates')
            raise
        after_rgb = alter_area(image=before_rgb,
                               polygon=polygon,
                               season=season)
        before_lst = self.predictor.predict(before_rgb)
        after_lst = self.predictor.predict(after_rgb)

        diff = diff_images(first=before_lst, second=after_lst)

        before_lst = GISLayer(image=before_lst,
                              coordinates=polygon.viewing_window)
        after_lst = GISLayer(image=after_lst,
                             coordinates=polygon.viewing_window)
        diff = GISLayer(image=diff, coordinates=polygon.viewing_window)
        return (before_lst, after_lst, diff)
