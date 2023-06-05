import cv2

# Load the image
img = cv2.imread('blob_image.jpg')

# Set up the SimpleBlobDetector with default parameters
detector = cv2.SimpleBlobDetector_create()

# Detect keypoints
keypoints = detector.detect(img)

# Filter keypoints based on circularity
circular_keypoints = []
for kp in keypoints:
    circularity = kp.size / kp.response
    if 0.8 < circularity < 1.2:
        circular_keypoints.append(kp)

# Get the position and radius of the circular blob
x, y = circular_keypoints[0].pt
radius = circular_keypoints[0].size / 2

# Draw the circular blob on the image
cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 0), 2)

# Show the image with the circular blob
cv2.imshow('Image with Circular Blob', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
