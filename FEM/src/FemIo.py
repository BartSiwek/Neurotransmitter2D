import string
import scipy
import PslgIo, ElementAwarePslg

def loadEle(filename):
    pslg = ElementAwarePslg.ElementAwarePslg()
    file = open(filename, "r")
    try:
        PslgIo.readFromFile(file, pslg, filename)
    finally:
        file.close()
    return pslg

def saveFem(filename, femResults):
    #Open the file
    file = open(filename, "w")
    
    #Header
    line = saveHeader(file, len(femResults), femResults[0][1].shape[0])
    
    #Actual contents
    try:
        for solutionDesc in femResults:
            saveResult(file, solutionDesc)
    finally:
        file.close()
    return

def saveResult(file, solutionDesc):
    file.write(str(solutionDesc[0]) + "\n")
    for i in range(0, solutionDesc[1].shape[0]):
        line = "%.12f" % solutionDesc[1][i,0]
        file.write(line + "\n")
    file.flush()

def saveRelease(file, releaseDesc):
    file.write(str(releaseDesc[0]) + "\t" + str(releaseDesc[1]) + "\n")
    file.flush()

def saveHeader(file, timeSteps, variableNumber):
    line = str(timeSteps) + " " + str(variableNumber) + "\n"
    file.write(line)
    file.flush()

def loadFem(filename):
    results = []
    file = open(filename, "r")
    try:
        resultNumber, n = readHeader(file)
        for i in range(0, resultNumber):
            time = float(getLine(file))
            z = []
            for j in range(0, n):
                currentZ = float(getLine(file))
                z.append(currentZ)
            results.append((time, z))
    finally:
        file.close()
    return results

def loadLastFemresult(filename):
    result = None
    file = open(filename, "r")
    try:
        #Skip header
        resultNumber, n = readHeader(file)
        currentLine = getLine(file)        
        while len(currentLine) > 0:            
            #Get the current record
            time = float(currentLine)
            z = []
            for j in range(0, n):
                currentZ = float(getLine(file))
                z.append(currentZ)
            result = (time, z)    
            
            #Get next line
            currentLine = getLine(file)
    except:
        pass
    finally:
        file.close()

    if(result is not None):
        return (result[0], scipy.array([result[1]]).transpose())
    else:
        return None

def readHeader(file):
    headerLine = getLine(file)
    if  len(headerLine) > 0:
        tokens = string.split(headerLine)
        if len(tokens) != 2:
            raise IOError("Invalid file format (header should contain exactly two positive integers)")
        return (int(tokens[0]), int(tokens[1]))
    else:
        raise IOError("Invalid file format (header not found)")

def getLine(file):
    return string.strip(file.readline())