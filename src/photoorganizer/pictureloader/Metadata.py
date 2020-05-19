
from util.Coord import Coord

class Metadata(object):

    def __init__(self):
        self.date = None
        self.coord = Coord(None, None)
        self.location = None
        self.num_faces = None