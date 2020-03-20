from pathlib import Path
from uhinet.backend.data.image_formatting import diff_images
from uhinet.backend.file_manager import save_pyplot_image
from uhinet.backend.requests import Predictor
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
img_bank = Path(
    '/home/mat/github/U-of-T/capstone/pytorch-CycleGAN-and-pix2pix/results/uhinet_pix2pix/test_latest/images')

img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case1_2015_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case1_2019_modified_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img2, img)
save_pyplot_image('1_diff_same.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)

img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case1_2015_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case1_2019_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('1_diff_real.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)

img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case1_2019_modified_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case1_2019_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('1_diff_modified.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)

print('s')

img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case2_2019_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case2_2015_modified_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('2_same.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)
img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case2_2015_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case2_2019_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('2_real.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)
img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case2_2015_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case2_2015_modified_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('2_modified.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)


print('s')
img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case3_2019_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case3_2015_modified_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('3_same.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)
img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case3_2015_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case3_2019_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('3_real.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)
img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case3_2015_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case3_2015_modified_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('3_modified.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)
case3_2019 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case3_2015_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
case3_2015m = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case3_2019_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(case3_2019, case3_2015m)
save_pyplot_image('dd.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)

print('s')

img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case4_2015_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case4_2019_modified_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('4_same.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)
img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case4_2015_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case4_2019_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('4_real.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)
img = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case4_2019_modified_fake_B.png')), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(
    str(img_bank / 'case4_2019_rgb_fake_B.png')), cv2.COLOR_BGR2RGB)
diff, val = diff_images(img, img2)
save_pyplot_image('4_modified.png', diff, cmap='bwr', vmin=0, vmax=255)
print(val)

# case2_2015_lst = cv2.imread(
#     '/home/mat/.uhinet/new-out/case2/2015/summer/0_LST.png')
# case2_2015_lst_ = cv2.imread(
#     '/home/mat/.uhinet/new-out/case2/2015/summer/_0_LST.png')
# case2_2019 = cv2.imread(
#     '/home/mat/.uhinet/new-out/case2/2019/summer/MODIFIED_LST.png')
# diff, val = diff_images(case2_2015_lst, case2_2019)
# print(f'true: {val * 100}')
# diff, val = diff_images(case2_2015_lst_, case2_2019)
# print(f'pred: {val * 100}')
#
# case2_2015_lst = cv2.imread(
#     '/home/mat/.uhinet/new-out/case2/2015/summer/2015_2019_LST.png')
# case2_2015_lst_ = cv2.imread(
#     '/home/mat/.uhinet/new-out/case2/2019/summer/_1_LST.png')
# case2_2019 = cv2.imread(
#     '/home/mat/.uhinet/new-out/case2/2019/summer/1_LST.png')
# diff, val = diff_images(case2_2019, case2_2015_lst)
# print(f'true: {val * 100}')
# diff, val = diff_images(case2_2015_lst_, case2_2015_lst)
# print(f'pred: {val * 100}')
#
# case3_2015 = cv2.imread(
#     '/home/mat/.uhinet/new-out/case3/2015/summer/MODIFIED_LST.png')
# case3_2019_rgb = cv2.imread(
#     '/home/mat/.uhinet/new-out/case3/2019/summer/0_RGB.png')
# case3_2019_lst = cv2.imread(
#     '/home/mat/.uhinet/new-out/case3/2019/summer/0_LST.png')
# case3_2019_lst_ = cv2.imread(
#     '/home/mat/.uhinet/new-out/case3/2019/summer/_0_LST.png')
# diff, val = diff_images(case3_2019_lst, case3_2015)
# print(f'true: {val * 100}')
# diff, val = diff_images(case3_2019_lst_, case3_2015)
# print(f'pred: {val * 100}')
#
# case4_2015_rgb = cv2.imread(
#     '/home/mat/.uhinet/new-out/case4/2015/summer/0_RGB.png')
# case4_2015_lst = cv2.imread(
#     '/home/mat/.uhinet/new-out/case4/2015/summer/0_LST.png')
# case4_2015_lst_ = cv2.imread(
#     '/home/mat/.uhinet/new-out/case4/2015/summer/_0_LST.png')
# case4_2019 = cv2.imread(
#     '/home/mat/.uhinet/new-out/case4/2019/summer/MODIFIED_LST.png')
# diff, val = diff_images(case4_2015_lst, case4_2019)
# print(f'true: {val * 100}')
# diff, val = diff_images(case4_2015_lst_, case4_2019)
# print(f'pred: {val * 100}')

# diff1, val = diff_images(reference=_2015_lst, other=_2015_lst_pred)
# save_pyplot_image('2015_diff.png',
#                   _2015_lst, cmap='jet', colorbar=True)
# print(f'2015: {val}')

# vals = []
# for img in images.iterdir():
#     if 'fake' in str(img):
#         fake = cv2.imread(str(img))
#         real = cv2.imread(str(img).replace('fake', 'real'))
#         diff, val = diff_images(reference=real, other=fake)
#         vals.append(val)
# print(np.mean(vals))
# print(np.max(vals))
# print(np.min(vals))
# vals = []
# for img in images.iterdir():
#     if 'fake' in str(img):
#         fake = cv2.imread(str(img))
#         real = cv2.imread(str(img).replace('fake', 'real'))
#         diff, val = diff_images(reference=real, other=fake)
#         vals.append(val)
# print(np.mean(vals))
# print(np.max(vals))
# print(np.min(vals))
# vals = []
# for img in images.iterdir():
#     if 'fake' in str(img):
#         fake = cv2.imread(str(img))
#         real = cv2.imread(str(img).replace('fake', 'real'))
#         diff, val = diff_images(reference=real, other=fake)
#         save_pyplot_image(image_name='/home/mat/Downloads/diff_2.png',
#                           image=diff, vmin=0, vmax=255, cmap='bwr')
#         vals.append(val)
# print(np.mean(vals))
# print(np.max(vals))
# print(np.min(vals))
# print(np.std(vals))
# _2015_path_lst = (
#     '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-80-range/other/images/2-targets.png')
# _2019_path_lst = (
#     '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-80-range/other/images/3-targets.png')
# _2015_lst = cv2.imread(str(_2015_path_lst))
# _2019_lst = cv2.imread(str(_2019_path_lst))
# _2015_path_lst_pred = (
#     '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-80-range/other/images/2-outputs.png')
# _2019_path_lst_pred = (
#     '/home/mat/github/U-of-T/capstone/pix2pix-tensorflow/5-metres-80-range/other/images/3-outputs.png')
# _2015_lst_pred = cv2.imread(str(_2015_path_lst_pred))
# _2019_lst_pred = cv2.imread(str(_2019_path_lst_pred))
#
# _2015_lst[:, :, 0] = 0
# _2015_lst[:, :, 1] = 0
# _2019_lst[:, :, 0] = 0
# _2019_lst[:, :, 1] = 0
# _2015_lst_pred[:, :, 0] = 0
# _2015_lst_pred[:, :, 1] = 0
# _2019_lst_pred[:, :, 0] = 0
# _2019_lst_pred[:, :, 1] = 0
#
# diff1, val = diff_images(reference=_2015_lst, other=_2015_lst_pred)
# save_pyplot_image('2015_diff.png',
#                   _2015_lst, cmap='jet', colorbar=True)
# print(f'2015: {val}')
#
# diff2, val = diff_images(reference=_2019_lst, other=_2019_lst_pred)
# save_pyplot_image('2019_diff.png',
#                   diff2, cmap='jet', colorbar=True)
# print(f'2019: {val}')
#
# diff2, val = diff_images(reference=_2015_lst, other=_2019_lst_pred)
# save_pyplot_image('2015_2019_lst_pred.png',
#                   diff2, cmap='jet', colorbar=True)
# print(f'2019: {val}')
#
#
# diff, val = diff_images(reference=_2015_lst, other=_2019_lst)
# save_pyplot_image('2015_2019_lst_lst.png',
#                   diff, cmap='jet', colorbar=True)
# print(f'2015/9: {val}')
#
#
# diff1, val = diff_images(reference=_2015_lst_pred, other=_2019_lst_pred)
# save_pyplot_image('2015_2019_pred_pred.png',
#                   diff1, cmap='jet', colorbar=True)
# print(f'2015/9_pred: {val}')
