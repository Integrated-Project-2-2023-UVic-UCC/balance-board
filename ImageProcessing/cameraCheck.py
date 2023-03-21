from picamera.array import PiRGBArray
from picamera import PiCamera
from gpiozero import Servo

from time import sleep
import cv2 as cv
import numpy as np

# initialize the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera)
ballDefault = 0
ballPos = 0
# set up servos
servo1 = Servo(17)  # adjust pin numbers as needed
servo2 = Servo(18)

# Set the PID parameters [TODO]
Kp = 1.0
Ki = 0.0
Kd = 0.0

# Set the initial error and control values [TODO]
error = 0.0
last_error = 0.0
integral = 0.0
control = 0.0

# Set the tolerance for the ball position
tolerance = 20


# Allow camera to wakeup
sleep(0.1)
# Capture from camera

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    # crop image, this will be adapted to the installation
    image = image[150:330, 275:500]

    # operation on the frame
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 80, 255, cv.THRESH_BINARY)

    # center of image,where we want the ball to be
    # This will be static once the distance between camera a board is defined [TODO]
    cx = thresh[:, 0]
    cy = thresh[0, :]
    posx = cy.size/2
    posy = cx.size/2
    ballDefault = (posx, posy)

    # calculate ball position
    rr, cc = np.nonzero(thresh > 0)
    if rr.size:
        cr = np.sum(rr)/rr.size
        cc = np.sum(cc)/cc.size
        rr = np.sqrt(rr.size/np.pi)
        cv.circle(thresh, (int(cc), int(cr)), int(rr),
                  (44, 236, 6), thickness=2, lineType=8, shift=0)
        ballPos = (cr, cc)
    # Calculate the error signal
    error_x = ballDefault[0] - ballPos[0]
    error_y = ballDefault[1] - ballPos[0]
    error = error_x

    # Calculate the derivative term
    derivative = error - last_error

    # Calculate the integral term
    integral += error

    # Calculate the control signal using the PID algorithm
    control = (Kp * error) + (Ki * integral) + (Kd * derivative)

    # Adjust the servo positions based on the control signal
    servo1.value = 0.5 + control
    servo2.value = 0.5 - control

    # check if the ball is within the tolerance range
    if abs(error_x) < tolerance and abs(error_y) < tolerance:
        # Stop the servos
        servo1.value = 0.5
        servo2.value = 0.5
    # Update the last error
    last_error = error

    # Show the image
    cv.imshow("Frame", thresh)
    key = cv.waitKey(1) & 0xFF
    # Delay to allow time for the servos to move
    sleep(0.01)  # adjust as needed
    # Clear stream
    rawCapture.truncate(0)
    if key == ord("q"):
        break
