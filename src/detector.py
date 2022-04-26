import cv2
import matplotlib.pyplot as plt
#import cvlib as cv
import urllib.request
import os
import numpy as np
import time
#from cvlib.object_detection import draw_bbox

# WEIGHTS_FILE = "yolov3.weights"
# CONFIG_FILE = "yolov3.cfg"
CLASSES_FILE = "coco.names" # constant 80 classes
ONNX_FILE = "yolov5n6.onnx"

# def detect():
#     while True:
#         # img_resp=urllib.request.urlopen(url='http://192.168.10.162/cam-hi.jpg')
#         # imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
#         # im = cv2.imdecode(imgnp,-1)
#         im= cv2.imread("Lena-Soederberg-256x256-JPEG-image-77-Kbytes.jpg")
#         type(im) 
#         bbox, label, conf = cv.detect_common_objects(im)
#         print(type(im))

#         im = draw_bbox(im, bbox, label, conf)
        
#         cv2.imshow('detection',im)
#         key=cv2.waitKey(5)
#         if key==ord('q'):
#             break

def detect():
    while True:
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        im = cv2.imdecode(imgnp,-1)
        net = cv2.dnn.readNet(ONNX_FILE)
        classes = []
    with open(CLASSES_FILE,"r") as f:
        classes = [line.strip() for line in f.readlines()]

    colors= np.random.uniform(0,255,size=(len(classes),3))
    layer_names = net.getLayerNames()
    outputlayers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    input_path = "Lena-Soederberg-256x256-JPEG-image-77-Kbytes.jpg"

    img = cv2.imread(input_path)
    height,width,channels = img.shape
    blob = cv2.dnn.blobFromImage(img,1/256,(640,640),(0,0,0),True,crop=False)
    net.setInput(blob)
    outs = net.forward(outputlayers)
    class_ids=[]
    confidences=[]
    boxes=[]
    for out in outs:
        for detection in out[0]:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = detection[4]
            if confidence > 0.25:
                center_x= int(detection[0]) * (width/640)
                center_y= int(detection[1]) * (width/640)
                w = int(detection[2] * (width/640))
                h = int(detection[3] * (width/640))

                x=int((center_x - w/2))
                y=int((center_y - h/2))

                boxes.append([x,y,w,h]) 
                confidences.append(float(confidence))
                class_ids.append(class_id)
    print(class_ids)

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.3,0.6)
    print(indexes)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            print(boxes[i])
            print(img.shape)
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            cv2.putText(img,label,(x,y+30),cv2.FONT_HERSHEY_SIMPLEX, 1,color,1,cv2.LINE_AA)
    
    return(img)
            # cv2.imshow('detection',img)
            # cv2.waitKey(1)
            # cv2.destroyAllWindows()
    # cv2.imwrite('image2.png',img)


    # im= cv2.imread("Lena-Soederberg-256x256-JPEG-image-77-Kbytes.jpg")
    # print(os.getcwd())
    # return type(im)