from typing import Optional, Tuple
from pathlib import Path

from geopandas import GeoDataFrame

import logging

import matplotlib.pyplot as plt
import numpy as np

from .components import Column, BBox


def map_from_shp(path: Path,
                 bbox: BBox = None,
                 column: Column = Column.HEIGHT,
                 sort_by: Column = Column.HEIGHT,
                 ascending: bool = True,
                 legend: bool = False,
                 cmap: str = 'tab20') -> Optional[np.ndarray]:
    '''
    '''
    if not path.exists():
        logging.critical(f"Map from Geopands: Path {path} does not exist")
        return None
    frame = GeoDataFrame.from_file(str(path))
    valid = [str(item) for item in Column.__members__.values()]
    keys = [str(item) for item in frame.keys()]
    if set(valid) != set(keys):
        logging.critical(f"Map from Geopandas: Shapefile does not contain " +
                         f"required keys. Keys must be {valid}")
        return None
    if str(column) not in keys:
        logging.critical(f"Map from Geopandas: *column* param {str(column)}" +
                         f" not valid. Must be one of {valid}")
        return None
    if str(sort_by) not in keys:
        logging.critical(
            f"Map from Geopandas: *sort_by* param {str(sort_by)}" +
            f" not valid. Must be one of {valid}")
        return None
    frame = frame.sort_values(by=str(sort_by))
    fig = plt.figure()
    fig, ax = plt.subplots(1, 1)
    plt.gca().set_xlim((bbox.top_left.lon, bbox.bottom_right.lon))
    plt.gca().set_ylim((bbox.top_left.lat, bbox.bottom_right.lat))
    if legend:
        frame.plot(column=str(column), ax=ax, legend=True, cmap=cmap)
    else:
        frame.plot(column=str(column), cmap=cmap)
    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data
