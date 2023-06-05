from picamera.array import PiRGBArray
from picamera import PiCamera

from time import sleep
import time
import cv2 as cv
from detectors import Detectors
import numpy as np
import math

import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory

pigpio_factory = PiGPIOFactory()
servo1 = gpiozero.AngularServo(17,min_angle=-90, max_angle=90, min_pulse_width=0.0005, max_pulse_width=0.0025,pin_factory=pigpio_factory)
servo2 = gpiozero.AngularServo(18,min_angle=-90, max_angle=90, min_pulse_width=0.0005, max_pulse_width=0.0025,pin_factory=pigpio_factory)


# initialize the camera
try:
    camera = PiCamera()
except:
    print("No camera connected")
    exit()
else:
    camera.resolution = (320,240)
    camera.framerate = 30
rawCapture = PiRGBArray(camera)
ballDefault = 0
ballPos = 0
# Set PID parameters
# kp = 0.07
# ki = 0.05
# kd = 0

kp = 0.075
ki = 0.00000
kd = 0.0000000


class FPSMeas:
    def __init__(self):
        self.init_time = time.time()
        self.counter = 0
        self.fps = 0
        
    def tick(self):
        self.counter += 1
        now = time.time()
        elapsed = now-self.init_time
        if elapsed > 5:
            self.fps = self.counter / elapsed
            self.counter = 0
            self.init_time = now
            print(f"{self.fps} fps")
            
class PID:
    
    def __init__(self, kp, ki, kd, set_pt, dt=None):
        # Set initial error and control values
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        
        self.val = 0
        self.set_pt = set_pt
        self.last_time = time.time()

        self.prev_err_x = 0.0
        self.integral_x = 0.0
        self.prev_err_y = 0.0
        self.integral_y = 0.0
        
        self.max_rate = 0.4
        self.last_output_x = 0
        self.last_output_y = 0
        
        
    def set_input(self,val):
        self.val = val
        if self.dt is None:
            now = time.time()
            self.dt = now - self.last_time
            self.last_time = now
        
    
    def get_output(self):
        x = self.correct_x()
        y = self.correct_y()
        print("the error is ",x ," and ", y)
        return [x/9, y/8]
    
    def correct_x(self):
        error_x =  self.val[0] - self.set_pt[0]
        self.integral_x = self.integral_x + error_x * self.dt
        derivative_x = (error_x - self.prev_err_x)/self.dt
        self.prev_err_x = error_x
        
        output_x = error_x*self.kp + self.integral_x*self.ki + derivative_x*self.kd
        rate = max(-self.max_rate, min(self.max_rate, output_x - self.last_output_x))
        output_x = self.last_output_x + rate
        self.last_output_x = rate
        
        return output_x
    
    def correct_y(self):
        error_y =  self.val[1] - self.set_pt[1]
        self.integral_y = self.integral_y + error_y * self.dt
        derivative_y = (error_y - self.prev_err_y)/self.dt
        self.prev_err_y = error_y
        
        output_y = error_y*self.kp + self.integral_y*self.ki + derivative_y*self.kd
        rate = max(-self.max_rate, min(self.max_rate, output_y - self.last_output_y))
        output_y = self.last_output_y + rate
        self.last_output_y = rate
        
        return output_y

def error_handling(rr, cc):
    if rr.size > 0 or cc.size > 0:
        return True
    return False

def check_ball_radius(rr):
    if rr > 10 and rr < 20:
        return True
    return False

def ball_tolerance(error_x, error_y):
    if (abs(error_x) < 20 and abs(error_y) < 20):
        return False
    return True
    

def pid_correction(values):
    if values[0] > 0.8:
        values[0] = 0.8
    elif values[0] < -0.8:
        values[0] = -0.8
        
    if values[1] > 0.8:
        values[1] = 0.8
    elif values[1] < -0.8:
        values[1] = -0.8
    
    ser1 = int((((values[0] + 0.8) * 115) / 1.6)-64)
    ser2 = int((((values[1] + 0.8) * 115) / 1.6)-62)
    print(ser1,ser2)

    servo1.angle = ser1
    servo2.angle = ser2
    #print(f"Servo 1= {servo1.angle:4.1f}; Servo 2 = {servo2.angle:4.1f}")
    
def ball_tracking():
    servo2.angle = -6
    servo1.angle = -6
    # Allow camera to wakeup
    sleep(0.1)
    # Capture from camera
    myPID = PID(kp, ki, kd, (160,120))
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
        image = frame.array
        
    #     operation on the frame
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 80, 255, cv.THRESH_BINARY)
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
   
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
            cr = np.sum(rr)/rr.size
            cc = np.sum(cc)/cc.size
            rr = np.sqrt(rr.size/np.pi)
            cv.circle(thresh, (int(cc),int(cr)), int(rr), (44,236,6), thickness=2, lineType=8, shift=0)
            ballPos = (cc,cr)
            
        #     Correct ball position proportionally
            if check_ball_radius(rr):
                myPID.set_input(ballPos)
                values = myPID.get_output()
                pid_correction(values)
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
