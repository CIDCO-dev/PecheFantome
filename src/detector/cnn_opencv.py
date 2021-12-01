#import torch
#import torchvision
#from torchvision import transforms
#from PIL import Image
import cv2
import numpy as np

def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    #print(net.getUnconnectedOutLayers())
    return [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]

def findObjects(outputs,img):
	confThreshold = 0.1
	nmsThreshold = 0.1
	hT = img.shape[0]
	wT = img.shape[1]
	bbox = []
	classIds = []
	confs = []
	for output in outputs:
		for out in output:
			#print(det.shape)
			for det in out:
				if(det[4] > 0.3):
					scores = det[5:]
					classId = np.argmax(scores)
					confidence = scores[classId]
					if confidence > confThreshold:
						width = int(det[2])
						height = int(det[3])
						top_left_x = int((det[0] - width))
						top_left_y = int((det[1] -70 - height)) # ouin pas sure que ca soit la bonne solution
						bbox.append([top_left_x, top_left_y, width, height])
						classIds.append(classId) # ca c'est bon
						confs.append(float(confidence))
						#print(left, top, width, height) 
						#print(det[0],det[1],det[2],det[3])
						
				        
	indices = cv2.dnn.NMSBoxes(bbox, confs,confThreshold,nmsThreshold)

	for i in indices:
		print(len(indices))
		box = bbox[i]
		x,y,w,h = box[0], box[1], box[2], box[3]
		cv2.rectangle(img, (x,y),(x+w,y+h),(255,0,255),2)
		#cv2.putText(img,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(255,0,255),2)
		print(classIds[i])
		cv2.imshow('Image', img)
		cv2.waitKey(2000)



#Main 
onnx_model_path = "best-batch1.onnx" 
sample_image = "model-test-data/crabtrap2-1_5.png"
 
#The Magic:
net =  cv2.dnn.readNetFromONNX(onnx_model_path) 
image = cv2.imread(sample_image)
#print(image)

blob = cv2.dnn.blobFromImage(image, 1.0 / 255, (640,640),(0, 0, 0), swapRB=True, crop=False)

#blob2 = numpy.repeat(blob,4,0)
#print(blob2.shape)
net.setInput(blob)
preds = net.forward(getOutputsNames(net))



findObjects(preds,image)
#cv2.imshow('Image', image)
#cv2.waitKey(10000)





