from pictureloader.Picture import Picture
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

if __name__== "__main__":
    # Clear the output dir
    picture_path = "C:\\Users\\Chris\\Documents\\My Projects\\photoOrganizer\\output\\2019-10_Unknown\\49bf7d2a-2b88-487a-9b7e-2344a8eed9cb.jpg"
    picture = Picture(picture_path)
    print(picture.exif)