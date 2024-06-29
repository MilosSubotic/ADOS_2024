


from roboflow import Roboflow
rf = Roboflow(api_key="fN5PpF88caTri9mVb2C6")
project = rf.workspace("ados-z5p8o").project("capacitors_resistors")
version = project.version(3)
dataset = version.download("yolov8")
