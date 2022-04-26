import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import urllib.request
import numpy as np
from cvlib.object_detection import draw_bbox

def detect():
    while True:
        # img_resp=urllib.request.urlopen(url='http://192.168.10.162/cam-hi.jpg')
        # imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        # im = cv2.imdecode(imgnp,-1)
        im = cv2.imread("Lena-Soederberg-256x256-JPEG-image-77-Kbytes.jpg")
 
        bbox, label, conf = cv.detect_common_objects(im)
        im = draw_bbox(im, bbox, label, conf)
        print(type(im))
        
        cv2.imshow('detection',im)
        key=cv2.waitKey(5)
        if key==ord('q'):
            break

if __name__ == "__main__":
    detect()
