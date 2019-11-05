from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def init_dirs(dir_name: Path):
    if not dir_name.exists():
        dir_name.mkdir(exist_ok=True, parents=True)


def save_pyplot_image(image_name: Path,
                      image: np.ndarray):
    """
    """
    fig = plt.subplots(nrows=1, ncols=1, figsize=(15, 7))
    plt.imshow(image)
    # plt.show()
    plt.savefig(str(image_name))
