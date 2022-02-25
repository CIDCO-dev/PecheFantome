# Documentation for YOLO:

train : 
python3 PATH/yolov5/yolo_git_repo/yolov5/train.py --img 640 --batch 4 --epoch 10 --data PATH/yolov5/train_data/data2021.yaml --cfg yolov5x.yaml --device cpu

export model : 
python3 export.py --weights PATH/runs/train/exp3/weights/best.pt --img 1440 --batch 1

test model :
python3 PATH/PecheFantome/src/detector/train_data/test_model.py
or
python3 detect.py --weights weights/best.pt --img 1888 --source ../../train_data/test/



