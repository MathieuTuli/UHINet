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


class EnergyColumn(Enum):
    '''
    What the stdlib did not provide!
    '''
    ENERGY = 0
    geometry = 3
    POLY_AREA = 4

    def __str__(self):
        return self.name


class HeightColumn(Enum):
    '''
    What the stdlib did not provide!
    '''
    HEIGHT = 0
    ELEV = 1
    HEIGHT_MSL = 2
    geometry = 3
    POLY_AREA = 4

    def __str__(self):
        return self.name


class Season(Enum):
    FALL = 0
    WINTER = 1
    SPRING = 2
    SUMMER = 3

    def __str__(self):
        return self.name


class DateRange(NamedTuple):
    year: int
    season: Season
    date_from: str
    date_to: str
