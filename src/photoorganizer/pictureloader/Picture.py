import os
import ntpath
import platform
import logging
from datetime import datetime
from PIL import Image
import PIL.ExifTags

logger = logging.getLogger(__name__)

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

    def get_datetime(self):
        if "DateTimeOriginal" in self.exif.keys():
            date = self.exif["DateTimeOriginal"]
            return datetime.strptime(date, self.exif_date_format)
        else:
            logger.warn("No exif date for image: %s" % self.file_path)
            if platform.system() == 'Windows':
                return datetime.fromtimestamp(os.path.getctime(self.file_path))
            else:
                stat = os.stat(path_to_file)
                try:
                    return fromtimestamp(stat.st_birthtime)
                except AttributeError:
                    return fromtimestamp(stat.st_mtime)

    def get_gps_info(self):
        if "GPSInfo" in self.exif.keys():
            return self.exif["GPSInfo"]
        else:
            logger.warn("No exif location for image: %s" % self.file_path)
            return None

    def write(self, path, file_name = None):
        if not os.path.exists(path):
            os.makedirs(path)
        
        if not os.path.isdir(path):
            raise "File exists at current directory location: %s" % path
        
        if file_name is None:
            file_name = ntpath.basename(self.file_path)

        full_path = os.path.join(path, file_name)
        if os.path.exists(full_path):
            raise "File exists: " + full_path
        
        self.file.save(full_path, self.file.format)




    def close(self):
        self.file.close()

    def __repr__(self):
        return "Picture: %s" % self.file_path
