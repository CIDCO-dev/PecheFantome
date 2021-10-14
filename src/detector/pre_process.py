import random
import os
from tqdm import tqdm
import cv2
import numpy as np


if not os.path.exists("background"):
	os.mkdir("background")

if not os.path.exists("temp"):
	os.mkdir("temp")
	

background_path = "background/"
trap_path = "manual_edits/"
saving_path = "temp/"
list_trap_path = []
count = 0
def process_fake_image():
    print("load crabtrap")
    for trap in tqdm(os.listdir(trap_path)):
    
        if ".png" in trap:
            list_trap_path.append(trap_path + trap)
    #print(len(list_trap))
    print("generating images")
    
    for image in tqdm(os.listdir(background_path)):
    
        if ".png" in image:
            #print(image)
            img = cv2.imread(background_path + image, 1)
            height, width, chan = img.shape
            #print(img.shape)
            
            if (height / width) > 1: # the number of time width can fit in height is the number of images created out of one file
                nb_image = int(height/width)
                #print("nb image ", nb_image)
                delta_height = int(height / nb_image)
                #print("delta h ", delta_height)
                start_height = 0
                start_width = 0
                end_height = delta_height
                end_width = width
                image_count = 0
                
                while image_count < nb_image:
                    img = cv2.imread(background_path + image, 1)
                    crop_img = img[start_height:end_height, start_width:end_width]
                    #print("crop region ",start_height, start_width , end_height , end_width )
                    crop_height, crop_width, chan = crop_img.shape
                    #print("crop shape" ,crop_img.shape)
                    image_count +=1
                    # each image will have X different crabpot
                    for i in range(len(list_trap_path)-1):
                        trap_x = random.randint(100,round(crop_width*0.75))
                        trap_y = random.randint(100, crop_height-300)
                        #print("trap position :",trap_x,trap_y)
                        index = random.randrange(len(list_trap_path)-1)
                        #print(list_trap_path[index])
                        trap = cv2.imread(list_trap_path[index], 1)
                        trap_height, trap_width, chan = trap.shape
                        #print("trap shape ",trap.shape)
                        #print("end trap",trap_width+trap_x, trap_height+trap_y)
                        #print("crop shape ", crop_img.shape)
 
                        mask = 255 *np.ones(trap.shape, trap.dtype)
                        x_center = trap_x + (trap_width // 2)
                        y_center = trap_y + (trap_height // 2)
                        #print("center x,y : ",x_center, y_center)
                        center = (y_center, x_center)
                        img = cv2.seamlessClone(trap, crop_img, mask, center, cv2.MIXED_CLONE)
                        #crop_img[trap_y:trap_height+trap_y, trap_x:trap_width+trap_x] = trap
                        global count
                        Count = str(count)
                        cv2.imwrite(saving_path + "fake-crabtrap" + Count + ".png", img)
                        normalized_x_center = str(x_center / crop_width)
                        normalized_y_center = str(y_center / crop_height)
                        normalized_width = str(trap_width / crop_width)
                        normalized_height = str(trap_height / crop_height)
                        
                        # only generating images for class zero which is crabtrap
                        f = open(saving_path + "fake-crabtrap" + Count + ".txt", "w")
                        f.write("0 " + normalized_x_center + " " + normalized_y_center + " " + normalized_width + " " + normalized_height)
                        f.close
                        count += 1
                        #print("\n")

                    start_height = end_height
                    end_height += delta_height
                    #print("start height ", start_height)
                    #print("end height ", end_height)
                    #print("generating images #", count)
                            
process_fake_image()
print(count," images created")

if not os.path.exists("yolov5"):
	os.mkdir("yolov5")
	
if not os.path.exists("yolov5/labels"):
	os.mkdir("yolov5/labels")
	
if not os.path.exists("yolov5/images"):
	os.mkdir("yolov5/images")


path = "temp/"
saving_path = "yolov5/"
list_width = []
list_height = []
list_image = []
def move_labels():
    print("move labels")
    for Files in tqdm(os.listdir(path)):
        if ".txt" in Files:
            os.rename(path + Files, saving_path + "labels/" + Files)
move_labels()

def pre_process():
    print("analyze images dimensions")            
    for image in tqdm(os.listdir(path)):
        if ".jpg" or ".png" in image:
            #print(image)
            img = cv2.imread(path + image, 1)
            height, width, chan = img.shape
            list_width.append(width)
            list_height.append(height)

    max_width = np.max(list_width)
    max_height = np.max(list_height)

    print("format images to same dimension ")
    for image in tqdm(os.listdir(path)):
        if ".jpg" or ".png" in image:
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
            cv2.imwrite(saving_path + "images/" + image, pad_img)
            
pre_process()
