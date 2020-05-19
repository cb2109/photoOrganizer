import os
import shutil 
import ntpath
import logging
from PIL import Image, ImageFile
import PIL.ExifTags

from pictureloader.Metadata import Metadata

ImageFile.LOAD_TRUNCATED_IMAGES = True
logger = logging.getLogger(__name__)

class Picture(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.file = Image.open(self.file_path)
        if self.file._getexif() is not None:
            self.exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in self.file._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
        else:
            self.exif = None
        self.metadata = Metadata()

    def get_datetime(self):

        if self.exif is None:
            return None
        elif "DateTimeOriginal" in self.exif.keys():
            return self.exif["DateTimeOriginal"]
        else:
            logger.warning("No exif date for image: %s" % self.file_path)
            return None
            

    def get_gps_info(self):
        if self.exif is None:
            return None
        elif "GPSInfo" in self.exif.keys():
            return self.exif["GPSInfo"]
        else:
            logger.warning("No exif location for image: %s" % self.file_path)
            return None

    def write(self, path, file_name = None):
        if not os.path.exists(path):
            os.makedirs(path)
        
        if not os.path.isdir(path):
            raise Exception("File exists at current directory location: %s" % path)
        
        if file_name is None:
            file_name = ntpath.basename(self.file_path)

        full_path = os.path.join(path, file_name)
        if os.path.exists(full_path):
            raise Exception("File exists: %s" % full_path)
        try:
            shutil.copyfile(self.file_path, full_path)
        except IOError as e:
            logger.error("Picture %s could not be saved %s" % (self, e))





    def close(self):
        self.file.close()

    def __repr__(self):
        return "Picture: %s" % self.file_path
