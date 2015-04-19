import math
import GaussPointFactory

def integrate2D(f, element):
    area = element.getArea()
    gaussPoints = GaussPointFactory.getGaussPoints2D()
    
    sum = 0.0
    for pointDesc in gaussPoints:
        sum += pointDesc[0] * f(*transformOrigin(element, pointDesc[1], pointDesc[2]))
    return area * sum;

def transformOrigin(element, x, y):
    xTransformed = x * (element.x2.x - element.x1.x) + y * (element.x3.x - element.x1.x) + element.x1.x
    yTransformed = x * (element.x2.y - element.x1.y) + y * (element.x3.y - element.x1.y) + element.x1.y
    return [float(xTransformed), float(yTransformed)]

def integrate1D(f, segment):
    factor = getTransformationFactor(segment)
    gaussPoints = GaussPointFactory.getGaussPoints1D()
    
    sum = 0.0
    for pointDesc in gaussPoints:
        sum += pointDesc[0] * f(*transformSegementParameter(segment, pointDesc[1]))
    return factor * sum

def transformSegementParameter(segment, t):
    x = 0.5 * (segment.endpoint.x - segment.startpoint.x) * t + 0.5 * (segment.endpoint.x + segment.startpoint.x)
    y = 0.5 * (segment.endpoint.y - segment.startpoint.y) * t + 0.5 * (segment.endpoint.y + segment.startpoint.y)
    return [float(x), float(y)]

def getTransformationFactor(segment):
    x = 0.5 * (segment.endpoint.x - segment.startpoint.x)
    y = 0.5 * (segment.endpoint.y - segment.startpoint.y)
    return math.sqrt(x ** 2 + y ** 2)