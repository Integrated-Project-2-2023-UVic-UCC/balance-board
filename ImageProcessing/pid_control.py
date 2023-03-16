import cv2
import time
from gpiozero import Servo

# Set up the servos
servo1 = Servo(17)  # adjust pin numbers as needed
servo2 = Servo(18)

# Set the PID parameters
Kp = 1.0
Ki = 0.0
Kd = 0.0

# Set the initial error and control values
error = 0.0
last_error = 0.0
integral = 0.0
control = 0.0

# Set the desired position of the ball
setpoint_x = 320  # adjust as needed
setpoint_y = 240

# Set the tolerance for the ball position
tolerance = 20

# Initialize the camera
cap = cv2.VideoCapture(0)  # adjust camera index as needed

# Loop indefinitely
while True:
    # Capture the current frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    # Detect the ball in the frame
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=0, maxRadius=0)

    # Check if the ball was detected
    if circles is not None:
        # Get the position of the ball
        x, y, radius = circles[0][0]

        # Calculate the error signal
        error_x = setpoint_x - x
        error_y = setpoint_y - y
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

        # Check if the ball is within the tolerance range
        if abs(error_x) < tolerance and abs(error_y) < tolerance:
            # Stop the servos
            servo1.value = 0.5
            servo2.value = 0.5

        # Update the last error
        last_error = error

    # Display the current frame with the ball position
    cv2.imshow('Frame', frame)

    # Wait for a key press and exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Delay to allow time for the servos to move
    time.sleep(0.01)  # adjust as needed

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
