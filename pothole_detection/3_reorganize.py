import os
import shutil
import random

def create_folders(base_dir):
    # Create train, val, and test directories inside images and labels folders
    for folder in ['images', 'labels']:
        folder_dir = os.path.join(base_dir, folder)
        for split in ['train', 'val', 'test']:
            split_dir = os.path.join(folder_dir, split)
            os.makedirs(split_dir, exist_ok=True)

def distribute_files(image_dir, label_dir, base_dir, train_ratio=0.8, val_ratio=0.1):
    # Get list of images and shuffle them
    images = [f for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png')]
    random.shuffle(images)
    
    # Calculate split indices
    total_images = len(images)
    train_split = int(total_images * train_ratio)
    val_split = int(total_images * (train_ratio + val_ratio))
    
    # Split images into train, val, and test sets
    train_images = images[:train_split]
    val_images = images[train_split:val_split]
    test_images = images[val_split:]
    
    # Copy images to train, val, and test directories
    def copy_files(file_list, src_dir, dest_dir):
        for file_name in file_list:
            src_path = os.path.join(src_dir, file_name)
            dest_path = os.path.join(dest_dir, file_name)
            shutil.copy(src_path, dest_path)

    copy_files(train_images, image_dir, os.path.join(base_dir, 'images', 'train'))
    copy_files(val_images, image_dir, os.path.join(base_dir, 'images', 'val'))
    copy_files(test_images, image_dir, os.path.join(base_dir, 'images', 'test'))

    # Get list of labels corresponding to images
    labels = [f[:-4] + '.txt' for f in images if os.path.exists(os.path.join(label_dir, f[:-4] + '.txt'))]

    # Split labels into train, val, and test sets
    train_labels = labels[:train_split]
    val_labels = labels[train_split:val_split]
    test_labels = labels[val_split:]

    # Copy labels to train, val, and test directories
    copy_files(train_labels, label_dir, os.path.join(base_dir, 'labels', 'train'))
    copy_files(val_labels, label_dir, os.path.join(base_dir, 'labels', 'val'))
    copy_files(test_labels, label_dir, os.path.join(base_dir, 'labels', 'test'))

if __name__ == '__main__':
    base_directory = r'C:\Users\anaze\Desktop\ADOS_2024\pothole_detection\dataset'
    image_directory = os.path.join(base_directory, 'images')
    label_directory = os.path.join(base_directory, 'labels')

    create_folders(base_directory)
    distribute_files(image_directory, label_directory, base_directory)
