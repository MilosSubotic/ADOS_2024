#!/bin/bash

IMG_DIR="./dataset/images/test"
DST_DIR="./dataset/images/train"
TMP_DIR="$IMG_DIR/tmp"
total_files=$(find "$IMG_DIR" -type f -name "*.jpg" | wc -l)
processed_files=0

display_percentage() {
    local current=$1
    local total=$2
    local percentage=$(( (current * 100) / total ))
    printf "\rProcessing... %d%% (%d/%d files)" "$percentage" "$current" "$total"
}

mkdir -p "$TMP_DIR"

find "$IMG_DIR" -type f -name "*.jpg" | while read -r file; do
    filename=$(basename "$file")
    convert "$file" -resize 640x480! "$TMP_DIR/$filename"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to resize $file"
        continue
    fi
    ((processed_files++))
    display_percentage "$processed_files" "$total_files"
done

echo "" 

# rm "$IMG_DIR"/*.jpg

mv "$TMP_DIR"/*.jpg "$DST_DIR"
rmdir "$TMP_DIR"

echo "Operation completed successfully!"