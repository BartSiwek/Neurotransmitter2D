class SlopeFunction:    
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        
        self.a = p2.y - p3.y
        self.b = p3.x - p2.x
        self.c = (p2.x * p3.y - p2.y * p3.x)
        self.denominator = self.a * p1.x + self.b * p1.y + self.c
        
    def __str__(self):
        return "1.0 / " + str(self.denominator) + " * ((" + str(self.a) + ")*x + (" + str(self.b) + ")*y + (" + str(self.c) + "))"
        
    def evaluate(self, x, y):
        return float(self.a * x + self.b * y + self.c) / self.denominator 
    
    def evaluateXDerivate(self, x, y):
        return float(self.a) / self.denominator
    
    def evaluateYDerivate(self, x, y):
        return float(self.b) / self.denominator
    
    def getDerivates(self):
        return [self.evaluateXDerivate, self.evaluateYDerivate]

def buildShapeFunctionsForPslg(pslg):
    result = [None for i in range(0, len(pslg.elements))]
    for element in pslg.elements:
        result[element.index] = (SlopeFunction(element.x1, element.x2, element.x3),
                                 SlopeFunction(element.x2, element.x3, element.x1),
                                 SlopeFunction(element.x3, element.x1, element.x2))
    return result
