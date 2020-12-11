import cv2
import numpy as np
import yolo

cap = cv2.VideoCapture("video1.mp4")
ret, frame = cap.read()
height,width,layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter('output1.avi',fourcc,20.0,(width,height))

while(cap.isOpened()):
    ret, frame = cap.read()
    output_img = yolo.objectDectector(frame)
    video.write(output_img)


cap.release()
cv2.destroyAllWindows()
video.release()