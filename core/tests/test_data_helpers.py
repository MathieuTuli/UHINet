from uhinet.backend.data.helpers import metres_to_latitude, \
    metres_to_longitude, lat_lon_plus_dx_dy, \
    conform_coordinates_to_spatial_resolution
from uhinet.backend.data.components import LatLon, ImageSize
from support import fail_if


def test_metres_to_latitude():
    metres = 10
    metres_to_latitude(metres=metres)


def test_metres_to_longitude():
    metres = 10
    metres_to_longitude(latitude=40, metres=metres)


def test_lat_long_plus_dx_dy():
    lat_lon_plus_dx_dy(LatLon(lat=40, lon=-70), dx=10, dy=10)


def test_conform_coordinates_to_spatial_resolution():
    conform_coordinates_to_spatial_resolution(
        spatial_resolution=30,
        image_size=ImageSize(width=256, height=256),
        center=LatLon(lat=40, lon=-70),)
    fail_if(conform_coordinates_to_spatial_resolution(
        spatial_resolution=30,
        image_size=ImageSize(width=256, height=256),) is not None)
