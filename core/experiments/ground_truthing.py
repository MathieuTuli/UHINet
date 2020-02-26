from pathlib import Path
from uhinet.backend.data.image_formatting import diff_images
from uhinet.backend.file_manager import save_pyplot_image
from matplotlib import pyplot as plt
import cv2
import numpy as np


# path = Path(
#     '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-80-range/test/images')
# # path = Path(
# #     '/home/mat/machine-learning/ground-truthing/')
#
# vals = list()
# for images in path.iterdir():
#     if 'inputs' in str(images):
#         image = cv2.imread(str(images))
#         output = cv2.imread(str(images).replace('inputs', 'outputs'))
#         target = cv2.imread(str(images).replace('inputs', 'targets'))
#         diff, val = diff_images(reference=target, other=output)
#         save_pyplot_image(str(images).replace('inputs', 'diff'),
#                           diff, cmap='coolwarm', colorbar=True)
#         plt.close('all')
#         vals.append(val)
# arr = np.array(vals)
# print(f'mean {np.mean(arr)}')
# print(f'std {np.std(arr)}')
# print(f'max {np.max(arr)}')
# print(f'min {np.min(arr)}')

vals = list()

_2015_path_lst = (
    '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-80-range/other/images/2-targets.png')
_2019_path_lst = (
    '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-80-range/other/images/3-targets.png')
_2015_lst = cv2.imread(str(_2015_path_lst))
_2019_lst = cv2.imread(str(_2019_path_lst))
_2015_path_lst_pred = (
    '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-80-range/other/images/2-outputs.png')
_2019_path_lst_pred = (
    '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-80-range/other/images/3-outputs.png')
_2015_lst_pred = cv2.imread(str(_2015_path_lst_pred))
_2019_lst_pred = cv2.imread(str(_2019_path_lst_pred))

_2015_lst[:, :, 0] = 0
_2015_lst[:, :, 1] = 0
_2019_lst[:, :, 0] = 0
_2019_lst[:, :, 1] = 0
_2015_lst_pred[:, :, 0] = 0
_2015_lst_pred[:, :, 1] = 0
_2019_lst_pred[:, :, 0] = 0
_2019_lst_pred[:, :, 1] = 0

diff1, val = diff_images(reference=_2015_lst, other=_2015_lst_pred)
save_pyplot_image('2015_diff.png',
                  _2015_lst, cmap='jet', colorbar=True)
print(f'2015: {val}')

diff2, val = diff_images(reference=_2019_lst, other=_2019_lst_pred)
save_pyplot_image('2019_diff.png',
                  diff2, cmap='jet', colorbar=True)
print(f'2019: {val}')

diff2, val = diff_images(reference=_2015_lst, other=_2019_lst_pred)
save_pyplot_image('2015_2019_lst_pred.png',
                  diff2, cmap='jet', colorbar=True)
print(f'2019: {val}')


diff, val = diff_images(reference=_2015_lst, other=_2019_lst)
save_pyplot_image('2015_2019_lst_lst.png',
                  diff, cmap='jet', colorbar=True)
print(f'2015/9: {val}')


diff1, val = diff_images(reference=_2015_lst_pred, other=_2019_lst_pred)
save_pyplot_image('2015_2019_pred_pred.png',
                  diff1, cmap='jet', colorbar=True)
print(f'2015/9_pred: {val}')
