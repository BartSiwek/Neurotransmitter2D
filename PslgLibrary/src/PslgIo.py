import os
import string
import Pslg
import ElementAwarePslg

def saveToFile(file, pslg):
    contents = []
    vertexNumber = str(len(pslg.points))
    segmentsNumber = str(len(pslg.segments))
    holesNumber = str(len(pslg.holes))
    regionsNumber = str(len(pslg.regions))
    
    #Write vertexes
    contents.append("# Points section\n")
    contents.append(vertexNumber + " 2 0 1\n")    
    i = 0
    for point in pslg.points:
        pointDesc = str(i) + " " + str(point.x) + " " + str(point.y)
        if point.boundaryMarker is None:
            pointDesc += " 0\n"
        else:
            pointDesc += " " + str(point.boundaryMarker) + "\n"
        contents.append(pointDesc)
        i = i + 1
                   
    #Write segments
    contents.append("# Segments section\n")
    contents.append(segmentsNumber + " 1\n")
    i = 0
    for segment in pslg.segments:
        startPointIndex = pslg.points.index(segment.startpoint)
        endPointIndex = pslg.points.index(segment.endpoint)
        boundaryMarker = tryToGetBoundarymarkerForSegment(segment)
        segmentDesc = str(i) + " " + str(startPointIndex) + " " + str(endPointIndex) + " " + str(boundaryMarker) + "\n"
        contents.append(segmentDesc)
        i = i + 1
                 
    #Write holes
    contents.append("# Holes section\n")
    contents.append(holesNumber + "\n")
    i = 0
    for hole in pslg.holes:
        segmentDesc = str(i) + " " + str(hole.x) + " " + str(hole.y) + "\n"
        contents.append(segmentDesc)
        i = i + 1
        
    #Write regions
    contents.append("# Regions section\n")
    contents.append(regionsNumber + "\n")
    i = 0
    for region in pslg.regions:
        if region.id is not None:
            segmentDesc = str(i) + " " + str(region.x) + " " + str(region.y) + " " + str(region.id) + "\n"
        else:
            segmentDesc = str(i) + " " + str(region.x) + " " + str(region.y) + " 0\n"
        contents.append(segmentDesc)
        i = i + 1
                   
    #Write to file
    file.writelines(contents) 
    
def tryToGetBoundarymarkerForSegment(segment):
    return segment.getBoundaryMarker()
    
def readFromFile(file, pslg, filename):
    filenameParts = os.path.splitext(filename)
    if filenameParts[1] == ".node":
        loadNodeFile(file, pslg)
    elif filenameParts[1] == ".poly":
        loadPolyFile(file, pslg, filenameParts[0])
    elif filenameParts[1] == ".ele":
        loadEleFile(file, pslg, filenameParts[0])    
        
def loadPolyFile(file, pslg, baseFilename):
    (nodeNumber, dimension, boundaryMarkers, attributes) = loadNodeHeader(file)

    if nodeNumber == 0:
        nodeFile = open(baseFilename + ".node", "r")
        loadNodeFile(nodeFile, pslg)
        nodeNumber = len(pslg.points)
    else:
        loadNodes(file, pslg, nodeNumber, dimension, boundaryMarkers, attributes)
        
    loadSegments(file, pslg)
    loadHoles(file, pslg)
    loadRegions(file, pslg)
    return
       
def loadEleFile(file, pslg, baseFilename):
    nodeFile = open(baseFilename + ".node", "r")
    loadNodeFile(nodeFile, pslg)
    
    (trianglesNumber, nodesNumber, attributesNumber) = loadEleHeader(file)
    segmentSet = set()
    for i in range(0, trianglesNumber):
        line = getLine(file)
        tokens = string.split(line)
        
        if len(tokens) != 1 + nodesNumber + attributesNumber:
            raise IOError("Invalid file format (triangle " + str(i) + " has invalid format)")
        
        #Read triangle index
        index = int(tokens[0])
        
        #Read nodes
        x = None;
        y = None;
        elementConstructorArgs = []
        for j in range(0, nodesNumber):
            startPoint = int(tokens[j  + 1])
            endPoint = int(tokens[((j + 1) % nodesNumber) + 1])
            elementConstructorArgs.append(pslg.points[startPoint])
            segmentSet.add((min(startPoint, endPoint), max(startPoint, endPoint)))
            if x is None or y is None:
                x = pslg.points[startPoint].x
                y = pslg.points[startPoint].y
            else:
                x = 0.5 * x + 0.5 * pslg.points[startPoint].x
                y = 0.5 * y + 0.5 * pslg.points[startPoint].y            
        
        #Read attributes
        id = None
        if attributesNumber == 1:
            id = int(tokens[1 + nodesNumber])
            elementConstructorArgs.append(id)
        
        #Append the index
        elementConstructorArgs.append(i)
        
        #Add the element
        if pslg.__class__ is ElementAwarePslg.ElementAwarePslg:
            pslg.elements.append(ElementAwarePslg.Element(*elementConstructorArgs))
        
        #Add the triangle region
#        triangleRegion = Pslg.Region(x, y)
#        if id is not None:
#            triangleRegion.id = id
#        pslg.regions.append(triangleRegion)
        
    #Add the segments
    for (startpoint, endpoint) in segmentSet:
        pslg.segments.append(Pslg.Segment(pslg.points[startpoint], pslg.points[endpoint]))
        
    return
                
def loadNodeFile(file, pslg):
    (nodeNumber, dimension, boundaryMarkers, attributes) = loadNodeHeader(file)
    loadNodes(file, pslg, nodeNumber, dimension, boundaryMarkers, attributes)
    return

