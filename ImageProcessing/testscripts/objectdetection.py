#REQUIRES TENSORFLOW
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()  # get evey frame from the video feed
    bbox, label, conf = cv.detect_common_objects(
        frame)  # detect objects in each frame
    output_image = draw_bbox(frame, bbox, label, conf)

    cv2.imshow("Object detection", output_image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
