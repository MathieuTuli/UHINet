from pathlib import Path
from uhinet.backend.data.image_formatting import diff_images
from uhinet.backend.file_manager import save_pyplot_image
from matplotlib import pyplot as plt
import cv2


before = Path('/home/mat/Downloads/test2-targets.png')
after = Path('/home/mat/Downloads/test2-outputs.png')

output = cv2.imread(str(before))
target = cv2.imread(str(after))
diff, val = diff_images(reference=output, other=target)
save_pyplot_image('diff.png',
                  diff, cmap='hot', colorbar=True)
plt.close('all')
print(val)
