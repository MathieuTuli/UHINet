from typing import NamedTuple
from enum import Enum


class ImageSize(NamedTuple):
    width: int
    height: int


class LatLon(NamedTuple):
    '''
    Bouding Box typed annotation
    '''
    lat: float
    lon: float


class BBox(NamedTuple):
    '''
    Bouding Box typed annotation
    '''
    top_left: LatLon
    bottom_right: LatLon


class Column(Enum):
    '''
    What the stdlib did not provide!
    '''
    HEIGHT = 0
    ELEV = 1
    HEIGHT_ELEV = 2

    def __str__(self):
        return self.name
