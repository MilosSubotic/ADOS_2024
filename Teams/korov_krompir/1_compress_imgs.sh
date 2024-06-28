#!/bin/bash

IMG_DIR=./dataset/images/train

mkdir -p "$IMG_DIR/tmp/"
find "$IMG_DIR/*.jpg" -exec convert {} -resize 640x480 tmp/{} \;
rm "$IMG_DIR/*.jpg"
mv "$IMG_DIR/tmp/*.jpg" .
rmdir "$IMG_DIR/tmp/"


IMG_DIR=./dataset/images/test

mkdir -p "$IMG_DIR/tmp/"
find "$IMG_DIR/*.jpg" -exec convert {} -resize 640x480 tmp/{} \;
rm "$IMG_DIR/*.jpg"
mv "$IMG_DIR/tmp/*.jpg" .
rmdir "$IMG_DIR/tmp/"

IMG_DIR=./dataset/images/val

mkdir -p "$IMG_DIR/tmp/"
find "$IMG_DIR/*.jpg" -exec convert {} -resize 640x480 tmp/{} \;
rm "$IMG_DIR/*.jpg"
mv "$IMG_DIR/tmp/*.jpg" .
rmdir "$IMG_DIR/tmp/"