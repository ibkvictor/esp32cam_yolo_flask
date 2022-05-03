import cv2
import base64
from flask import Flask


app = Flask(__name__)

def hello_world():
    image = cv2.imread("/Users/user/Documents/Arduino/esp32cam_objectdetection/src/Lena-Original-Image-512x512-pixels.png")
    ret, buffer = cv2.imencode('.jpg', image)
    frame = base64.b64encode(buffer)
    # print(frame)
    # with open("/Users/user/Documents/Arduino/esp32cam_objectdetection/src/encoded_image.txt", "wb") as file:
    #     file.write(frame)
    return f"<img src = 'data:image/jpeg;base64,{frame}'>"


if __name__ == '__main__':
    app.run(threaded = True, debug=True)


