import os
import glob
from PIL import Image

img_dir = 'datasets/train/images'
tmp_dir = os.path.join(img_dir, 'tmp')
extension = "JPG"

os.makedirs(tmp_dir, exist_ok=True)

image_files = glob.glob(os.path.join(img_dir, f'*.{extension}'))

for img_path in image_files:
    img = Image.open(img_path)
    img = img.resize((640, 480))
    tmp_img_path = os.path.join(tmp_dir, os.path.basename(img_path))
    img.save(tmp_img_path)

for img_path in image_files:
    os.remove(img_path)

resized_images = glob.glob(os.path.join(tmp_dir, f'*.{extension}'))
for img_path in resized_images:
    os.rename(img_path, os.path.join(img_dir, os.path.basename(img_path)))

os.rmdir(tmp_dir)

