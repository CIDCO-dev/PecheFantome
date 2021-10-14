import os
import torch

model = model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='home/glm/yolov5/yolo_git_repo/yolov5/runs/train/exp3/weights/best.pt')

path = "/home/glm/yolov5/train_data/test/"
imgs = [path + img for img in os.listdir(path)]

results = model(imgs)
results.print()
