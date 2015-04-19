import os.path

def GetMeshFilename(filenameRoot):
    return "..\\..\\Data\\Meshes\\" + filenameRoot + ".1.ele"

def GetResultsFilename(filenameRoot, experimentNumber):
    return "..\\..\\Data\\Results\\" + filenameRoot + "_" + experimentNumber + ".fem"

def GetReleaseFilename(filenameRoot, experimentNumber):
    return "..\\..\\Data\\Results\\" + filenameRoot + "_" + experimentNumber + ".release"

def GetResultsGraphicsDir(filenameRoot, experimentNumber):
    returnValue = "..\\..\\Data\\Simulations\\" + filenameRoot + "_" + experimentNumber
    if(not os.path.isdir(returnValue)):
      os.mkdir(returnValue)
    return returnValue

def GetVesiclesFilename(filenameRoot, experimentNumber):
    return "..\\..\\Data\\Results\\" + filenameRoot + "_" + experimentNumber + ".vesicles"