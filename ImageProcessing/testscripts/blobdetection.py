import cv2
import numpy as np


def blobAnalysis(im, img):
    #contours = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # find contours in the binary image
    contours, hierarchy = cv2.findContours(
        im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        # calculate moments for each contour
        M = cv2.moments(c)

        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(img, (cX, cY), 5, (0, 0, 255), -1)
        
        # display the image

    while True:
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            exit()


# Read the image
im = cv2.imread("./coins.png", cv2.IMREAD_GRAYSCALE)
inverted_img = cv2.bitwise_not(im)
ret, thresh_au = cv2.threshold(
    inverted_img, 175, 255, cv2.THRESH_BINARY)  # Threshold
detector = cv2.SimpleBlobDetector_create()

keypoints = detector.detect(inverted_img)
#print(keypoints)

# draw detected blob as round circles
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(inverted_img, keypoints, np.array(
    []), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

print(dir(keypoints))

for keyPoint in keypoints:
    x = keyPoint.pt[0]
    y = keyPoint.pt[1]
    s = keyPoint.size
    print((x,y,s))
    cv2.circle(im, (int(x), int(y)), 5, (0, 0, 255), -1)
#blobAnalysis(thresh_au, im)
# Show keypoints

while True:
    cv2.imshow("Keypoints", im)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        exit()
