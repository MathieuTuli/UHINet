from typing import NamedTuple, List, Union
from pathlib import Path
from enum import Enum
import numpy as np

from ..backend.data.components import BBox, LatLon


class BuildingType(Enum):
    '''
    Names can be changed
    Caution: If you change names here, you also need to change
             frontend/run.py where the names are called
    '''
    RESIDENTIAL = 0
    COMMERCIAL = 1
    GREEN_SPACE = 2
    PARKING_LOT = 3

    def __str__(self):
        return self.name


class Season(Enum):
    FALL = 0
    WINTER = 1
    SPRING = 2
    SUMMER = 3

    def __str__(self):
        return self.name


class Orientation(Enum):
    '''
    Just an enum to define the orientation of the polygon coordinates
    use like -> orientation = Orientation.CCW
    '''
    CCW = 0
    CW = 1

    def __str__(self):
        return self.name


class GISLayer(NamedTuple):
    '''
    A layer to display on the map. The image is either
    a numpy array or a Path to an image file.

    NameTuples are immutable, meaning once created, you can't change
    their values, only access them. So, you would create it like

    layer = Layer(image=..., coordinates=...)
    and then access it like layer.image or layer.coordinates.

    note that there is a weird behaviour if you create a variable
    and then assign to to a member of a NamedTuple.
    ie. don't do bbox = BBox(top_left=LatLon(lat=..., lon=...),
                             bottom_right=LatLon(lat=..., lon=...))

            then layer = Layer(image=..., coordinates=bbox)

            do
            layer = Layer(
                image=...,
                coordinates=BBox(
                        top_left=LatLon(lat=..., lon=...),
                        bottom_right=LatLon(lat=..., lon=...)))


        and to that extent, don't do

            tl = LatLon(lat=..., lon=...)
            br = LatLon(lat=..., lon=...)
            BBox(top_left=tl,
                 bottom_right=br)
    '''
    image: Path
    coordinates: BBox


class Polygon(NamedTuple):
    '''
    Nothing new here that you can't learn from above
    use as

    polygon = Polygon(coordinates=[LatLon(lat=..., lon=...),
                                   LatLon(lat=..., lon=...),
                                   LatLon(lat=..., lon=...),
                                   ...],
                      orientation=Orientation.CWW) // or CW
    '''
    coordinates: List[LatLon]
    viewing_window: BBox
    orientation: Orientation
    building_type: BuildingType
