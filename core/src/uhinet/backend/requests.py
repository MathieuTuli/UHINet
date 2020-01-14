from typing import Tuple

from ..frontend.components import Layer, Polygon, Orientation, Season


def getn_raw_LST() -> Layer:
    ...


def get_updated_LST() -> Layer:
    ...


def get_diff_LST() -> Layer:
    ...


def predict(polygon: Polygon,
            season: Season) -> Tuple[Layer, Layer, Layer]:
    ...
