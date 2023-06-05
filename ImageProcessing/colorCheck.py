from picamera.array import PiRGBArray
from picamera import PiCamera

from time import sleep
import cv2 as cv
from detectors import Detectors
import numpy as np

# initialize the camera
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera)
ballDefault = 0
ballPos = 0

# Allow camera to wakeup
sleep(0.1)
# Capture from camera

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    
#     crop image, this will be adapted to the installation
    image = image[150:300, 350:550]
    
    

#     Normalize hsv values
    lH = (51/360)*180
    lS = (45/100)*255
    lV = (64/100)*255
    uH = (65/360)*180
    uS = (100/100)*255
    uV = (100/100)*255
    #     operation on the frame
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    lower_yellow = np.array([20,100,100], np.uint8)
    upper_yellow = np.array([40,255,255], np.uint8)
#   Threshold to only get yellow colors
    mask = cv.inRange(hsv,lower_yellow, upper_yellow)
    
#   Bitwise and mask and original image
    res = cv.bitwise_and(image, image,mask=mask)
    
  
    cv.imshow("og", image)
    cv.imshow("mask", mask)
    cv.imshow("Frame", res)
    key=cv.waitKey(1) & 0xFF
#     Clear stream
    rawCapture.truncate(0)
    if key == ord("q"):
        break