def loadHoles(file, pslg):
    line = getLine(file)
    tokens = string.split(line)
    
    if len(tokens) != 1:
        raise IOError("Invalid file format (the hole format descriptor must contain exactly one integer)")
    
    holeNumber = int(tokens[0])
    
    if holeNumber < 0:
        raise IOError("Invalid file format (the hole number must be nonnegative)")

    pslg.holes = [None for i in range(0, holeNumber)]
    for i in range(0, holeNumber):
        line = getLine(file)
        tokens = string.split(line)
        
        if len(tokens) != 3:
            raise IOError("Invalid file format (hole " + str(i) + " has invalid format)")
        
        index = int(tokens[0])
        x = float(tokens[1])
        y = float(tokens[2])
        
        pslg.holes[index] = Pslg.Hole(x, y)
    return    

def loadRegions(file, pslg):
    line = getLine(file)
    tokens = string.split(line)
    
    if len(tokens) != 1:
        raise IOError("Invalid file format (the region format descriptor must contain exactly one integer)")
    
    regionNumber = int(tokens[0])
    
    if regionNumber < 0:
        raise IOError("Invalid file format (the region number must be nonnegative)")

    pslg.regions = [None for i in range(0, regionNumber)]
    for i in range(0, regionNumber):
        line = getLine(file)
        tokens = string.split(line)
        
        if len(tokens) != 3 and len(tokens) != 4 and len(tokens) != 5:
            raise IOError("Invalid file format (region " + str(i) + " has invalid format)")
        
        index = int(tokens[0])
        x = float(tokens[1])
        y = float(tokens[2])
        id = None
                
        if len(tokens) > 3:
            id = int(tokens[3])
        
        pslg.regions[index] = Pslg.Region(x, y)
        if id is not None:
            pslg.regions[index].id = id
    return 

def loadSegments(file, pslg):
    line = getLine(file)
    tokens = string.split(line)
    
    if len(tokens) != 2:
        raise IOError("Invalid file format (the segment format descriptor must contain exactly two integers)")
    
    segmentNumber = int(tokens[0])
    boundaryMarkers = int(tokens[1])
    
    if segmentNumber < 0:
        raise IOError("Invalid file format (the segment number must be nonnegative)")
    if boundaryMarkers != 0 and boundaryMarkers != 1:
        raise IOError("Invalid file format (number of boundary markers must be either 0 or 1)")

    pslg.segments = [None for i in range(0, segmentNumber)]
    for i in range(0, segmentNumber):
        line = getLine(file)
        tokens = string.split(line)
        
        if len(tokens) != 3 + boundaryMarkers:
            raise IOError("Invalid file format (segment " + str(i) + " has invalid format)")
        
        index = int(tokens[0])
        startpointIndex = int(tokens[1])
        endpointIndex = int(tokens[2])
        
        pslg.segments[index] = Pslg.Segment(pslg.points[startpointIndex], pslg.points[endpointIndex])
    return
    
def loadEleHeader(file):
    line = getLine(file)
    tokens = string.split(line)
    
    if len(tokens) != 3:
        raise IOError("Invalid file format (element format descriptor must contain exacly 3 integers)")
    
    trianglesNumber = int(tokens[0])
    nodesNumber = int(tokens[1])
    attributesNumber = int(tokens[2])
    
    if trianglesNumber < 0:
        raise IOError("Invalid file format (the node triangle must be nonnegative)")
    if nodesNumber != 3:
        raise IOError("Invalid file format (the node number per element must be 3)")
    if attributesNumber != 0 and attributesNumber != 1:
        raise IOError("Invalid file format (the attributes number must either zero or one)")
    
    return (trianglesNumber, nodesNumber, attributesNumber)
    
def loadNodeHeader(file):
    line = getLine(file)
    tokens = string.split(line)
    
    if len(tokens) != 4:
        raise IOError("Invalid file format (point format descriptor must contain exacly 4 integers)")
    
    nodeNumber = int(tokens[0])
    dimension = int(tokens[1])
    attributes = int(tokens[2])
    boundaryMarkers = int(tokens[3])
    
    if nodeNumber < 0:
        raise IOError("Invalid file format (the node number must be nonnegative)")
    if dimension != 2:
        raise IOError("Invalid file format (the dimesion must be 2)")
    if boundaryMarkers != 0 and boundaryMarkers != 1:
        raise IOError("Invalid file format (number of boundary markers must be either 0 or 1)")
    if attributes < 0:
        raise IOError("Invalid file format (the atribute number must be nonnegative)")
    
    return (nodeNumber, dimension, boundaryMarkers, attributes)

def loadNodes(file, pslg, nodeNumber, dimension, boundaryMarkers, attributes):
    pslg.points = [None for i in range(0, nodeNumber)]
    for i in range(0, nodeNumber):
        line = getLine(file)
        tokens = string.split(line)
        if len(tokens) != 1 + dimension + attributes + boundaryMarkers:
            raise IOError("Invalid file format (point " + str(i) + " has invalid format)")
        index = int(tokens[0])
        x = float(tokens[1])
        y = float(tokens[2])
        pslg.points[index] = Pslg.GridPoint(x,y)
        pslg.points[index].index = index
        if boundaryMarkers == 1:
            marker = int(tokens[3 + attributes])
            pslg.points[index].boundaryMarker = marker
    return    

def getLine(file):
    line = string.strip(file.readline())
    while line[0] == "#":
        line = string.strip(file.readline())
    return line