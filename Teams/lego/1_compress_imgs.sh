#!/bin/bash

#TODO Python script.

IMG_DIR=../../../../Agriculture_Machinery_Data_Heavy/Cherry_Picker_Arm/Media/lego/

mkdir -p "$IMG_DIR/tmp/"
find "$IMG_DIR/*.jpg" -exec convert {} -resize 640x480 tmp/{} \;
rm "$IMG_DIR/*.jpg"
mv "$IMG_DIR/tmp/*.jpg" .
rmdir "$IMG_DIR/tmp/"
