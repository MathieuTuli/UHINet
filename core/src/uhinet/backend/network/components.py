from typing import NamedTuple

import Enum


class ImageDirection(Enum):
    AtoB = 0
    BtoA = 1

    def __str__(self):
        return self.name
