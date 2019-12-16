'''
'''
from typing import Optional

import logging
import math

from .components import BBox, LatLon, ImageSize

EARTH_RADIUS = 6378.1 * 1000  # in metres


def metres_to_latitude(metres: float) -> float:
    """Returns a latitude difference from 0 to metres"""
    return (metres / EARTH_RADIUS) * (180 / math.pi)


def metres_to_longitude(latitude: float, metres: float) -> float:
    """Returns a longitude difference from 0 to metres"""
    return (metres / EARTH_RADIUS) * (180 / math.pi) / \
        math.cos(latitude * math.pi / 180.0)


def lat_lon_plus_dx_dy(lat_lon: LatLon, dx, dy) -> LatLon:
    lat = lat_lon.lat
    lon = lat_lon.lon
    lat += metres_to_latitude(dy)
    lon += metres_to_longitude(lat_lon.lat, dx)
    return LatLon(lat=lat, lon=lon)


def conform_coordinates_to_spatial_resolution(
        spatial_resolution: int,
        image_size: ImageSize,
        center: LatLon = None,
        bbox: BBox = None,) -> Optional[BBox]:
    if center is None and bbox is None:
        logging.error(
            "image_formatting: Must specify a center of bounding box")
        return None
    if bbox is not None:
        center = LatLon(lat=(bbox.top_left.lat + bbox.bottom_right.lat) / 2,
                        lon=(bbox.top_left.lon + bbox.bottom_right.lon) / 2)
    dx = (image_size.width / 2)
    dy = (image_size.height / 2) + 1
    top_left = lat_lon_plus_dx_dy(
        center,
        -dx * spatial_resolution, dy * spatial_resolution)
    bottom_right = lat_lon_plus_dx_dy(
        center,
        dx * spatial_resolution, -dy * spatial_resolution)
    return BBox(top_left=top_left, bottom_right=bottom_right)
