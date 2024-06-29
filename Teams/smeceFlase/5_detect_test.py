#!/usr/bin/env python3


from ultralytics import YOLO

import glob

# Load a model
model = YOLO("C:/Users/user/Desktop/adosProj/ADOS_2024/Teams/smeceFlase/runs/detect/train6")

imgs = glob.glob('dataset/images/train/*.jpg')

'''
#model.predict(source='dataset/images/train/', show=True)
model(imgs[0])[0].show()

res_plot = model(imgs[0])[0].plot()
import cv2
cv2.imshow("res", res_plot)
'''


#result = model(imgs[0])[0]
#result.save(filename = "tmp.jpg")

# importing the tkinter module and PIL
# that is pillow module
from tkinter import *
from PIL import ImageTk, Image

def forward(img_no):
    global label
    global button_forward
    global button_back
    global button_exit
    label.grid_forget()

    label = Label(image=List_images[img_no-1])
    label.grid(row=1, column=0, columnspan=3)
    button_forward = Button(root, text="forward",
                        command=lambda: forward(img_no+1))

    if img_no == 4:
        button_forward = Button(root, text="Forward",
                                state=DISABLED)

    button_back = Button(root, text="Back",
                         command=lambda: back(img_no-1))

    button_back.grid(row=5, column=0)
    button_exit.grid(row=5, column=1)
    button_forward.grid(row=5, column=2)

def back(img_no):
    global label
    global button_forward
    global button_back
    global button_exit
    label.grid_forget()

    label = Label(image=List_images[img_no - 1])
    label.grid(row=1, column=0, columnspan=3)
    button_forward = Button(root, text="forward",
                            command=lambda: forward(img_no + 1))
    button_back = Button(root, text="Back",
                         command=lambda: back(img_no - 1))

    if img_no == 1:
        button_back = Button(root, text="Back", state=DISABLED)

    label.grid(row=1, column=0, columnspan=3)
    button_back.grid(row=5, column=0)
    button_exit.grid(row=5, column=1)
    button_forward.grid(row=5, column=2)

root = Tk()
root.title("Image Viewer")
root.geometry("700x700")

# Change the png file name a/c to your image 
image_no_1 = ImageTk.PhotoImage(Image.open(imgs[1]))
image_no_2 = ImageTk.PhotoImage(Image.open(imgs[2]))
image_no_3 = ImageTk.PhotoImage(Image.open(imgs[3]))
image_no_4 = ImageTk.PhotoImage(Image.open(imgs[4]))

List_images = [image_no_1, image_no_2, image_no_3, image_no_4]

label = Label(image=image_no_1)
label.grid(row=1, column=0, columnspan=3)

button_back = Button(root, text="Back", command=back,
                     state=DISABLED)

button_exit = Button(root, text="Exit",
                     command=root.quit)

button_forward = Button(root, text="Forward",
                        command=lambda: forward(1))

button_back.grid(row=5, column=0)
button_exit.grid(row=5, column=1)
button_forward.grid(row=5, column=2)

root.mainloop()