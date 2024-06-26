import ultralytics

model = ultralytics.YOLO('yolov8n.pt')

results = model.train(
    data='/home/tonke9/ADOS24/ADOS_2024/kultura+korov/data.yaml',
    epochs=10,
    batch=4,
    imgsz=640,
    device=0,
    cache=False,
    workers=8,
    project='runs/detect',
    name='train42',
    exist_ok=False,
    half=True,
)
