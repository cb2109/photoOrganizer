
from pictureloader.Picture import Picture
from typing import List
from util.Coord import Coord
import logging

logger = logging.getLogger(__name__)


class LocationOrganizer(object):

    def __init__(self):
        self.unique_coord_groups = {}
        self.unique_coord_groups[Coord(None, None)] = (0, "Unknown")
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
        self.unique_coord_groups[Coord(34.162850, -84.651571)] = (5, "Allatoona Lake")
        self.unique_coord_groups[Coord(34.108536111111114, -84.7104638888889)] = (1, "Allatoona Landing")
        self.unique_coord_groups[Coord(34.058596, -84.680308)] = (5, "Acworth")
        self.unique_coord_groups[Coord(33.981275000000004, -84.03390555555555)] = (1, "Bob Bruffey's")
        self.unique_coord_groups[Coord(33.88934444444445, -84.46881944444445)] = (1, "The Battery")
        self.unique_coord_groups[Coord(33.80598055555555, -84.68133611111112)] = (1, "Ashley & John Roger's")
        self.unique_coord_groups[Coord(33.923030555555556, -84.46796388888889)] = (1, "Delk Road Publix")
        self.unique_coord_groups[Coord(33.845075, -84.501275)] = (1, "US Cafe")
        self.unique_coord_groups[Coord(33.90162222222222, -84.44085)] = (2, "Cochran Shoals")
        self.unique_coord_groups[Coord(33.237208333333335, -83.94449722222222)] = (5, "Indian Springs State Park")
        self.unique_coord_groups[Coord(34.23898611111111, -84.0747611111111)] = (1, "Len & Mary Locurto's")
        # One set of photos has bad geodata
        self.unique_coord_groups[Coord(33.82868888888889, -84.30294166666667)] = (1, "Casey Dutro's Family Home")
        self.unique_coord_groups[Coord(33.84957222222222, -84.31900833333333)] = (1, "Casey Dutro's Family Home")
        self.unique_coord_groups[Coord(33.897933333333334, -84.47943055555555)] = (1, "Target Cobb Parkway")
        self.unique_coord_groups[Coord(33.98184722222222, -84.43100833333334)] = (1, "Sprouts Rosswell Rd")
        self.unique_coord_groups[Coord(33.926849999999995, -84.49780277777778)] = (1, "Schoolhouse Brewing")
        self.unique_coord_groups[Coord(34.053980555555555, -84.30631944444444)] = (1, "Ameris Bank Amphitheatre")
        self.unique_coord_groups[Coord(33.975119444444445, -84.41426944444444)] = (1, "Goldbergs Johnson Ferry Rd")
        self.unique_coord_groups[Coord(33.88014166666667, -84.46863611111111)] = (1, "Cumberland Mall")
        self.unique_coord_groups[Coord(33.97788611111111, -84.45329166666667)] = (1, "East Cobb Park")
        self.unique_coord_groups[Coord(34.10904444444444, -84.42401944444445)] = (1, "Berry Patch Farms")
        self.unique_coord_groups[Coord(33.79896111111111, -84.73339722222222)] = (1, "Sleepy Hollow Farm")
        self.unique_coord_groups[Coord(33.81135833333333, -84.63380555555557)] = (1, "Austell Presbyterian Church")
        self.unique_coord_groups[Coord(34.04650833333333, -84.60215833333332)] = (1, "Kennesaw Pediatrics Newborn Center")
        self.unique_coord_groups[Coord(0, 0)] = (0, "Unmatched")

        self.matching_distance = 1
        self.unmatched = {}

    def organize(self, picture_arr: List[Picture]) -> List[Picture]:
        # search through the coords to find matching "unique coordinates"
        for picture in picture_arr:
            coord = self._get_coord(picture)
            group = self._get_group(coord)
            picture.metadata.coord = coord
            picture.metadata.location = group

        return picture_arr
        

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

        matched = False
        for unmatched_coord in self.unmatched.keys():
            if coord.distance(unmatched_coord) <= self.matching_distance:
                self.unmatched[unmatched_coord].append(coord)
                matched = True
                break

        if not matched:
            self.unmatched[coord] = [coord]
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