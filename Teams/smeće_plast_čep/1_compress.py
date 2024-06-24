import os
from PIL import Image

# Define the source directory and the new destination directory paths
img_dir = '/home/aleksandar/Desktop/nove'
dest_dir = '/home/aleksandar/Desktop/compressed_images'

# Ensure the destination directory exists
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# List all.jpg files in the source directory
jpg_files = [f for f in os.listdir(img_dir) if f.endswith('.jpg')]

# Resize each image to 768x768 and save it in the destination directory
for jpg_file in jpg_files:
    img_path = os.path.join(img_dir, jpg_file)
    try:
        with Image.open(img_path) as img:
            img_resized = img.resize((768, 768), Image.ANTIALIAS)
            # Update the destination path to the new directory
            dest_path = os.path.join(dest_dir, jpg_file)
            img_resized.save(dest_path)
    except Exception as e:
        print(f"Error processing {jpg_file}: {e}")

# Optionally, move the original.jpg files to a backup location or delete them
# Example: To move them to a backup directory
backup_dir = os.path.join(img_dir, 'backup')
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)
for jpg_file in jpg_files:
    os.rename(os.path.join(img_dir, jpg_file), os.path.join(backup_dir, jpg_file))

# Or, to delete the original.jpg files
# for jpg_file in jpg_files:
#     os.remove(os.path.join(img_dir, jpg_file))
