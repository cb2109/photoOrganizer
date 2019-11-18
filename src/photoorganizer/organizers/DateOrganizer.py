
from pictureloader.Picture import Picture
from typing import List
import platform
import os
from datetime import datetime

class DateOrganizer(object):

    def __init__(self):
        self.exif_date_format = "%Y:%m:%d %H:%M:%S"

    def organize(self, picture_arr: List[Picture]):
        date_to_picture = {}
        for picture in picture_arr:
            date_modified = self._get_date(picture)
            picture.metadata.date = date_modified
        return picture_arr

    def _get_date(self, picture: Picture):
        exif_date = picture.get_datetime()
        if exif_date is not None:
            return datetime.strptime(exif_date, self.exif_date_format)
        else:
            return None
            # if platform.system() == 'Windows':
            #     return datetime.fromtimestamp(os.path.getctime(picture.file_path))
            # else:
            #     stat = os.stat(picture.file_path)
            #     try:
            #         return fromtimestamp(stat.st_birthtime)
            #     except AttributeError:
            #         return fromtimestamp(stat.st_mtime)
        

