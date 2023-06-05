from picamera.array import PiRGBArray
from picamera import PiCamera

from time import sleep
import time
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

kp = 0.05
ki = 0.0
kd = 0


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
      
        
        
    def set_input(self,val):
        self.val = val
        if self.dt is None:
            now = time.time()
            self.dt = now - self.last_time
            self.last_time = now
        
    
    def get_output(self):
        x = self.correct_x()
        y = self.correct_y()
        return [x/10, y/10]
    
    def correct_x(self):
        error_x =  self.val[0] - self.set_pt[0]
        self.integral_x = self.integral_x + error_x * self.dt
        derivative_x = (error_x - self.prev_err_x)/self.dt
        self.prev_err_x = error_x
        
        output_x = error_x*self.kp + self.integral_x*self.ki + derivative_x*self.kd
        
        return output_x
    
    def correct_y(self):
        error_y =  self.val[1] - self.set_pt[1]
        self.integral_y = self.integral_y + error_y * self.dt
        derivative_y = (error_y - self.prev_err_y)/self.dt
        self.prev_err_y = error_y
        
        output_y = error_y*self.kp + self.integral_y*self.ki + derivative_y*self.kd
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
    

def pid_correction(ballDefault, ballPos):
    myPID = PID(kp, ki, kd, ballDefault)
    myPID.set_input(ballPos)
    values = myPID.get_output()
#     if values[0] > 0.7:
#         values[0] = 0.7
#     elif values[0] < -0.7:
#         values[0] = -0.7
#         
#     if values[1] > 0.7:
#         values[1] = 0.7
#     elif values[1] < -0.7:
#         values[1] = -0.7
#         
#     ser1 = round(values[0]/0.7, 2)
#     ser2 = values[1]/0.7
#     print(ser1, ser2)   
#     servo1.value = ser1
#     servo2.value = ser2
    servo1.value = max(-1, min(1, values[0]))
    servo2.value = max(-1, min(1, values[1]))
#     print(f"Servo 1= {servo1.value:4.1f}; Servo 2 = {servo2.value:4.1f}")
    
def ball_tracking():
    servo2.value = 0
    servo1.value = 0
    # Allow camera to wakeup
    sleep(0.1)
    # Capture from camera
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
                pid_correction(ballDefault,ballPos)
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
