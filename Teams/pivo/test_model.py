import cv2
import os
from ultralytics import YOLO
from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk

class ImageLabeler:
    def __init__(self, master, model_path, image_folder):
        self.master = master
        self.model = YOLO(model_path)
        self.image_folder = image_folder
        self.image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.current_index = 0

        self.label = Label(master)
        self.label.pack()

        self.next_button = Button(master, text="Next", command=self.next_image)
        self.next_button.pack(side="right")

        self.prev_button = Button(master, text="Previous", command=self.prev_image)
        self.prev_button.pack(side="left")

        self.display_image(self.current_index)

    def process_image(self, image_path):
        image = cv2.imread(image_path)
        results = self.model.predict(source=image)
        annotated_image = results[0].plot()  
        return annotated_image

    def display_image(self, index):
        image_path = os.path.join(self.image_folder, self.image_files[index])
        processed_image = self.process_image(image_path)
        image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)

        self.label.config(image=image_tk)
        self.label.image = image_tk
        self.master.title(f"Image {index + 1} of {len(self.image_files)}")

    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.display_image(self.current_index)

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_image(self.current_index)

def main():
    root = Tk()
    root.title("YOLOv8 Image Labeler")

    model_path = filedialog.askopenfilename(title="Select YOLOv8 model file")
    image_folder = filedialog.askdirectory(title="Select Image Folder")

    if model_path and image_folder:
        app = ImageLabeler(root, model_path, image_folder)
        root.mainloop()

if __name__ == "__main__":
    main()
