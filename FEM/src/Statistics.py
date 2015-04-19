import math

def ComputeOmegaDLength(parameters):
    omegaDLength = 0.0
    for (segment, element) in parameters.omegaD:
        omegaDLength += segment.getLength()
    return omegaDLength

def ComputeSegmentLengthRange(parameters):
    min = 1E30
    minStart = None
    minEnd = None
    max = 0.0
    maxStart = None
    maxEnd = None
    
    for element in parameters.omega:
        for i in range(0, 3):
            a = element.points[i]
            b = element.points[(i + 1) % 3]
            
            length = math.sqrt((b.x - a.x)**2 + (b.y - a.y)**2)
            
            if(length < min):
                min = length
                minStart = a
                minStop = b
            if(length > max):
                max = length
                maxStart = a
                maxStop = b
    
    return ((min, minStart, minStop), (max, maxStart, maxStop))
            
def ComputeElementAngleRange(parameters):
    min = 2.0 * math.pi
    max = 0.0 * math.pi
    for element in parameters.omega:
        for i in range(0, 3):
            a = element.points[i]
            b = element.points[(i + 1) % 3]
            c = element.points[(i + 2) % 3]
            
            angle = ComputeAngleBetweenPoints(a, b, c)
            
            if(angle < min):
                min = angle
            if(angle > max):
                max = angle
    
    min = (min / math.pi) * 360.0
    max = (max / math.pi) * 360.0
    return (min, max)

def ComputeAngleBetweenPoints(a, b, c):
    v1 = (b.x - a.x, b.y - a.y)
    v2 = (c.x - a.x, c.y - a.y)
            
    dot = v1[0]*v2[0] + v1[1]*v2[1] 
    v1Len = math.sqrt(v1[0]**2 + v1[1]**2);
    v2Len = math.sqrt(v2[0]**2 + v2[1]**2);
            
    angleCos = dot / (v1Len * v2Len)
    angle = math.acos(angleCos)
    
    return angle