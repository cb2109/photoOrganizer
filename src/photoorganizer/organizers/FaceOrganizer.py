import logging
from typing import List
import cv2
import numpy as np
from pictureloader.Picture import Picture

logger = logging.getLogger(__name__)


class FaceOrganizer(object):

    def __init__(self, trained_xml_path, proto_model, caffe_model):
        self.xml = trained_xml_path
        self.proto_model = proto_model
        self.caffe_model = caffe_model
        self.scaleFactor = 1.5
        self.minNeighbors = 6
        self.confidence_filter = 0.9
        self.minSize = (30, 30)


    def organize(self, picture_arr: List[Picture]) -> List[Picture]:
        # search through the coords to find matching "unique coordinates"
        for picture in picture_arr:
            num_faces_found = self._detect_faces_dnn(picture)
            picture.metadata.num_faces = num_faces_found
        return picture_arr

    def _detect_faces_haarcascade(self, picture: Picture) -> int:
        image = cv2.imread(picture.file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faceCascade = cv2.CascadeClassifier(self.xml)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=self.scaleFactor,
            minNeighbors=self.minNeighbors,
            minSize=self.minSize
        )

        num_faces_found = len(faces)
        logger.info("Found %s faces!" % (num_faces_found))

        # if num_faces_found > 0:
        #     # Draw a rectangle around the faces
        #     for (x, y, w, h) in faces:
        #         cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #     cv2.imshow("Faces found", self._resize_with_ascpect_ratio(image, None, 900))
        #     cv2.waitKey(1000)
        #     cv2.destroyAllWindows()
        return num_faces_found

    def _detect_faces_dnn(self, picture: Picture) -> int:
        net = cv2.dnn.readNetFromCaffe(self.proto_model, self.caffe_model)

        image = cv2.imread(picture.file_path)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        detected_face = 0
        # Draw a rectangle around the faces
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]
         
            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > self.confidence_filter:
                detected_face = detected_face + 1
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
        if detected_face > 0 and False:
            cv2.imshow("Output", self._resize_with_ascpect_ratio(image, None, 900))
            cv2.waitKey(0)
        return detected_face

    def _resize_with_ascpect_ratio(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)