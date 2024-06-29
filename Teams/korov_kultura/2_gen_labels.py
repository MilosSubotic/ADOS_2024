#!/usr/bin/env python3
import subprocess

cfg = 'HSV_Thresholds.cfg.yaml'
labeler = '/home/tonke9/ADOS24/ADOS_2024/kultura+korov/HSV_Labeler.py'
images_dir = '/home/tonke9/ADOS24/ADOS_2024/kultura+korov/dataset/'
labels_dir = '/home/tonke9/ADOS24/ADOS_2024/kultura+korov/dataset/'



import os
import glob
import subprocess
import shutil
from os.path import *

def run_cmd(cmd):
    r = subprocess.run(cmd.split())
    if r.returncode != 0:
        raise RuntimeError(f'Failed command: {cmd}')


subdirs_to_process = ['train', 'test']

for subdir in subdirs_to_process:
    images_subdir = join(images_dir, subdir)
    labels_subdir = join(labels_dir, subdir)
    os.makedirs(labels_subdir, exist_ok=True)
    
    for img in glob.glob(join(images_subdir, '*.jpg')):
        b = basename(img)
        c, e = splitext(b)
        label = join(labels_subdir, c + ".txt")
        run_cmd(f'{labeler} {cfg} {img} {label}')

print("Processing complete.")
