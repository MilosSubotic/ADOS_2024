import os
import glob
from shutil import move, rmtree
from PIL import Image

#IMG_DIR = 'C:/Users/user/Desktop/adosProj/ADOS_2024/Teams/smeceFlase/dataset/images/test'
#IMG_DIR = 'C:/Users/user/Desktop/adosProj/ADOS_2024/Teams/smeceFlase/dataset/images/train'
IMG_DIR = 'C:/Users/user/Desktop/adosProj/ADOS_2024/Teams/smeceFlase/dataset/images/val'
TMP_DIR = os.path.join(IMG_DIR, 'tmp')


os.makedirs(TMP_DIR, exist_ok=True)

print(glob.glob(os.path.join(IMG_DIR, '*.jpg')))

for filename in glob.glob(os.path.join(IMG_DIR, '*.jpg')):
    img = Image.open(filename)
    img = img.resize((640, 480))
    new_filename = os.path.join(TMP_DIR, os.path.basename(filename))
    img.save(new_filename)
    print(f"saved {filename}")

for filename in glob.glob(os.path.join(IMG_DIR, '*.jpg')):
    os.remove(filename)


for filename in glob.glob(os.path.join(TMP_DIR, '*.jpg')):
    move(filename, IMG_DIR)


rmtree(TMP_DIR)
