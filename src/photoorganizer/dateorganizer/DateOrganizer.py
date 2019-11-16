
from pictureloader.Picture import Picture
from typing import List, Dict

from datetime import datetime

class DateOrganizer(object):

    def organize(self, picture_arr: List[Picture]) -> Dict[str, Picture]:
        date_to_picture = {}
        for picture in picture_arr:
            print(picture.get_file_modified_time())
