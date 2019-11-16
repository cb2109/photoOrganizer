#!/usr/bin/env python
from typing import List, Dict
from pictureloader.Picture import Picture
from dateorganizer.DateOrganizer import DateOrganizer
import os

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

def write_pictures(dir: str, pictures: Dict):
    for folder_name in pictures.keys():
        sub_path = os.path.join(dir, folder_name)
        if isinstance(pictures[folder_name], list):
            for picture in pictures[folder_name]:
                picture.write(sub_path)
        else:
            write_pictures(sub_path, pictures[folder_name])


if __name__== "__main__":
    start_dir = "C:\\Users\\Chris\\Pictures\\iCloud Photos\\Downloads\\2018\\"
    output_dir = "C:\\Users\\Chris\\Documents\\My Projects\\photoOrganizer\\output"
    picture_paths = get_picture_paths(start_dir)
    pictures = []
    try:
        pictures = convert_to_pictures(picture_paths)
        date_organized_pictures = organize_by_date(pictures)
        write_pictures(output_dir, date_organized_pictures)
    finally:
        for picture in pictures:
            picture.close()
