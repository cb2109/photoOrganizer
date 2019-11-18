
from pictureloader.Picture import Picture
from util.Coord import Coord
from typing import List
import logging
import os

logger = logging.getLogger(__name__)

class DefaultOutput(object):

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.date_format = "%Y-%m"

    def write(self, pictures: List[Picture]):
        for picture in pictures:
            dir_name = self._get_dir_name(picture)
            if dir_name is not None:
                sub_path = os.path.join(self.output_path, dir_name)
                picture.write(sub_path)

                    
    def _get_dir_name(self, picture: Picture) -> str:
        metadata = picture.metadata
        if metadata.date is None or metadata.coord == Coord(None, None):
            return None
        else:
            return metadata.date.strftime(self.date_format) + "_" + metadata.location