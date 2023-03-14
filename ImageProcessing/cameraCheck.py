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
detector = Detectors()
ball_pose = 0

# Allow camera to wakeup
sleep(0.1)
# Capture from camera

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    
#     crop image
    image = image[130:300, 210:400]
    
#     operation on the frame
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    #inverted = cv.bitwise_not(gray)
    ret, thresh = cv.threshold(gray, 80, 255, cv.THRESH_BINARY)
    
    rr,cc = np.nonzero(thresh>0)
    if rr.size:
        cr = np.sum(rr)/rr.size
        cc = np.sum(cc)/cc.size
        rr = np.sqrt(rr.size/np.pi)
        cv.circle(thresh, (int(cc),int(cr)), int(rr), (44,236,6), thickness=2, lineType=8, shift=0)
#     Show the image
    cv.imshow("Frame", thresh)
    key=cv.waitKey(1) & 0xFF
#     Clear stream
    rawCapture.truncate(0)
    if key == ord("q"):
        break