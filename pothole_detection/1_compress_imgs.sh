#!/bin/bash

# Source and destination folders
SOURCE_DIR="/home/ana/Desktop/ADOS_2024/pothole_detection/raw_images/"
DEST_DIR="/home/ana/Desktop/ADOS_2024/pothole_detection/dataset/images"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory $SOURCE_DIR does not exist."
    exit 1
fi

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Iterate over each JPEG image in the source directory
for img_file in "$SOURCE_DIR"/*.jpg; do
    if [ -f "$img_file" ]; then
        img_name=$(basename "$img_file")
        dest_path="$DEST_DIR/${img_name%.*}.jpg"
        
        # Resize image to 640x480 and save to destination directory
        convert "$img_file" -resize 640x480 "$dest_path"
        
        echo "Resized $img_name and saved to $dest_path"
    fi
done

echo "Resizing completed."

