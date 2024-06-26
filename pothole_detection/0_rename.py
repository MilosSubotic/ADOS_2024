import os
import random
import string

def get_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def rename_images_to_random(directory):
    # List all files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    
    # Rename each file to a random 10-character string
    for filename in files:
        random_name = get_random_string() + ".jpg"
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, random_name)
        os.rename(src, dst)
        print(f"Renamed {src} to {dst}")

def rename_images_sequentially(directory):
    # List all files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    
    # Sort files to ensure consistent ordering
    files.sort()

    # Rename each file sequentially
    for i, filename in enumerate(files):
        new_name = f"{i + 1}.jpg"
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_name)
        os.rename(src, dst)
        print(f"Renamed {src} to {dst}")

if __name__ == "__main__":
    input_directory = r'C:\Users\anaze\Desktop\ADOS_2024\pothole_detection\raw_images'
    
    # Step 1: Rename images to random 10-character strings
    rename_images_to_random(input_directory)
    
    # Step 2: Rename images sequentially
    rename_images_sequentially(input_directory)
