from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import face_recognition as fr
import pickle
from paths1 import list_images
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
                help="name of user to add")
args = vars(ap.parse_args())

prototxtPath = "./files/deploy.prototxt"
weightsPath = "./files/res10_300x300_ssd_iter_140000.caffemodel"
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxtPath, weightsPath)
user = args["name"]

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
g = 0
# while True:
#     # grab the frame from the threaded video stream and resize it
#     # to have a maximum width of 400 pixels
#     frame = vs.read()
#     frame2 = imutils.resize(frame, width=400)
#     # grab the frame dimensions and convert it to a blob
#     (h, w) = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(cv2.resize(
#         frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

#     g += 1
#     net.setInput(blob)
#     detections = net.forward()

#     # loop over the detections
#     for i in range(0, detections.shape[2]):
#         # extract the confidence (i.e., probability) associated with the
#         # prediction
#         confidence = detections[0, 0, i, 2]

#         # filter out weak detections by ensuring the `confidence` is
#         # greater than the minimum confidence
#         if confidence < 0.5:
#             continue

#         # compute the (x, y)-coordinates of the bounding box for the
#         # object
#         box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

#         (startX, startY, endX, endY) = box.astype("int")
#         main = frame[startY:endY, startX:endX]

#         # draw the bounding box of the face along with the associated
#         # probability
#         text = "{:.2f}%".format(confidence * 100)
#         y = startY - 10 if startY - 10 > 10 else startY + 10

#     cv2.imwrite("./dataset/" + user + "/" + str(g) + ".jpg", main)
#     cv2.imshow("Frame", frame)

#     key = cv2.waitKey(100) & 0xFF

#     # if the `q` key was pressed, break from the loop
#     if key == ord("q"):
#         break

cv2.destroyAllWindows()

print("[INFO] Training images")

imagePaths = list(list_images('dataset/'))
# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

for (i, imagePath) in enumerate(imagePaths):
    name = imagePath.split(os.path.sep)[-2]
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = fr.face_locations(rgb, model="hog")
    encodings = fr.face_encodings(rgb, boxes)
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open('encodings.pickle', "wb")
f.write(pickle.dumps(data))
f.close()
