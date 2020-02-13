from pathlib import Path
from uhinet.backend.data.image_formatting import diff_images
from uhinet.backend.file_manager import save_pyplot_image
from matplotlib import pyplot as plt
import cv2
import numpy as np


# path = Path(
#     '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-v2/test/images')
path = Path(
    '/home/mat/machine-learning/ground-truthing/')

total = 0
count = 0
max_val = -1
min_val = 9999999999
vals = list()
for images in path.iterdir():
    if 'pred' in str(images):
        output = cv2.imread(str(images))
        # output = cv2.imread(str(images).replace('pred', 'target'))
        target = cv2.imread(str(images).replace('pred', 'target'))
        diff, val = diff_images(reference=target, other=output)
        save_pyplot_image(str(images).replace('pred', 'diff'),
                          diff, cmap='coolwarm', colorbar=True)
        plt.close('all')
        vals.append(val)
        max_val = val if val > max_val else max_val
        min_val = val if val < min_val else min_val
        total += val
        count += 1
total /= count
print(f'total {total}')
print(f'max {max_val}')
print(f'min {min_val}')

arr = np.array(vals)
print(f'mean {np.mean(arr)}')
print(f'std {np.std(arr)}')
