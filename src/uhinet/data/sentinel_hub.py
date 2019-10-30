from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox, \
    WebFeatureService, BBox, CRS, DataSource, get_area_info
from sentinelhub import CustomUrlParam

import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys

INSTANCE_ID = '5131c369-a0fe-48d9-921c-1ed575caab08'


def plot_image(fname, image, factor=1):
    """
    Utility function for plotting RGB images.
    """
    fig = plt.subplots(nrows=1, ncols=1, figsize=(15, 7))

    if np.issubdtype(image.dtype, np.floating):
        plt.imshow(np.minimum(image * factor, 1))
    else:
        plt.imshow(image)
    plt.savefig(fname)


# volcano_bbox = BBox(bbox=[(-2217485.0, 9228907.0),
#                           (-2150692.0, 9284045.0)], crs=CRS.POP_WEB)
# l8_request = WmsRequest(data_source=DataSource.LANDSAT8,
#                         layer='LST',
#                         bbox=volcano_bbox,
#                         time='2017-08-20',
#                         width=512,
#                         instance_id=INSTANCE_ID)
#
# l8_data = l8_request.get_data()
# plot_image('test.jpg', l8_data[-1])

betsiboka_coords_wgs84 = [46.16, -16.15, 46.51, -15.58]
betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
geometry = BBox(bbox=[-79.477810, 43.945970,
                      -79.407530, 43.754350], crs=CRS.WGS84)
for month in range(12):
    for day in range(31):
        date = '2017-{:02d}-{:02d}'.format(month + 1, day + 1)
        print(date)
        try:
            l8_request = WmsRequest(data_source=DataSource.LANDSAT8,
                                    layer='LST',
                                    bbox=betsiboka_bbox,
                                    time=date,
                                    width=512,
                                    instance_id=INSTANCE_ID)

            l8_data = l8_request.get_data()
            if len(l8_data):
                print("saved")
                plot_image(f"{month}_{day}.jpg", l8_data[-1])
        except ValueError:
            print("ValueError: Date?")
