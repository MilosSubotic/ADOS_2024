from ultralytics import YOLO
import glob
import os

# Putanje do modela
model_best_path = r"C:\Users\anaze\Desktop\ADOS_2024\pothole_detection\runs\detect\train\weights\best.pt"
model_last_path = r"C:\Users\anaze\Desktop\ADOS_2024\pothole_detection\runs\detect\train\weights\last.pt"

# Provera postojanja modela
if not os.path.exists(model_best_path):
    print(f"Model best.pt not found at {model_best_path}")
    exit()
if not os.path.exists(model_last_path):
    print(f"Model last.pt not found at {model_last_path}")
    exit()

# Ucitavanje modela
try:
    model_best = YOLO(model_best_path)
    model_last = YOLO(model_last_path)
except Exception as e:
    print(f"Error loading models: {e}")
    exit()

# Putanja do test skupa podataka
test_images_path = r'C:\Users\anaze\Desktop\ADOS_2024\pothole_detection\dataset\images\test\*.jpg'
test_images = glob.glob(test_images_path)
if not test_images:
    print(f"No test images found at {test_images_path}")
    exit()

# Predikcija i cuvanje rezultata za best.pt
try:
    results_best = model_best.predict(source=test_images, save=True, save_txt=True, save_conf=True)
except Exception as e:
    print(f"Error during prediction with best.pt model: {e}")
    exit()

# Predikcija i cuvanje rezultata za last.pt
try:
    results_last = model_last.predict(source=test_images, save=True, save_txt=True, save_conf=True)
except Exception as e:
    print(f"Error during prediction with last.pt model: {e}")
    exit()

# Funkcija za poredjenje rezultata 
def compare_results(results_best, results_last):
    for i, (res_best, res_last) in enumerate(zip(results_best, results_last)):
        print(f"Image {i+1}:")
        print(f"Best model detections: {len(res_best.boxes)}")
        print(f"Last model detections: {len(res_last.boxes)}")

# Poziv funkcije za poredjenje rezultata
compare_results(results_best, results_last)
