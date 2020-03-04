from typing import Optional, Union
# from pathlib import Path

from geopandas import GeoDataFrame

import logging
import io

import matplotlib.pyplot as plt
import numpy as np
import cv2

from .components import EnergyColumn, HeightColumn, BBox, ImageSize


def map_from_frame(frame: GeoDataFrame,
                   size: ImageSize,
                   bbox: BBox,
                   column: Union[HeightColumn, EnergyColumn],
                   sort_by: Union[HeightColumn, EnergyColumn],
                   ascending: bool = True,
                   legend: bool = False,
                   cmap: str = 'tab20') -> Optional[np.ndarray]:
    '''
    '''
    members = EnergyColumn.__members__.values() if \
        isinstance(column, EnergyColumn) else \
        HeightColumn if isinstance(column, HeightColumn) \
        else None
    if members is None:
        logging.critical("Unknown Column type")
        return None
    valid = [str(item) for item in members]
    keys = [str(item) for item in frame.keys()]
    if set(valid) != set(keys):
        logging.critical(
            f"Generate Energy Map: Shapefile does not contain " +
            f"required keys. Keys must be \n{set(valid)}, but keys are " +
            f"\n{set(keys)}")
        return None
    if str(column) not in keys:
        logging.critical(f"Generate Energy Map: *column* param {str(column)}" +
                         f" not valid. Must be one of {valid}")
        return None
    # if str(sort_by) not in keys:
    #     logging.critical(
    #         f"Map from Geopandas: *sort_by* param {str(sort_by)}" +
    #         f" not valid. Must be one of {valid}")
    #     return None
    # frame = frame.sort_values(by=str(sort_by))
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.canvas.draw()
    fig.add_axes(ax)
    if legend:
        frame.plot(column=str(column), ax=ax, legend=True, cmap=cmap)
    else:
        frame.plot(column=str(column), ax=ax, cmap=cmap)
    plt.gca().set_xlim([bbox.top_left.lon, bbox.bottom_right.lon])
    plt.gca().set_ylim([bbox.top_left.lat, bbox.bottom_right.lat])
    plt.gca().invert_yaxis()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=200,
                bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    image = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    image = cv2.imdecode(image, 1)
    return cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                      (size.width, size.height))


def ax_from_frame(frame: GeoDataFrame,
                  size: ImageSize,
                  column: Union[HeightColumn, EnergyColumn],
                  sort_by: Union[HeightColumn, EnergyColumn],
                  ascending: bool = True,
                  legend: bool = False,
                  cmap: str = 'tab20'):
    '''
    '''
    members = EnergyColumn.__members__.values() if \
        isinstance(column, EnergyColumn) else \
        HeightColumn if isinstance(column, HeightColumn) \
        else None
    if members is None:
        logging.critical("Unknown Column type")
        return None
    valid = [str(item) for item in members]
    keys = [str(item) for item in frame.keys()]
    if set(valid) != set(keys):
        logging.critical(
            f"Generate Energy Map: Shapefile does not contain " +
            f"required keys. Keys must be \n{set(valid)}, but keys are " +
            f"\n{set(keys)}")
        return None
    if str(column) not in keys:
        logging.critical(f"Generate Energy Map: *column* param {str(column)}" +
                         f" not valid. Must be one of {valid}")
        return None
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.canvas.draw()
    fig.add_axes(ax)
    if legend:
        frame.plot(column=str(column), ax=ax, legend=True, cmap=cmap)
    else:
        frame.plot(column=str(column), ax=ax, cmap=cmap)
    return fig, ax
