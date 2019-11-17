
from pictureloader.Picture import Picture
from typing import List, Dict, Tuple
from organizers.Coord import Coord
import logging

logger = logging.getLogger(__name__)


class LocationOrganizer(object):

    def __init__(self):
        self.unique_coord_groups = {}
        self.unique_coord_groups[Coord(None, None)] = (0, "No data")
        self.unique_coord_groups[Coord(32.764793, -117.133807)] = (15, "San Diego")
        self.unique_coord_groups[Coord(30.25861111111111, -97.74694444444445)] = (15, "Austin")
        self.unique_coord_groups[Coord(33.965833333333336, -84.54972222222221)] = (5, "Marietta")
        self.unique_coord_groups[Coord(33.905277777777776, -84.47166666666666)] = (1, "Belmont Place")
        self.unique_coord_groups[Coord(33.755840, -84.389865)] = (6, "Downtown Atlanta")
        self.unique_coord_groups[Coord(33.57, -84.71972222222223)] = (5, "Cochran Mill Park")
        self.unique_coord_groups[Coord(34.88638888888889, -84.34055555555555)] = (20, "Blue Ridge")
        self.unique_coord_groups[Coord(33.683055555555555, -84.7125)] = (2, "High Country Dr")
        self.unique_coord_groups[Coord(33.659166666666664, -84.715)] = (1, "Chapelhill Church")
        self.unique_coord_groups[Coord(34.099722222222226, -84.51972222222223)] = (5, "Woodstock")
        self.unique_coord_groups[Coord(0, 0)] = (0, "Unknown")

    def organize(self, picture_arr: List[Picture]) -> Dict[str, List[Picture]]:
        grouped_pictures = {}
        # search through the coords to find matching "unique coordinates"
        for picture in picture_arr:
            coord = self._get_coord(picture)
            group = self._get_group(coord)
            if not group in grouped_pictures:
                grouped_pictures[group] = []     
            grouped_pictures[group].append(picture)
            if group == "Unknown":
                logger.warning("Unknown picture at %s: %s" % (coord, picture))

        return grouped_pictures
        

    def _get_coord(self, picture: Picture):
        gps_info = picture.get_gps_info()
        if gps_info is None:
            return Coord(None, None)
        lat = self._convert_to_degress(gps_info[2])
        lon = self._convert_to_degress(gps_info[4])
        if gps_info[1] == 'S':
            lat = -lat
        if gps_info[3] == 'W':
            lon = -lon
        return Coord(lat, lon)

    def _get_group(self, coord: Coord):
        
        # the unknown Coord(None, None)
        if coord.is_unknown():
            logger.debug("Unknown coord %s, returning %s" % (coord, self.unique_coord_groups[coord][1]))
            return self.unique_coord_groups[coord][1]

        closest = Coord(0, 0)
        distance = coord.distance(closest)
        # search for any unique coords in range
        for unique_coord in self.unique_coord_groups.keys():
            # if matching then use the same group
            dist = coord.distance(unique_coord)
            if dist is not None and dist <= self.unique_coord_groups[unique_coord][0]:
                return self.unique_coord_groups[unique_coord][1]
        # if not matched then add this to a new group
        logger.debug("Unmatched coord %s, returning %s" % (coord, self.unique_coord_groups[closest][1]))
        return self.unique_coord_groups[closest][1]

    # borrowed from 
    # https://gist.github.com/snakeye/fdc372dbf11370fe29eb 
    def _convert_to_degress(self, value):
        """
        Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
        :param value:
        :type value: exifread.utils.Ratio
        :rtype: float
        """
        d = float(value[0][0]) / float(value[0][1])
        m = float(value[1][0]) / float(value[1][1])
        s = float(value[2][0]) / float(value[2][1])

        return d + (m / 60.0) + (s / 3600.0)