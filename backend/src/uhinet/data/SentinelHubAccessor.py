from sentinelhub import WmsRequest, DataSource, CustomUrlParam, CRS, \
    BBox as SentinelBBox
from typing import List

import numpy as np
import traceback
import logging

from .components import BBox, ImageSize


class SentinelHubAccessor:
    def __init__(self,
                 instance_id: str = ''):
        self.instance_id = instance_id

    def get_landsat_image(self,
                          layer: str,
                          date: str,
                          image_size: ImageSize,
                          bbox: BBox,
                          cloud_cov_perc: float) -> List[np.ndarray]:
        if layer not in ['RGB', 'LST']:
            logging.error("SentinelHubAccessor: " +
                          "@param layer must be one of RGB of LST")
            return []
        if not isinstance(image_size, ImageSize):
            logging.error("SentinelHubAccessor: " +
                          "@param image_size must be of type ImageSize")
            return []
        if not isinstance(bbox, BBox):
            logging.error("SentinelHubAccessor: " +
                          "@param bbox must be of type BBox")
            return []
        if cloud_cov_perc < 0.0 or cloud_cov_perc > 1.0:
            logging.error("SentinelHubAccessor: " +
                          "@param cloud_cov_perc must be in the range [0, 1]")
            return []
        try:
            coords = [bbox.top_left.lon, bbox.top_left.lat,
                      bbox.bottom_right.lon, bbox.bottom_right.lat]
            geometry = SentinelBBox(bbox=coords, crs=CRS.WGS84)
            request = WmsRequest(
                data_source=DataSource.LANDSAT8,
                layer=layer,
                bbox=geometry,
                time=date,
                width=image_size.width,
                instance_id=self.instance_id,
                maxcc=cloud_cov_perc,
                custom_url_params={
                    CustomUrlParam.SHOWLOGO: False})
            logging.debug(
                f"SentinelHubAccessor: URLs: {request.get_url_list()}")
            data = request.get_data()
            if len(data):
                return data
            return None
        except Exception:
            traceback.print_exc()
            return None
