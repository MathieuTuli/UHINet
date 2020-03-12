from pathlib import Path

from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import inspect
import logging
import re


def check_suffix(file_name: Path, suffix: str) -> bool:
    regex = "^\..*"
    ret = re.search(regex, suffix)
    if not ret:
        logging.error(
            f"check_suffix: called from {inspect.stack()[1][3]}: " +
            f"Suffix \"{suffix}\" does not match regex. Must follow" +
            f" \"{regex}\".")
        return False

    if file_name.suffix != ".json":
        logging.error(
            f"check_suffix: called from {inspect.stack()[1][3]}: " +
            f"File suffix \"{file_name.suffix}\" " +
            f"invalid. Must be \"{suffix}\".")
        return False
    return True


def file_exists(file_name: Path) -> bool:
    if not file_name.exists():
        logging.error(
            f"file_exists: called from {inspect.stack()[1][3]}: " +
            f"File path \"{file_name}\" invalid. File not found.")
        return False
    return True


def init_dirs(dir_name: Path):
    if not dir_name.exists():
        dir_name.mkdir(exist_ok=True, parents=True)


def save_pyplot_image(image_name: Path,
                      image: np.ndarray,
                      cmap: str = None,
                      vmin: int = -1,
                      vmax: int = -1,
                      colorbar: bool = False):
    """
    image: expecting value between [0, 1]
    """
    # fig = plt.subplots(nrows=1, ncols=1, figsize=(15, 7))
    fig = plt.figure(frameon=False)
    # plt.imshow(image)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.set_aspect('equal')
    fig.canvas.draw()
    fig.add_axes(ax)
    logging.debug(f"save_pyplot_image: {image_name} is of shape {image.shape}")
    norm = None
    if vmin != -1:
        norm = matplotlib.colors.Normalize(
            vmin=vmin,
            vmax=vmax)
    if cmap is not None:
        if norm is not None:
            ax.imshow(image, norm=norm, aspect='equal', cmap=cmap)
        else:
            ax.imshow(image, aspect='equal', cmap=cmap)
    else:
        if norm is not None:
            ax.imshow(image, aspect='equal')
        else:
            ax.imshow(image, norm=norm, aspect='equal')
    if colorbar:
        mappable = plt.imshow(image)
        mappable.set_cmap(cmap)
        plt.clim(-3, 3)
        plt.colorbar()
    plt.savefig(str(image_name), bbox_inches='tight')
    plt.close(fig)
