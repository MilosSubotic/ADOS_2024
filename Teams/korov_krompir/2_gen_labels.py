#!/usr/bin/env python3


cfg = 'HSV_Thresholds.cfg.yaml'
labeler = 'OpenCV/HSV/build/HSV_Labeler'
images_dir = 'Teams/korov_krompir/dataset/images/'
labels_dir = 'Teams/korov_krompir/dataset/gen_labels/'



import os
import glob
import subprocess
import shutil
from os.path import *

def run_cmd(cmd):
	r = subprocess.run(cmd.split())
	if r.returncode != 0:
		error('failed cmd:', cmd)


for subdir in ['train', 'val', 'test']:
	images_subdir = join(images_dir, subdir)
	labels_subdir = join(labels_dir, subdir)
	os.makedirs(labels_subdir, exist_ok = True)
	print(labels_subdir)
	for img in glob.glob(join(images_subdir, '*.jpg')):
		print(img)
		b = basename(img)
		c, e = splitext(b)
		label = join(labels_subdir, c + ".txt")
		run_cmd(f'{labeler} {cfg} {img} {label}')


