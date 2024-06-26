from PIL import Image
import os

# Putanja do foldera sa slikama koje želiš kompresovati
folder_path = "output_frames_poklopac_antifriza_i_tecnosti_za_soferku_Noc"

# Novi folder za čuvanje kompresovanih slika (možeš promeniti ime foldera ovde)
new_folder_name = "compressed_poklopac_antifriza_i_tecnosti_za_soferku_Noc"
compressed_folder_path = os.path.join(folder_path, new_folder_name)

# Provera da li novi folder već postoji, ako ne, napravi ga
if not os.path.exists(compressed_folder_path):
    os.makedirs(compressed_folder_path)

# Prođi kroz svaku sliku u folderu
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # Učitaj sliku
        img_path = os.path.join(folder_path, filename)
        img = Image.open(img_path)
        
        # Kompresuj sliku na 640x480
        img = img.resize((640, 480))
        
        # Sačuvaj kompresovanu sliku u novom folderu
        new_img_path = os.path.join(compressed_folder_path, filename)
        img.save(new_img_path)

        print(f"Kompresovana slika {filename} i smeštena u {new_img_path}")

