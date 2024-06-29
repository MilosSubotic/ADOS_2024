#!/usr/bin/env python3

import os
import glob
import subprocess
from os.path import join, basename, splitext

cfg = 'HSV_Thresholds.cfg.yaml'
labeler = 'OpenCV/HSV/build/HSV_Labeler'
dataset_dir = 'dataset'

def run_cmd(cmd):
    print(f"Running command: {cmd}")
    r = subprocess.run(cmd.split(), capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Failed cmd: {cmd}")
        print(f"Error: {r.stderr}")
    else:
        print(f"Command output: {r.stdout}")

# Define subdirectories
subdirs = ['train', 'valid', 'test']

for subdir in subdirs:
    images_subdir = join(dataset_dir, subdir, 'images')
    labels_subdir = join(dataset_dir, subdir, 'labels')
    os.makedirs(labels_subdir, exist_ok=True)
    
    for img in glob.glob(join(images_subdir, '*.jpg')):
        b = basename(img)
        c, e = splitext(b)
        label = join(labels_subdir, c + ".txt")
        run_cmd(f'{labeler} {cfg} {img} {label}')

