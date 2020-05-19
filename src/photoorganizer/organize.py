#!/usr/bin/env python
from typing import List, Dict
from pictureloader.Picture import Picture
from organizers.DateOrganizer import DateOrganizer
from organizers.LocationOrganizer import LocationOrganizer
from organizers.FaceOrganizer import FaceOrganizer
from pictureoutput.DefaultOutput import DefaultOutput
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def remove_output(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            logger.info("Deleting file: %s" % file_path)
            os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            logger.info("Deleting dir: %s" % dir_path)
            os.rmdir(dir_path)
    os.rmdir(path)

def get_picture_paths(path: str) -> List[str]:
    with os.scandir(path) as dir_entries:
        picture_paths = []
        for entry in dir_entries:
            if entry.is_dir():
                picture_paths.extend(get_pictures(entry.path))
            elif entry.is_file():
                picture_paths.append(entry.path)
        return picture_paths

def convert_to_pictures(paths: List[str]) -> List[Picture]:
    pictures = []
    for path in paths:
        try:
            pictures.append(Picture(path))
        except IOError as io:
            pass
    return pictures

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]



if __name__== "__main__":
    # Clear the output dir
    output_dir = "F:\\photoOrganizer\\output\\"
    if os.path.exists(output_dir):
        remove_output(output_dir)

    dirs = [
        "C:\\Users\\Chris\\Pictures\\iCloud Photos\\Downloads\\2018\\",
        "C:\\Users\\Chris\\Pictures\\iCloud Photos\\Downloads\\2019\\"
    ]
    picture_paths = []
    for directory in dirs:
        picture_paths.extend(get_picture_paths(directory))
        break
    
    date_organizer = DateOrganizer()
    location_organizer = LocationOrganizer()
    face_organizer = FaceOrganizer(
        os.path.abspath("haarcascade_frontalface_default.xml"),
        os.path.abspath("deploy.prototxt"),
        os.path.abspath("res10_300x300_ssd_iter_140000.caffemodel")
    )

    pictures = []
    for picture_paths_batch in batch(picture_paths, 50):
        try:
            pictures = convert_to_pictures(picture_paths_batch)
            
            output = DefaultOutput(output_dir)
            organized_pictures = face_organizer.organize(
                date_organizer.organize(
                    location_organizer.organize(pictures)))
            output.write(organized_pictures)
        finally:
            for picture in pictures:
                picture.close()

    for coord in location_organizer.unmatched.keys():
        logger.warn("Unmatched coord %s" % coord)
