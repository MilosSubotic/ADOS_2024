import os
from PIL import Image, ExifTags

# Source and destination folders
SOURCE_DIR = r"C:\Users\anaze\Desktop\ADOS_2024\pothole_detection\raw_images"
DEST_DIR = r"C:\Users\anaze\Desktop\ADOS_2024\pothole_detection\dataset\images"

# Check if source directory exists
if not os.path.isdir(SOURCE_DIR):
    print(f"Error: Source directory {SOURCE_DIR} does not exist.")
    exit(1)

# Create destination directory if it doesn't exist
os.makedirs(DEST_DIR, exist_ok=True)

# Iterate over each file in the source directory
for img_file in os.listdir(SOURCE_DIR):
    if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(SOURCE_DIR, img_file)
        dest_path = os.path.join(DEST_DIR, img_file)

        try:
            # Open the image and preserve its orientation
            with Image.open(img_path) as img:
                # Check for EXIF orientation tag
                if hasattr(img, "_getexif") and isinstance(img._getexif(), dict):
                    exif_data = img._getexif()
                    orientation_tag = ExifTags.TAGS.get("Orientation")
                    if orientation_tag and orientation_tag in exif_data:
                        exif_orientation = exif_data[orientation_tag]
                        # Rotate the image according to EXIF orientation tag
                        if exif_orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif exif_orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif exif_orientation == 8:
                            img = img.rotate(90, expand=True)

                # Resize the image while preserving the aspect ratio
                width, height = img.size
                max_dimension = max(width, height)
                scale_factor = 640 / max_dimension
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                img_resized = img.resize((new_width, new_height), Image.LANCZOS)
                img_resized.save(dest_path)
                print(f"Resized {img_file} and saved to {dest_path}")
        except Exception as e:
            print(f"Error processing {img_file}: {e}")

print("Resizing completed.")
