import random
import os
from tqdm import tqdm
import cv2
import numpy as np
import linecache


if not os.path.exists("background"):
	os.mkdir("background")

if not os.path.exists("temp"):
	os.mkdir("temp")

if not os.path.exists("yolov5"):
	os.mkdir("yolov5")
	
if not os.path.exists("yolov5/labels"):
	os.mkdir("yolov5/labels")
	
if not os.path.exists("yolov5/images"):
	os.mkdir("yolov5/images")


background_path = "background/"
trap_path = "crabtrap/"
temp_saving_path = "temp/"
count = 0
hits_file = []
fake_hits = {}

#generating fake images. the function slice the height of background images by the width of that same image_count
#for each of those sliced image we add a crabtrap ramdomly than we same the position of the crabtrap for further processing
def process_fake_image():
    list_trap_path = []
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
                nb_image = round(height/width)
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
                        trap_x = random.randint(100,crop_width-600)
                        trap_y = random.randint(100, crop_height-300)
                        #print("trap position :",trap_x,trap_y)
                        #print(list_trap_path[i])
                        trap = cv2.imread(list_trap_path[i], 1)
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
                        
                        #img[trap_y:trap_height+trap_y, trap_x:trap_width+trap_x] = trap
                        global count
                        img_name = "fake-crabtrap" + str(count) + ".png"
                        img_path = temp_saving_path + img_name
                        cv2.imwrite(img_path, img)
                        
                        x_center = str(x_center) 
                        y_center = str(y_center)
                        width = str(trap_width)
                        height = str(trap_height)
                        
                        hits_file.append([x_center,y_center,width,height])
                        fake_hits.update({img_name:hits_file[count]})
                        count += 1

                    break;
                    start_height = end_height
                    end_height += delta_height
                    #print("start height ", start_height)
                    #print("end height ", end_height)
                    #print("generating images #", count)
        break;                          
process_fake_image()
print(count," images created")
if(count == len(fake_hits)):
    print("number of labels and images are equal :) ")
    
else:
    print("number of labels and images are NOT equal !!")  

#print("size of hit", len(hits_file[0]))
#print("size of hits dictionary", len(fake_hits))
#for image in dict_hits.keys():
#    print(image)
#    print(fake_hits.get(image))


temp_path = "temp/"
saving_path = "yolov5/"
list_width = []
list_height = []
list_image = []

def get_images_dimension():
    print("analyze images dimensions")            
    for image in tqdm(os.listdir(temp_path)):
        if ".jpg" or ".png" in image:
            #print(image)
            img = cv2.imread(temp_path + image, 1)
            height, width, chan = img.shape
            list_width.append(width)
            list_height.append(height)

    max_height = np.max(list_height)
    return max_height
    
new_img_dimension = get_images_dimension()
print("max dimension: ", new_img_dimension)

def read_hit_file_at_line(File, line):
    data = linecache.getline(File, line)
    #print(data)
    hit = data.split()
    return hit

#read_hit_file(saving_path + "labels/fake-crabtrap0.txt", 1)



final_dimension = 0
def format_and_normalise(dimension):
    print("format images to same dimension ")
    for image in tqdm(os.listdir(temp_path)):
        if ".jpg" or ".png" in image:
            #print(image)
            img = cv2.imread(temp_path + image, 1)
            height, width, chan = img.shape
            new_height = (round(dimension/16)+1)*16 # image dimension needs to be a multiple of 16
            new_width = new_height # image needs to be squared
            delta_width = new_width - width
            delta_height = new_height - height
            
            #print("delta height",delta_height)
            #print("delta width",delta_width)
            pad_img = cv2.copyMakeBorder(img, 0, delta_height, 0, delta_width, cv2.BORDER_CONSTANT,None, value = 0)
            pad_img = cv2.resize(pad_img,(1280,1280), interpolation = cv2.INTER_AREA)
            global final_dimension
            final_dimension = pad_img.shape[0]
            cv2.imwrite(saving_path + "images/" + image, pad_img)
            
            # get position of crabptrap processed by process_fake_image() and normalise the position with new dimension
            pad_img_width, pad_img_height, chan = pad_img.shape
            trap_name = image[:-4]
            if image in fake_hits.keys():
                
                hit = fake_hits.get(image)
                normalized_x_center = str(round((int(hit[0]) / pad_img_width), 6))
                normalized_y_center = str(round((int(hit[1]) / pad_img_height), 6))
                normalized_width = str(round((int(hit[2]) / pad_img_width), 6))
                normalized_height = str(round((int(hit[3]) / pad_img_height), 6))
                # only generating images for class zero which is crabtrap
                f = open(saving_path + "labels/" + trap_name + ".txt", "w")
                f.write("0 " + normalized_x_center + " " + normalized_y_center + " " + normalized_width + " " + normalized_height)
                f.close
                
            # without this part theres no image from opensidescan that can be process            
            else:
                hit_file_name = image[:-4]
                hit_file_name += ".txt"
                print(hit_file_name)
                with open(hit_file_name, "r") as hit_file:
                    f = open(hit_file, "w")
                    nb_lines = len(image.readLines())
                    for i in range(nb_lines - 1):
                        hit = read_hit_file_at_line(hit_file_name, i)
                        CLASS = str(hit[0])
                        normalized_x_center = str(round((int(hit[1]) / pad_img_width), 6))
                        normalized_y_center = str(round((int(hit[2]) / pad_img_height), 6))
                        normalized_width = str(round((int(hit[3]) / pad_img_width), 6))
                        normalized_height = str(round((int(hit[4]) / pad_img_height), 6))
                        # only generating images for class zero which is crabtrap
                        f.write(CLASS + normalized_x_center + " " + normalized_y_center + " " + normalized_width + " " + normalized_height)
                    f.close
                    
         
format_and_normalise(new_img_dimension)
print("final dimension = ", final_dimension)

print("verify number of images = number of labels")
nb_images = len([name for name in tqdm(os.listdir('yolov5/images')) if os.path.isfile(name)])
nb_labels = len([name for name in tqdm(os.listdir('yolov5/labels')) if os.path.isfile(name)])
if(nb_labels == nb_images):
    print("number of labels and images are equal :) ")
    
else:
    print("number of labels and images are NOT equal !!")
    

