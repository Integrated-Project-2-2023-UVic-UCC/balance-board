import numpy as np
import cv2 as cv

def blobAnalysis(im):
    #contours = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv.findContours(im, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(im, contours, -1, (0,255,0), 3)


cap = cv.VideoCapture(0)  # use videocapture function to load the object
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # capture frame by frame
    ret, frame = cap.read()
    # if frame is read correctly ret is true
    if not ret:
        print("Can't receive frame(stream end). Exiting ...")
        break
    # operation on the frame
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    inverted_img = cv.bitwise_not(gray)
    ret,thresh_au = cv.threshold(inverted_img,20,255,cv.THRESH_BINARY) #Threshold
    detector = cv.SimpleBlobDetector_create()

    keypoints = detector.detect(thresh_au)
    #print(keypoints)

    # draw detected blob as round circles
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob

    im_with_keypoints = cv.drawKeypoints(thresh_au, keypoints, np.array(
        []), (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # display the results
    blobAnalysis(thresh_au)
    cv.imshow("Frame", thresh_au)
    if cv.waitKey(1) == ord("q"):
        break

# release the capture
cap.release()
cv.destroyAllWindows()
