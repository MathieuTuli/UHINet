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
    plt.savefig(image_name.str())
