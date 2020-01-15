from typing import Tuple
from pathlib import Path

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
        before_rgb = self.accessor.get_landsat_image(
                layer='RGB',
                date=None,
                image_size=ImageSize(width=None, height=None),
                cloud_cov_perc=None,
                bbox=BBox(top_left=LatLon(lat=None, lon=None),
                          bottom_right=LatLon(lat=None, lon=None)))
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
