import numpy as np
import cv2

class Detectors(object):
    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        
    
    def Detect_ball(self,frame):
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        gray_blurred = cv2.blur(gray, (3,3))
        
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=40, param2=70, minRadius=50, maxRadius=100)
        
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            
            return detected_circles[0]
        
        else:
            return [[0]]
            