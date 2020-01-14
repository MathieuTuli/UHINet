from typing import Tuple
from pathlib import Path

from TFPix2Pix import Predictor
from ..frontend.components import Layer, Polygon, Orientation, Season
from .data.sentinel_hub import SentinelHubAccessor
from .data.image_formatting import alter_area


class Requests():
    def __init__(self,
                 instance_id: Path,
                 weights_file: Path) -> None:
        self.predictor = Predictor()
        self.accessor = SentinelHubAccessor()

    def __str__(self) -> str:
        return 'Requests'

    def get_raw_LST() -> Layer:
        ...

    def get_updated_LST() -> Layer:
        ...

    def get_diff_LST() -> Layer:
        ...

    def predict(self,
                polygon: Polygon,
                season: Season) -> Tuple[Layer, Layer, Layer]:
        new_image = alter_area(polygon=polygon, season=season)
