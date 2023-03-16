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
    image = image[150:330, 275:500]
    
    
#     operation on the frame
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    #inverted = cv.bitwise_not(gray)
    ret, thresh = cv.threshold(gray, 80, 255, cv.THRESH_BINARY)
#    center of image,where we want the ball to be
    cx = thresh[:,0]
    cy = thresh[0,:]
    posx = cy.size/2
    posy = cx.size/2
    ballDefault = (posx,posy)
    
    
    rr,cc = np.nonzero(thresh>0)
    if rr.size:
        cr = np.sum(rr)/rr.size
        cc = np.sum(cc)/cc.size
        rr = np.sqrt(rr.size/np.pi)
        cv.circle(thresh, (int(cc),int(cr)), int(rr), (44,236,6), thickness=2, lineType=8, shift=0)
        ballPos = (cr,cc)
#     Show the image
#     print("Default : ", ballDefault)
#     print("Actual : ", ballPos)
    cv.imshow("Frame", thresh)
    key=cv.waitKey(1) & 0xFF
#     Clear stream
    rawCapture.truncate(0)
    if key == ord("q"):
        break
