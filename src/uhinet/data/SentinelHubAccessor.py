from sentinelhub import WmsRequest, DataSource, CustomUrlParam
from typing import Optional
from pathlib import Path

import numpy as np

from .components import BBox, ImageSize, LandsatLayer


class SentinelHubAccessor:
    def __init__(self,
                 image_dir: Path,
                 instance_id: str = ''):
        self.instance_id = instance_id
        self.image_dir = image_dir

    def get_landsat_image(self,
                          layer: LandsatLayer,
                          date: str,
                          image_size: ImageSize,
                          bbox: BBox) -> Optional[np.ndarray]:
        if not isinstance(layer, LandsatLayer):
            print("SentinelHubAccessor: Error: " +
                  "@param layer must be of type LandsatLayer")
        if not isinstance(image_size, ImageSize):
            print("SentinelHubAccessor: Error: " +
                  "@param image_size must be of type ImageSize")
        if not isinstance(bbox, BBox):
            print("SentinelHubAccessor: Error: " +
                  "@param bbox must be of type BBox")
        try:
            request = WmsRequest(
                data_source=DataSource.LANDSAT8,
                layer=layer,
                bbox=betsiboka_bbox,
                time=date,
                width=512,
                instance_id=self.instance_id,
                custom_url_params={
                    CustomUrlParam.SHOWLOGO: False})
            data = request.data()
            if len(data):
                return data[-1]
            return None
        except Exception:
            return None
