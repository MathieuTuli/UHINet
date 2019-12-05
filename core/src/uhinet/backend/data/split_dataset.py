from pathlib import Path

import random
import cv2

from .image_formatting import concatenate_horizontal

if __name__ == "__main__":
    files = Path('images')
    counter = 0
    for _dir in files.iterdir():
        if 'jpg' in str(_dir):
            continue
        for year in _dir.iterdir():
            if 'jpg' in str(year):
                continue
            for images in year.iterdir():
                if 'LST' in str(images):
                    rgb_img = str(images).replace('LST', 'RGB')
                    im1 = cv2.imread(str(images))
                    im2 = cv2.imread(str(rgb_img))
                    new_img = concatenate_horizontal([im1, im2])
                    if random.randint(0, 100) < 30:
                        cv2.imwrite(f'images/test/{counter}.jpg', new_img)
                    else:
                        cv2.imwrite(f'images/train/{counter}.jpg', new_img)
                    counter += 1
    # for x in files.iterdir():
    #     if 'png' in str(x):
    #         if random.randint(0, 100) < 30:
    #             shutil.move(str(x), f"test/{str(x)}")
    #         else:
    #             shutil.move(str(x), f"train/{str(x)}")
