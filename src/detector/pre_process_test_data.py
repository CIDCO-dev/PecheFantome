import os
from tqdm import tqdm
import cv2
import numpy as np

#pre process test data:
path = "raw_test_data/"

list_width = []
list_height = []
list_image = []
def pre_process():
    print("analyze images")
    for Files in tqdm(os.listdir(path)):
        if "jpg" in Files:
            #print(Files)
            img = cv2.imread(path + Files, 1)
            height, width, chan = img.shape
            #print(width)
            #print(height)
            list_width.append(width)
            list_height.append(height)


    max_width = np.max(list_width)
    max_height = np.max(list_height)
    if max_height == max_width :
        print("max height == max width")
    print("format images: ")
    for image in tqdm(os.listdir(path)):
        if "jpg" in image:
            #print(image)
            img = cv2.imread(path + image, 1)
            height, width, chan = img.shape
            new_height = (round(max_height/16)+1)*16 # image dimension needs to be a multiple of 16
            new_width = new_height # image needs to be squared
            delta_width = new_width - width
            delta_height = new_height - height
            
            #print("delta height",delta_height)
            #print("delta width",delta_width)
            pad_img = cv2.copyMakeBorder(img, 0, delta_height, 0, delta_width, cv2.BORDER_CONSTANT,None, value = 0)
            #list_image.append(pad_img)
            cv2.imwrite("test_data/"+image, pad_img)
            
pre_process()
for image in list_image:
    print(image.shape)
