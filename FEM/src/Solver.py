import numpy, scipy, scipy.sparse, scipy.sparse.linalg, scipy.linalg, pylab
import FemIo, Assembler

def Solve(pslg, slopeFunctions, parameters, G, A, BPrime, femFilename, releaseFilename):   
    #Initialize the variables
    deltaT = parameters.deltaT
    tEnd = parameters.tEnd

    #Open the output file
    resultsFile = open(femFilename, "a")
    releaseFile = open(releaseFilename, "a")
    try:     
        currentResults = FemIo.loadLastFemresult(femFilename)
        if(currentResults is None):          
            #Create inital vector
            zt = scipy.zeros((parameters.n, 1))
            for i in range(0, parameters.n):
                zt[i,0] = parameters.initialDensity(pslg.points[i].x, pslg.points[i].y)
            
            #Save initial results (if the density is zero the release has to be zero also)
            FemIo.saveHeader(resultsFile, int(tEnd/deltaT)+1, parameters.n)
            FemIo.saveResult(resultsFile, (0.0, zt))
            FemIo.saveRelease(releaseFile, (0.0, 0.0))
         
            #Set initial time
            t = 0
        else:
            #Create inital vector
            t = currentResults[0]
            zt = currentResults[1]
         
        #Set initial values
        MostOfLeftSide = G - (deltaT / 2.0) * A
        PartOfRightSide = G + (deltaT / 2.0) * A  
          
        #Calculate the release factor
        ReleaseFactor = (G.todense().I) * BPrime
          
        #Iterate over time
        while t < tEnd:
            #Calculate next vector
            zNext = SolveInTime(slopeFunctions, parameters, MostOfLeftSide, PartOfRightSide, BPrime, zt, t)

            #Calculate the release
            releaseSum = CalculateReleaseSumInTime(parameters, ReleaseFactor, zNext, t)
            
            #Report min/max
            reportMinMax(zNext.min(), zNext.max())
               
            #Save the result
            FemIo.saveResult(resultsFile, (t + deltaT, zNext))
            FemIo.saveRelease(releaseFile, (t + deltaT, releaseSum))
               
            #Go to next iteration
            zt = zNext
            t += deltaT
    finally:
        resultsFile.close()
        releaseFile.close()
    return

def CalculateReleaseSumInTime(parameters, ReleaseFactor, zt, t):
    #Initialize the variables
    deltaT = parameters.deltaT
    alpha = parameters.releaseEfficiency
    
    #Calculate the release sum
    releaseT = alpha(t + deltaT) * ReleaseFactor * zt
    releaseSum = sum(releaseT)[0,0]
    return releaseSum

def SolveInTime(slopeFunctions, parameters, MostOfLeftSide, PartOfRightSide, BPrime, zt, t):
    #Initialize the variables
    deltaT = parameters.deltaT
    alpha = parameters.releaseEfficiency

    #Report solving stared
    reportSolvingForTime(t + deltaT)
      
    #Calculate the iteration independent values
    prodT = Assembler.computeProductionVector(zt, slopeFunctions, parameters)
    LeftSide = MostOfLeftSide - (deltaT / 2.0) * alpha(t + deltaT) * BPrime
    MostOfRightSide = (PartOfRightSide + (deltaT / 2.0) * alpha(t) * BPrime) * zt + \
                       (deltaT / 2.0) * prodT
       
    #Set the initial value
    zPrev = scipy.zeros((parameters.n, 1))
    for i in range(0, parameters.n):
        zPrev[i,0] = zt[i,0]
    
    #Iterate
    diff = 10000
    epoch = 0
    while diff >= parameters.maxDiff:
        zNew = SolveSingleStep(slopeFunctions, parameters, deltaT, LeftSide, MostOfRightSide, zPrev);
        diff = abs(zPrev - zNew).max()
               
        if (epoch + 1) % parameters.reportEpoch == 0:
            reportSolutionChange(epoch, diff)
                
        zPrev = zNew
        epoch += 1
    #Return the result
    return zPrev

def SolveSingleStep(slopeFunctions, parameters, deltaT, LeftSide, MostOfRightSide, zPrev):
    prodPrev = Assembler.computeProductionVector(zPrev, slopeFunctions, parameters)
    RightSide = (deltaT / 2.0) * prodPrev + MostOfRightSide
    zNew = scipy.sparse.linalg.bicgstab(LeftSide, RightSide, zPrev, parameters.maxIterativeDiff)[0]
    zNew = scipy.matrix(zNew).transpose()    
    return zNew;

def reportSolvingForTime(t):
    print "Solving for time " + str(t)
    
def reportMinMax(min, max):
    print "Max (current step): " + str(max) 
    print "Min (current step): " + str(min)
    
def reportSolutionChange(epoch, diff):
    print "Solution change [" + str(epoch + 1) + "]: " + str(diff)