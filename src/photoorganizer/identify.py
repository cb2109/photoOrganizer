from pictureloader.Picture import Picture
import logging
import numpy as np

import cv2

logging.basicConfig()
logger = logging.getLogger(__name__)

def scan_face(picture_path, trained_xml):
    net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

    image = cv2.imread(picture_path)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    # Draw a rectangle around the faces
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]
     
        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
     
            # draw the bounding box of the face along with the associated
            # probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(image, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
            cv2.putText(image, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    cv2.imshow("Output", image)
    cv2.waitKey(0)

if __name__== "__main__":
    # Clear the output dir
    picture_path = "F:\\photoOrganizer\\output\\2018-03_San Diego\\IMG_0029.JPG"
    picture = Picture("C:\\Users\\Chris\\Pictures\\iCloud Photos\\Downloads\\2018\\IMG_0029.JPG")
    try:
        picture.write("F:\\photoOrganizer\\output\\2018-03_San Diego\\")
    except:
        pass

    scan_face(picture_path, "haarcascade_frontalface_default.xml")


    


