from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox, \
    WebFeatureService, BBox, CRS, DataSource, get_area_info
from sentinelhub import CustomUrlParam

import matplotlib.pyplot as plt
import numpy as np
import cv2


INSTANCE_ID = '5131c369-a0fe-48d9-921c-1ed575caab08'


def plot_image(image, factor=1):
    """
    Utility function for plotting RGB images.
    """
    fig = plt.subplots(nrows=1, ncols=1, figsize=(15, 7))

    if np.issubdtype(image.dtype, np.floating):
        plt.imshow(np.minimum(image * factor, 1))
    else:
        plt.imshow(image)


volcano_bbox = BBox(bbox=[(-2217485.0, 9228907.0),
                          (-2150692.0, 9284045.0)], crs=CRS.POP_WEB)

l8_request = WmsRequest(data_source=DataSource.LANDSAT8,
                        layer='RGB',
                        bbox=volcano_bbox,
                        time=('2017-11-01', '2018-02-28'),
                        width=512,
                        instance_id=INSTANCE_ID)

l8_data = l8_request.get_data()
cv2.imwrite('test.jpg', l8_data[-1])
plot_image(l8_data[-1])
