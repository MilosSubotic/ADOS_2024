from PIL import Image
import os
import threading

input_folder = 'used_images/original'
output_folder = 'used_images/resized'
target_width = 640
target_height = 480

drinks = {
    "cola",
    "fanta",
    "guarana",
    "pepsi"
}
 
def resize_images(input_folder, output_folder, target_width, target_height, drink):
    os.makedirs(output_folder, exist_ok=True)
    i = 1
 
    images = os.listdir(input_folder + "/" + drink)
 
    for image_name in images:
        try:
            image_path = os.path.join(input_folder, drink, image_name)
            img = Image.open(image_path)
 
            img_resized = img.resize((target_width, target_height))
 
            output_path = os.path.join(output_folder, drink, f"{drink}{i}.jpg")
            img_resized.save(output_path)

            print(f"{image_name} -> {drink}{i}.jpg uspešno resizeovana.")

            i += 1
        except Exception as e:
            print(f"Greška prilikom resizeovanja {image_name} -> {drink}{i}: {str(e)}")
 

threads = []

for drink in drinks:
    thread = threading.Thread(target=resize_images, args=(input_folder, output_folder, target_width, target_height, drink))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
