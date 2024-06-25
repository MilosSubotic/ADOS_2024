import os
import glob
from shutil import move, rmtree
from PIL import Image

IMG_DIR = 'C:/Users/Vuk Antovic/Desktop/ADOS_2024/Teams/korov_krompir/dataset/images/train'
TMP_DIR = os.path.join(IMG_DIR, 'tmp')

# Create temporary directory
os.makedirs(TMP_DIR, exist_ok=True)

# Resize images and move them to temporary directory
for filename in glob.glob(os.path.join(IMG_DIR, '*.jpg')):
    img = Image.open(filename)
    img = img.resize((640, 480))
    new_filename = os.path.join(TMP_DIR, os.path.basename(filename))
    img.save(new_filename)
    print(new_filename)

# Remove original .jpg files
for filename in glob.glob(os.path.join(IMG_DIR, '*.jpg')):
    os.remove(filename)

# Move resized images back to IMG_DIR
for filename in glob.glob(os.path.join(TMP_DIR, '*.jpg')):
    move(filename, IMG_DIR)

# Remove temporary directory
rmtree(TMP_DIR)
