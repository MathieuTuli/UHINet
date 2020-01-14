from typing import Tuple

from ..frontend.components import Layer


def getn_raw_LST() -> Layer:
    ...


def get_updated_LST() -> Layer:
    ...


def get_diff_LST() -> Layer:
    ...


def predict() -> Tuple[Layer, Layer, Layer]:
    ...
