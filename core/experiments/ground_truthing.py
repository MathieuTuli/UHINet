from pathlib import Path
from uhinet.backend.data.image_formatting import diff_images
from uhinet.backend.file_manager import save_pyplot_image
from matplotlib import pyplot as plt
import cv2


path = Path('/home/mat/work/U-of-T/capstone/uhinet/data/images')

total = 0
count = 0
for images in path.iterdir():
    if 'inputs' in str(images):
        image = cv2.imread(str(images))
        output = cv2.imread(str(images).replace('inputs', 'outputs'))
        target = cv2.imread(str(images).replace('inputs', 'targets'))
        diff, val = diff_images(reference=target, other=output)
        save_pyplot_image(str(images).replace('inputs', 'diff'),
                          diff, cmap='Reds', colorbar=True)
        plt.close('all')
        total += val
        count += 1
total /= count
print(total)
