import FilenameComposer
import Parameters, FemIo

class ReleaseCalculator:   
    def __init__(self, parameters):
        self.eleFilename = FilenameComposer.GetMeshFilename(Parameters.Parameters.filenameRoot)
        self.femFilename = FilenameComposer.GetResultsFilename(Parameters.Parameters.filenameRoot, Parameters.Parameters.experimentNumber)
        self.vesiclesFilename = FilenameComposer.GetVesiclesFilename(Parameters.Parameters.filenameRoot, Parameters.Parameters.experimentNumber)
        self.parameters = parameters

    def run(self):
        #Load mesh and parameters 
        self.pslg = FemIo.loadEle(self.eleFilename)
        self.parameters.initialize(self.pslg)
        
        #Load results
        self.results = FemIo.loadFem(self.femFilename)
               
        #Iterate over parameters
        spatialSums = []
        for result in self.results:               
            currentSum = 0.0
            for segment in self.parameters.omegaD:
                rhoStart = result[1][segment[0].startpoint.index]
                rhoEnd = result[1][segment[0].endpoint.index]
                currentSum += segment[0].getLength() * (rhoStart + rhoEnd) / 2.0
            spatialSums.append((result[0], currentSum))
        
        vesicleFile = open(self.vesiclesFilename, "w")
        for i in range(0, len(spatialSums)-1):
            alphaValue = self.parameters.releaseEfficiency(spatialSums[i][0])           
            value = alphaValue * parameters.deltaT * (spatialSums[i][1] + spatialSums[i+1][1]) / 2.0
            vesicleFile.write(str(spatialSums[i][0]) + "\t" + str(value) + "\n")
        vesicleFile.close()    

if __name__ == '__main__':
    parameters = Parameters.Parameters()
    releaseCalculator = ReleaseCalculator(parameters)
    releaseCalculator.run()