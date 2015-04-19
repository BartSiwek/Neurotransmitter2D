import Pslg

class Element:
    def __init__(self, x1, x2, x3, id, index):
        self.points = [x1, x2, x3]
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.id = id
        self.index = index
        
    def __str__(self):
        return "(" + str(self.x1) + ";" + str(self.x2) + ";" + str (self.x3) + ";ID = " + str(id) + ")"
    
    def getArea(self):
        v1 = (self.x1.x - self.x2.x, self.x1.y - self.x2.y)
        v2 = (self.x1.x - self.x3.x, self.x1.y - self.x3.y)
        crossProduct = v1[0] * v2[1] - v1[1] * v2[0]
        return 0.5 * abs(crossProduct)

    def isSideOf(self, segment):
        for i in range(0, 3):
            if (segment.startpoint == self.points[i] and segment.endpoint == self.points[(i + 1) % 3]):
                return True               
            if (segment.endpoint == self.points[i] and segment.startpoint == self.points[(i + 1) % 3]):
               return True
        return False
    
    def pointToElementIndex(self, point):
        if(self.x1 == point):
            return 0
        if(self.x2 == point):
            return 1
        return 2

class ElementAwarePslg(Pslg.Pslg):
    def __init__(self):
        Pslg.Pslg.__init__(self)
        self.elements = []
