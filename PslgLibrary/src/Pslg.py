import math

class Point:   
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __eq__(self, rhs):
        if self.__class__ is not rhs.__class__:
            return False
        return (self.x == rhs.x) and (self.y == rhs.y) 
    
    def asTuple(self):
        return (self.x, self.y)
    
class GridPoint(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.boundaryMarker = None
        self.index = None
    
class Segment:
    def __init__(self, startpoint, endpoint):
        self.points = [startpoint, endpoint]
        self.startpoint = startpoint
        self.endpoint = endpoint
        
    def __str__(self):
        return "(" + str(self.startpoint) + ", " + str(self.endpoint) + ")"

    def __eq__(self, rhs):
        if self.__class__ is not rhs.__class__:
            return False
        return ((self.startpoint == rhs.startpoint) and (self.endpoint == rhs.endpoint)
                or
                (self.startpoint == rhs.endpoint) and (self.endpoint == rhs.startpoint))

    def getBoundaryMarker(self):
        firstBoundaryMarker = self.startpoint.boundaryMarker
        secondBoundaryMarker = self.endpoint.boundaryMarker
        
        if firstBoundaryMarker is not None and secondBoundaryMarker is not None and firstBoundaryMarker == secondBoundaryMarker:
            return firstBoundaryMarker
        return 0;

    def getLength(self):
        return math.sqrt((self.startpoint.x - self.endpoint.x)**2 + (self.startpoint.y - self.endpoint.y)**2)

class Hole(Point):
    pass

class Region(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.id = None

class Pslg:
    def __init__(self):
        self.points = []
        self.segments = []
        self.holes = []
        self.regions = []
    
    def __str__(self):
        return str(self.getSegmentsAsLinesList())
    
    def getSegmentsAsLinesList(self):
        lines = []
        for segment in self.segments:
            start = segment.startpoint
            end = segment.endpoint
            lines.append((start.x, start.y, end.x, end.y, segment.getBoundaryMarker()))
        return lines
    
    def getPointsAsList(self):
        points = []
        for point in self.points:
            points.append(point.asTuple())
        return points

    def getHolesAsList(self):
        holes = []
        for hole in self.holes:
            holes.append(hole.asTuple())
        return holes
    
    def getRegionsAsList(self):
        regions = []
        for region in self.regions:
            regions.append(region.asTuple())
        return regions