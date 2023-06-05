from picamera.array import PiRGBArray
from picamera import PiCamera

from time import sleep
import cv2 as cv
from detectors import Detectors
import numpy as np
import math

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

pigpio_factory = PiGPIOFactory()
servo1 = Servo(17,pin_factory=pigpio_factory)
servo2 = Servo(18,pin_factory=pigpio_factory)

# initialize the camera
camera = PiCamera()
camera.resolution = (320,208)
camera.framerate = 32
rawCapture = PiRGBArray(camera)
ballDefault = 0
ballPos = 0
kp = 5

def error_handling(rr, cc):
    if rr.size > 0 or cc.size > 0:
        return True
    return False

def check_ball_radius(rr):
    print("radius is ", rr)
    if rr > 10 and rr < 25:
        return True
    return False
def ball_tolerance(error_x, error_y):
    print("error x", error_x)
    print("error y", error_y)
#     if (error_x < 20 and error_y < 20):
#         return False
    return True
    

def pid_correction(ballDefault, ballPos):
    error_x = ballDefault[0]- ballPos[0]
    error_y = ballDefault[1]- ballPos[1]
    if ball_tolerance(error_x, error_y):
        servo_posx = kp * error_x
        servo_posy = kp * error_y
        print("Servo posx", servo_posx)
        print("Servo posy", servo_posy)
        servo1.value = max(-1, min(1, servo_posx))
        servo2.value = max(-1, min(1, servo_posy))

        print("Servo value 1", servo1.value)
        print("Servo value 2", servo2.value)
    return
    
def ball_tracking():
    servo2.value = 0
    servo1.value = 0
    # Allow camera to wakeup
    sleep(0.1)
    # Capture from camera

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        
    #     crop image, this will be adapted to the installation
#         image = image[70:370, 150:470]
        
        
    #     operation on the frame
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 80, 255, cv.THRESH_BINARY)
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
#         lower_white = np.array([0,0,200], np.uint8)
#         upper_white = np.array([179,30,255], np.uint8)
        lower_green = np.array([40,50,50], np.uint8)
        upper_green = np.array([80,255,255], np.uint8)
    #   Threshold to only get green colors
        thresh = cv.inRange(hsv,lower_green, upper_green)
        
    #   Bitwise and mask and original image
        res = cv.bitwise_and(image, image,mask=thresh)
    #    center of image,where we want the ball to be
        cx = thresh[:,0]
        cy = thresh[0,:]
        posx = cy.size/2
        posy = cx.size/2
        ballDefault = (posx,posy)
        cv.circle(thresh, (int(posx),int(posy)), int(2), (44,236,6), thickness=2, lineType=8, shift=0)
        
        
        rr,cc = np.nonzero(thresh>0)
    #   Check if ball is detected
        if rr.size > 0:
            print("Found an object")
            cr = np.sum(rr)/rr.size
            cc = np.sum(cc)/cc.size
            rr = np.sqrt(rr.size/np.pi)
            cv.circle(thresh, (int(cc),int(cr)), int(rr), (44,236,6), thickness=2, lineType=8, shift=0)
            ballPos = (cc,cr)
        #     Correct ball position proportionally
            if check_ball_radius(rr):
                pid_correction(ballDefault,ballPos)
                print("Default", ballDefault)
                print("position", ballPos)
        cv.imshow("Frame", thresh)
        
        key=cv.waitKey(1) & 0xFF
    #     Clear stream
        rawCapture.truncate(0)
        if key == ord("q"):
            break
    
def main():
    ball_tracking()

if __name__=="__main__":
    main()