from flask import Flask, render_template, Response
import cv2
from detector import detect
import numpy as np
import sys
app = Flask(__name__)


camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera 
        if not success:
            break
        else:
            # cv2.putText(frame,"intruder",(10,10+30),cv2.FONT_HERSHEY_SIMPLEX, 1, np.array([255, 0, 0]),1,cv2.LINE_AA)
            cv2.putText(frame,"intruder",(10,10+30),cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 0, 0],1,cv2.LINE_AA)
            cv2.imshow("change",frame)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            # ret, buffer = cv2.imencode('.jpg', frame)
            # frame = buffer.tobytes()
            # yield (b'--frame\r\n'
            #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


if __name__ == '__main__':
    gen_frames()