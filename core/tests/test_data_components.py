from uhinet.backend.data.components import LatLon, ImageSize, BBox
from support import fail_if


def test_lat_lon():
    ll = LatLon(lat=10, lon=10)
    fail_if(ll.lat != 10 or ll.lon != 10)


def test_image_size():
    img = ImageSize(width=10, height=10)
    fail_if(img.width != 10 or img.height != 10)


def test_bbox():
    bbox = BBox(top_left=LatLon(lat=0, lon=0),
                bottom_right=LatLon(lat=10, lon=10))
    fail_if(bbox.top_left.lat != 0 or bbox.top_left.lon != 0)
    fail_if(bbox.bottom_right.lat != 10 or bbox.bottom_right.lon != 10)
