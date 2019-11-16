import os
import platform
from datetime import datetime
from PIL import Image
import PIL.ExifTags

class Picture(object):

    def __init__(self, file_path):
        self.exif_date_format = "%Y:%m:%d %H:%M:%S"
        self.file_path = file_path
        self.file = Image.open(self.file_path)
        self.exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in self.file._getexif().items()
            if k in PIL.ExifTags.TAGS
        }

    def get_file_modified_time(self):
        if "DateTimeOriginal" in self.exif.keys():
            date = self.exif["DateTimeOriginal"]
            return datetime.strptime(date, self.exif_date_format)
        else:
            print("No exif date for image: " + self.file_path)
            if platform.system() == 'Windows':
                return datetime.fromtimestamp(os.path.getctime(self.file_path))
            else:
                stat = os.stat(path_to_file)
                try:
                    return fromtimestamp(stat.st_birthtime)
                except AttributeError:
                    return fromtimestamp(stat.st_mtime)

    def close(self):
        self.file.close()

