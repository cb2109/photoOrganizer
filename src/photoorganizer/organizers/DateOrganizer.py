
from pictureloader.Picture import Picture
from typing import List, Dict

from datetime import datetime

class DateOrganizer(object):

    def __init__(self):
        self.date_format = "%Y-%m-%d"

    def organize(self, picture_arr: List[Picture]) -> Dict[str, Picture]:
        date_to_picture = {}
        for picture in picture_arr:
            date_modified = picture.get_file_modified_time()
            date_str = self.extract_date_str(date_modified)
            if not (date_str in date_to_picture.keys()):
                date_to_picture[date_str] = []
            date_to_picture[date_str].append(picture)
        return date_to_picture

    def extract_date_str(self, date):
        return date.strftime(self.date_format)