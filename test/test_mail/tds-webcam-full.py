# from flask import Flask, Response
# import cv2
# import matplotlib.pyplot as plt
# import cvlib as cv
# import urllib.request
# import numpy as np
# from cvlib.object_detection import draw_bbox
# import concurrent.futures
# from detector import detect

# url='http://192.168.1.61/cam-lo.jpg'

# app = Flask(__name__)

# img_resp=urllib.request.urlopen(url)
# imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
# im = cv2.imdecode(imgnp,-1)


# # video = cv2.VideoCapture(0)
# # face_cascade = cv2.CascadeClassifier()
# # face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))

# @app.route('/')
# def index():
#     return "Default Message"

# def gen(video):
#     while True:
#         success, image = video.read()
#         frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         frame_gray = cv2.equalizeHist(frame_gray)

#         #faces = face_cascade.detectMultiScale(frame_gray)
#         image = detect(frame_gray)
#         # for (x, y, w, h) in faces:
#         #     center = (x + w//2, y + h//2)
#         #     cv2.putText(image, "X: " + str(center[0]) + " Y: " + str(center[1]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
#         #     image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

#         #     faceROI = frame_gray[y:y+h, x:x+w]
#         ret, jpeg = cv2.imencode('.jpg', image)
        
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
#     global video
#     return Response(gen(video),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=2204, threaded=True)
