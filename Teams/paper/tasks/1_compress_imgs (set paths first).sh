#!/bin/bash

IMG_DIR=" "   # Set source path (images to convert)
DST_DIR=" "   # Set destination path (folder to move converted images)

TMP_DIR="$IMG_DIR/tmp"
total_files=$(find "$IMG_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" \) | wc -l)
processed_files=0


# Display progress on terminal
display_percentage() {
    local current=$1
    local total=$2
    local percentage=$(( (current * 100) / total ))
    printf "\rProcessing... %d%% (%d/%d files)" "$percentage" "$current" "$total"
}

mkdir -p "$TMP_DIR"

# Convert images
find "$IMG_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" \) | while read -r file; do
    filename=$(basename "$file")
    
    convert "$file" -auto-orient "$TMP_DIR/$filename"
    
    convert "$TMP_DIR/$filename" -resize 640x480! -gravity center -extent 640x480 "$TMP_DIR/$filename"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to resize $file"
        continue
    fi
    ((processed_files++))
    display_percentage "$processed_files" "$total_files"
done

echo ""

# Move processed .jpg files if they exist
if ls "$TMP_DIR"/*.jpg 1> /dev/null 2>&1; then
    mv "$TMP_DIR"/*.jpg "$DST_DIR"
fi

# Move processed .jpeg files if they exist
if ls "$TMP_DIR"/*.jpeg 1> /dev/null 2>&1; then
    mv "$TMP_DIR"/*.jpeg "$DST_DIR"
fi

rmdir "$TMP_DIR"

echo "Operation completed successfully!"

