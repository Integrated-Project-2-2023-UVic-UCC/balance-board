'''
File name : ball tracking.py

'''
import cv2
import numpy as np
import time
from detectors import Detectors

def main():
    
    start_time = time.time()
    cap = cv2.VideoCapture(0)
    detector = Detectors()
    pause = False
    ball_pose = 0
     
     
     
    while (True):
        ret, frame = cap.read()
        cv2.imshow('Visor',frame) 
        trap = detector.Detect_ball(frame)
        
        
            
        print(trap)
        print("\n")
        print(trap[0])
        if any(trap[0]) == True:
            for i in range(len(trap)):
                xx, yy, rr = trap[i]
                cv2.circle(frame, (xx, yy), rr, (44, 236, 6), thickness=2, lineType=8, shift=0) 
                print((xx, yy))
                cv2.imshow('Visor',frame)
        
       
        
        if cv2.waitKey(50) & 0xFF == 27:
            break
        
        if cv2.waitKey(50) & 0xFF == 112:
            pause = not pause
            if pause == True:
                key = cv2.waitKey(30) & 0xFF
                if key == 112:
                    pause = False
    
            
    cap.release()
    cv2.destroyAllWindows() 
   
        
        
if __name__ == "__main__":
    main()