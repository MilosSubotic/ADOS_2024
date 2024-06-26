#5_detect_test.py
#!/usr/bin/env python3

from ultralytics import YOLO
import glob
import cv2
from tkinter import *
from PIL import ImageTk, Image

# Load a model
model = YOLO("runs/detect/train424/weights/best.pt")

# Get image paths
imgs = glob.glob('/home/tonke9/ADOS24/ADOS_2024/kultura+korov/dataset/train/images/*.jpg')

# Function to detect objects and create image with bounding boxes
def detect_and_label_image(img_path):
    results = model(img_path)[0]
    res_plot = results.plot()

    # Convert the result image to a format that can be used by Tkinter
    img_rgb = cv2.cvtColor(res_plot, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    return ImageTk.PhotoImage(img_pil)

# Create Tkinter window
root = Tk()
root.title("Image Viewer")
root.geometry("700x700")

# Detect objects in images and create labels
List_images = [detect_and_label_image(img) for img in imgs]

# Functions for navigation
def forward(img_no):
    global label
    global button_forward
    global button_back
    global button_exit
    label.grid_forget()

    label = Label(image=List_images[img_no])
    label.grid(row=1, column=0, columnspan=3)
    button_forward = Button(root, text="forward", command=lambda: forward(img_no+1))

    if img_no == len(List_images) - 1:
        button_forward = Button(root, text="Forward", state=DISABLED)

    button_back = Button(root, text="Back", command=lambda: back(img_no-1))

    button_back.grid(row=5, column=0)
    button_exit.grid(row=5, column=1)
    button_forward.grid(row=5, column=2)

def back(img_no):
    global label
    global button_forward
    global button_back
    global button_exit
    label.grid_forget()

    label = Label(image=List_images[img_no])
    label.grid(row=1, column=0, columnspan=3)
    button_forward = Button(root, text="forward", command=lambda: forward(img_no + 1))
    button_back = Button(root, text="Back", command=lambda: back(img_no - 1))

    if img_no == 0:
        button_back = Button(root, text="Back", state=DISABLED)

    label.grid(row=1, column=0, columnspan=3)
    button_back.grid(row=5, column=0)
    button_exit.grid(row=5, column=1)
    button_forward.grid(row=5, column=2)

# Initial display
label = Label(image=List_images[0])
label.grid(row=1, column=0, columnspan=3)

button_back = Button(root, text="Back", command=lambda: back(0), state=DISABLED)
button_exit = Button(root, text="Exit", command=root.quit)
button_forward = Button(root, text="Forward", command=lambda: forward(1))

button_back.grid(row=5, column=0)
button_exit.grid(row=5, column=1)
button_forward.grid(row=5, column=2)

root.mainloop()
