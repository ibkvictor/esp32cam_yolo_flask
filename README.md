# Home Surveillance Project with esp32 cam

## Introduction
This is a home surveillance project with esp32 cam, flask, and opencv using the YOLOv5n6 object detection model

## Instruction
### Installation of Required Packages
Install required packages from requirements.txt using:
	`pip install -r requirements.txt`


### Install Esp32 cam and esp32 libraries
Ensure you have the arduino ide esp32 cam package package installed on your computer. I have provided the esp32cam library in the `library` folder

### Compile and Upload sketch to esp32cam
open the Arduino sketch file `sketch\esp32cam_objectdetection.ino` in the Arduino IDE change the network credentials and upload to your esp32cam.

### Change email credentials
Change the email address and password in app.py. If you are using gmail, ensure that the less secure apps setting is switched on. You can check here for more details. [My google account activity settings](https://www.google.com/settings/security/lesssecureapps)

### Run
```python
	flask run
```

## Updates
- Before running the flask app, check the ip address of the esp32 from the serial monitor and set the image quality in `app.py`. Replace the ip address of the esp32 cam with the 

## TODO
- Concurrency to improve frame rate
	- contact me if you can help @victorezekielib on twitter or my @ibkvictor github account

