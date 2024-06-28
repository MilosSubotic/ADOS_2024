import os
import glob
from shutil import move, rmtree
from PIL import Image

IMG_DIR = 'C:/Users/radov/Desktop/ADOS/ADOS_2024/Teams/banana/dataset/images/train'
TMP_DIR = os.path.join(IMG_DIR, 'tmp')

# Create temporary directory
os.makedirs(TMP_DIR, exist_ok=True)

try:
    # Resize images and move them to temporary directory
    for filename in glob.glob(os.path.join(IMG_DIR, '*.jpg')):
        try:
            img = Image.open(filename)
            img = img.resize((640, 480))
            new_filename = os.path.join(TMP_DIR, os.path.basename(filename))
            img.save(new_filename)
            print(f'Resized and moved to tmp: {new_filename}')
            img.close()  # Make sure to close the image file
        except Exception as e:
            print(f'Failed to process {filename}: {e}')

    # Remove original .jpg files
    for filename in glob.glob(os.path.join(IMG_DIR, '*.jpg')):
        try:
            os.remove(filename)
            print(f'Removed original: {filename}')
        except Exception as e:
            print(f'Failed to remove {filename}: {e}')

    # Move resized images back to IMG_DIR
    for filename in glob.glob(os.path.join(TMP_DIR, '*.jpg')):
        try:
            move(filename, IMG_DIR)
            print(f'Moved back to IMG_DIR: {filename}')
        except Exception as e:
            print(f'Failed to move {filename}: {e}')

finally:
    # Remove temporary directory
    try:
        rmtree(TMP_DIR)
        print(f'Removed temporary directory: {TMP_DIR}')
    except Exception as e:
        print(f'Failed to remove temporary directory {TMP_DIR}: {e}')