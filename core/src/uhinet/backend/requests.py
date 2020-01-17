from typing import Tuple
from pathlib import Path

import logging

# from TFPix2Pix import Predictor
from ..frontend.components import GISLayer, Polygon, Orientation, Season
from .data.image_formatting import alter_area, diff_images
from .data.components import BBox, ImageSize, LatLon
from .data.sentinel_hub import SentinelHubAccessor
from .file_manager import save_pyplot_image


class Requests():
    def __init__(self,
                 instance_id: str,
                 weights_file: Path) -> None:
        # self.predictor = Predictor()
        self.accessor = SentinelHubAccessor(instance_id=instance_id)

    def __str__(self) -> str:
        return 'Requests'

    def predict(self,
                polygon: Polygon,
                season: Season,
                flask_static_dir: Path) -> Tuple[GISLayer, GISLayer, GISLayer]:
        vw = polygon.viewing_window
        before_rgb = self.accessor.get_landsat_image(
                layer='SENTINEL',
                date='latest',
                image_size=ImageSize(width=1920, height=1920),
                cloud_cov_perc=0.1,
                bbox=BBox(top_left=LatLon(lat=vw.top_left.lat,
                                          lon=vw.top_left.lon),
                          bottom_right=LatLon(lat=vw.bottom_right.lat,
                                              lon=vw.bottom_right.lon)))
        if len(before_rgb) == 0:
            logging.critical(
                    'Requests: no RGB image found for those coordinates')
            raise
        before_rgb = before_rgb[0]
        after_rgb = alter_area(image=before_rgb,
                               polygon=polygon,
                               season=season)
        before_lst = before_rgb  # self.predictor.predict(before_rgb)
        after_lst = after_rgb  # self.predictor.predict(after_rgb)

        diff = diff_images(first=before_lst, second=after_lst)

        save_pyplot_image(str(flask_static_dir / 'before.png'), before_lst)
        save_pyplot_image(str(flask_static_dir / 'after.png'), after_lst)
        save_pyplot_image(str(flask_static_dir / 'diff.png'), diff)
        before_lst = GISLayer(image=Path('before.png'),
                              coordinates=polygon.viewing_window)
        after_lst = GISLayer(image=Path('after.png'),
                             coordinates=polygon.viewing_window)
        diff = GISLayer(image=Path('diff.png'),
                        coordinates=polygon.viewing_window)
        return (before_lst, after_lst, diff)
