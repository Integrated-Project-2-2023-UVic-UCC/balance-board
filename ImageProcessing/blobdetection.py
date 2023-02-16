import cv2
import numpy as np

# Read the image
im = cv2.imread("./coins.jpg", cv2.IMREAD_GRAYSCALE)
inverted_img = cv2.bitwise_not(im)
ret, thresh_au = cv2.threshold(inverted_img, 200, 255, cv2.THRESH_BINARY)
#detector = cv2.SimpleBlobDetector_create()

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Filter by Area.
params.filterByArea = True
params.minArea = 50

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.75

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.7

detector = cv2.SimpleBlobDetector_create(params)


keypoints = detector.detect(thresh_au)
print(keypoints)

# draw detected blob as round circles
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
blank_im = np.zeros((1, 1))
im_with_keypoints = cv2.drawKeypoints(thresh_au, keypoints, np.array(
    []), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
while True:
    cv2.imshow("Keypoints", im_with_keypoints)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        exit()
