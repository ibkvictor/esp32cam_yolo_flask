# Author - @ibkvictor
# Github - ibkvictor@github.com

from flask import Flask, render_template, Response, request # web application creation
import cv2 # model inferencing and image processing
import numpy as np # required for cv2
import urllib.request # get esp 32 server responses
import time # to log the time for counting and deactivating
import yagmail # mail client, easier than Flask-Mail
import os # generate relative paths


# email credentials
email = input("enter sender email address:   ")
password = input("enter recipient's password:    ")
receipient_email = input("enter recipients email address:    ")

# esp 32 url
url = input("esp 32 cam response url:   ") # url esp32 broadcast, subject to change #'http://192.168.23.13/cam-lo.jpg'

# model classes
CLASSES_FILE = os.path.join("labels", "coco.names") # constant 80 classes
ONNX_FILE = os.path.join("models", "yolov5n6.onnx") # yolo model

# flask app
app = Flask(__name__)
app.debug = True

t = time.perf_counter() # time of detection
mail_time = None # time last email was sent
counter = 0 # number of times an intruder is detected
interval_mins = 20 # how long till next email if intruder is detected
action = "activate" # deactivate or activate
frames_per_second = 1 # number of frames per second. too high a problem and too low is too slow

def handle_person(image):
    global action
    global t
    global counter
    global mail_time
    global interval_mins
    if counter == 0:
        t = time.perf_counter()

    counter += 1
    if (time.perf_counter() - t <= 15) and (counter >= 9):
        if not mail_time:
            checker = time.perf_counter()
            print(action)
            print(mail_time)
            if action == "activate":
                print(send_mail(image))
            print(time.perf_counter() - checker, "time checker")
            t = time.perf_counter()
            mail_time = t
            counter = 0
        else:
            if (mail_time - time.perf_counter() >= (60 * interval_mins)):
                if action == "activate":
                    print(action)
                    print(mail_time)
                    print(send_mail())
            t = time.perf_counter()
            mail_time = t
            counter = 0

    elif (t - time.perf_counter() > 15) and (counter < 12):
        counter = 1
        t = time.perf_counter()
    elif (time.perf_counter() - t > 15) and (counter >= 9):
        counter = 1
        t = time.perf_counter()
    print(counter)

def send_mail(image):
    host_url = "http://127.0.0.1:5000/"
    yagmail.register(email, password)
    yag = yagmail.SMTP(email)
    subject = "!INTRUDER ALERT FROM YOUR HOME SURVEILLANCE CAM!"
    ret, buffer = cv2.imencode('.jpg', image)
    frame = buffer.tobytes()
    contents = [rf"""
                               Caution: There is an intruder in your house
        
                                You can deactivate this message by going to {host_url} on your local network
                                <img src = "data:image/jpeg;base64, {frame}>
                                                Thank you :)"""]
    yag.send(receipient_email, subject, contents)
    return "Sent"

def detect_person():
    global frames_per_second
    global counter
    while True:
        requests = [urllib.request.urlopen(url) for i in range(frames_per_second)]
        for request in requests:
            array = np.array(bytearray(request.read()),dtype=np.uint8)
            img = cv2.imdecode(array,-1)
            classes = []
            net = cv2.dnn.readNet(ONNX_FILE)
            with open(CLASSES_FILE,"r") as f:
                classes = [line.strip() for line in f.readlines()]
            
            colors= np.random.uniform(0,255,size=(len(classes),3))
            layer_names = net.getLayerNames()
            outputlayers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

            input_path = "Lena-Soederberg-256x256-JPEG-image-77-Kbytes.jpg"

            # img = cv2.imread(input_path)
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
                    if confidence > 0.5:
                        center_x= int(detection[0]) * (width/640)
                        center_y= int(detection[1]) * (height/640)
                        w = int(detection[2] * (height/640))
                        h = int(detection[3] * (width/640))

                        x=int((center_x - w/2))
                        y=int((center_y - h/2))

                        boxes.append([x,y,w,h]) 
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            print(len(boxes))
            indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.6)

            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)):
                if (i in indexes):
                    x,y,w,h = boxes[i]
                    label = str(classes[class_ids[i]])
                    if label == "person":
                        handle_person(img)
                        label += str(counter)
                        color = colors[class_ids[i]]
                        cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
                        cv2.putText(img,label,(x,y+30),cv2.FONT_HERSHEY_SIMPLEX, 1,color,1,cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(detect_person(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=["POST", "GET"])
def index():
    global action
    if request.method == 'POST':
        if request.form.get('activate') == 'activate':
            action = "activate"
        elif  request.form.get('deactivate') == 'deactivate':
            action = "deactivate"
            
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(threaded = True, debug=True)