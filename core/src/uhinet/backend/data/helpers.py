'''
'''
from typing import Optional, List

import datetime
import calendar
import logging
import math
import re

from .components import BBox, LatLon, ImageSize, DateRange, Season

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
    """
    if both center and bbox are specified, bbox will be used
    """
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


def get_seasons(year_from: int,
                year_to: int) -> List[DateRange]:
    seasons = []
    for year in range(year_from, year_to + 1):
        feb_day = calendar.monthrange(year, 2)[1]
        seasons.append(DateRange(
            year=year,
            season=Season.WINTER,
            date_from=f"{year-1}-12-01",
            date_to=f"{year}-02-{feb_day}"))
        seasons.append(DateRange(
            year=year,
            season=Season.SPRING,
            date_from=f"{year}-03-01",
            date_to=f"{year}-05-31"))
        seasons.append(DateRange(
            year=year,
            season=Season.SUMMER,
            date_from=f"{year}-06-01",
            date_to=f"{year}-08-31"))
        seasons.append(DateRange(
            year=year,
            season=Season.FALL,
            date_from=f"{year}-09-01",
            date_to=f"{year}-11-30"))
    return seasons
