from math import sin, cos, sqrt, atan2, radians

class Coord(object):

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def distance(self, other):
        if self.is_unknown() or other.is_unknown():
            return None
        else:
            radius_of_earth = 6373.0
            lat1 = radians(self.lat)
            lon1 = radians(self.lon)
            lat2 = radians(other.lat)
            lon2 = radians(other.lon)
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return radius_of_earth * c

    def is_unknown(self):
        return self.lat is None and self.lon is None

    def __eq__(self, other):
        if isinstance(other, Coord):
            return self.lat == other.lat and self.lon == other.lon
        return False

    def __hash__(self):
        return hash((self.lat, self.lon))

    def __repr__(self):
        return "(%s, %s)" % (self.lat, self.lon)