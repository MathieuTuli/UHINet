from typing import NamedTuple

import enum


LandsatLayer = enum.Enum(
    'LandsatLayer', ['RGB', 'LST'])


class ImageSize(NamedTuple):
    width: int
    height: int


class BBox(NamedTuple):
    '''
    Bouding Box typed annotation
    '''
    left: int
    top: int
    right: int
    bottom: int
