import cv2
from yolo_segmentation import YOLOSEG
import cvzone
import numpy as np

ys = YOLOSEG("best_1.pt")

with open("coco1.txt", "r") as my_file:
    class_list = my_file.read().split("\n")

video_path = "/home/maja/Documents/6_semestar/ADOS/video2.mp4"  # Prilagodite putanju do vašeg videa
cap = cv2.VideoCapture(video_path)

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1020, 500))
    overlay = frame.copy()
    alpha = 0.5

    bboxes, classes, segmentations, scores = ys.detect(frame)
    for bbox, class_id, seg, score in zip(bboxes, classes, segmentations, scores):
        (x, y, x2, y2) = bbox
        c = class_list[class_id]

        # Convert segment to numpy array with correct dtype and reshape
        seg_np = np.array(seg, dtype=np.int32).reshape((-1, 1, 2))

        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 2)

        # Draw segment edges
        if seg_np.size > 0:
            cv2.polylines(frame, [seg_np], True, (0, 0, 255), 4)

        # Fill segment with color
        if seg_np.size > 0:
            cv2.fillPoly(overlay, [seg_np], (0, 0, 255))

        # Add transparency overlay
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Add class label text
        cvzone.putTextRect(frame, f'{c}', (x, y), 1, 1)

    # Show the frame
    cv2.imshow("RGB", frame)

    # Exit on 'Esc' key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
