from __future__ import division
import cv2
import time
import sys

def detectFaceOpenCVDnn(net, frame):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes




DNN = "TF"

modelFile = "opencv_face_detector_uint8.pb"
configFile = "opencv_face_detector.pbtxt"
print("Using TF")
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

conf_threshold = 0.7

source = 0
if len(sys.argv) > 1:
    source = sys.argv[1]

cap = cv2.VideoCapture(source)
hasFrame, frame = cap.read()

vid_writer = cv2.VideoWriter('output-dnn-{}.avi'.format(str(source).split(".")[0]),cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))

frame_count = 0
tt_opencvDnn = 0
while(1):
    hasFrame, frame = cap.read()
    if not hasFrame:
        break
    frame_count += 1


    outOpencvDnn, bboxes = detectFaceOpenCVDnn(net,frame)
   

    cv2.imshow("Face Detection Comparison", outOpencvDnn)

    vid_writer.write(outOpencvDnn)
    if frame_count == 1:
        tt_opencvDnn = 0
    
    k = cv2.waitKey(10)
    if k == 27:
        break
cv2.destroyAllWindows()
vid_writer.release()

