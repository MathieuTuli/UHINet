from sentinelhub import WmsRequest, DataSource, CustomUrlParam, CRS, \
    BBox as SentinelBBox
from typing import Optional

import numpy as np
import traceback

from ..components import BBox, ImageSize


class SentinelHubAccessor:
    def __init__(self,
                 instance_id: str = ''):
        self.instance_id = instance_id

    def get_landsat_image(self,
                          layer: str,
                          date: str,
                          image_size: ImageSize,
                          bbox: BBox) -> Optional[np.ndarray]:
        if layer not in ['RGB', 'LST']:
            print("SentinelHubAccessor: Error: " +
                  "@param layer must be one of RGB of LST")
        if not isinstance(image_size, ImageSize):
            print("SentinelHubAccessor: Error: " +
                  "@param image_size must be of type ImageSize")
        if not isinstance(bbox, BBox):
            print("SentinelHubAccessor: Error: " +
                  "@param bbox must be of type BBox")
        try:

            coords = [bbox.top_left.lon, bbox.top_left.lat,
                      bbox.bottom_right.lon, bbox.bottom_right.lat]
            geometry = SentinelBBox(bbox=coords, crs=CRS.WGS84)
            print(layer)
            print(date)
            print(image_size.height)
            print(image_size.width)
            print(self.instance_id)
            request = WmsRequest(
                data_source=DataSource.LANDSAT8,
                layer=layer,
                bbox=geometry,
                time=date,
                # height=image_size.height,
                width=image_size.width,
                instance_id=self.instance_id,
                custom_url_params={
                    CustomUrlParam.SHOWLOGO: False})
            print(request.get_url_list())
            data = request.get_data()
            if len(data):
                return data[-1]
            return None
        except Exception:
            traceback.print_exc()
            return None
