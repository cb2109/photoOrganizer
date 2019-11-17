#!/usr/bin/env python
from typing import List, Dict
from pictureloader.Picture import Picture
from organizers.DateOrganizer import DateOrganizer
from organizers.LocationOrganizer import LocationOrganizer
import os
import logging

logging.basicConfig()
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
        pictures.append(Picture(path))
    return pictures

def organize_by_date(pictures: List[Picture]) -> Dict[str, Picture]:
    date_organizer = DateOrganizer()
    organized_pictures = date_organizer.organize(pictures)
    return organized_pictures

def organize_by_location(pictures: Dict[str, Picture]) -> Dict[str, Dict[str, List[Picture]]]:
    location_organizer = LocationOrganizer()
    organized_pictures = {}
    for folder in pictures.keys():
        organized_pictures[folder] = location_organizer.organize(pictures[folder])
    return organized_pictures

def write_pictures(dir: str, pictures: Dict):
    for folder_name in pictures.keys():
        sub_path = os.path.join(dir, folder_name)
        if isinstance(pictures[folder_name], Dict):
            write_pictures(sub_path, pictures[folder_name])
        else:
            for picture in pictures[folder_name]:
                picture.write(sub_path)


if __name__== "__main__":
    start_dir = "C:\\Users\\Chris\\Pictures\\iCloud Photos\\Downloads\\2018\\"
    output_dir = "C:\\Users\\Chris\\Documents\\My Projects\\photoOrganizer\\output"
    if os.path.exists("..\\..\\output"):
        remove_output("..\\..\\output")
    picture_paths = get_picture_paths(start_dir)
    pictures = []
    try:
        pictures = convert_to_pictures(picture_paths)
        date_organized_pictures = organize_by_date(pictures)
        location_organized_pictures = organize_by_location(date_organized_pictures)
        write_pictures(output_dir, location_organized_pictures)
    finally:
        for picture in pictures:
            picture.close()
