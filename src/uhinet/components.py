from typing import NamedTuple

import enum


LandsatLayer = enum.Enum(
    'LandsatLayer', ['RGB', 'LST'])


class ImageSize(NamedTuple):
    width: int
    height: int


class LatLon(NamedTuple):
    '''
    Bouding Box typed annotation
    '''
    lat: int
    lon: int


class BBox(NamedTuple):
    '''
    Bouding Box typed annotation
    '''
    top_left: LatLon
    bottom_right: LatLon
