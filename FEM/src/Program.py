import time
import psyco
import FilenameComposer
import Parameters, Statistics, FemIo
import ShapeFunctions
import GaussPointFactory, Integrator, Assembler, Solver

class FEM:
    def __init__(self, parameters):
        self.eleFilename = FilenameComposer.GetMeshFilename(Parameters.Parameters.filenameRoot) 
        self.femFilename = FilenameComposer.GetResultsFilename(Parameters.Parameters.filenameRoot, Parameters.Parameters.experimentNumber)
        self.releaseFilename = FilenameComposer.GetReleaseFilename(Parameters.Parameters.filenameRoot, Parameters.Parameters.experimentNumber)
        self.parameters = parameters
        
    def run(self):
        #Report start
        self.reportProgamStarted()
        
        #Load PSLG
        self.reportMeshLoadingStarted()
        self.pslg = FemIo.loadEle(self.eleFilename)
        self.parameters.initialize(self.pslg)
        self.reportMeshLoadingFinished()
    
        #Create shape functions
        self.reportBuildingShapeFunctionsStarted()
        slopeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(self.pslg)
        self.reportBuildingShapeFunctionsFinished()
    
        #Precompute matrices
        self.reportPrecomputingMatricesStarted()
        (G, A, BPrime) = Assembler.precomputeMatrices(slopeFunctions, self.parameters)
        self.reportPrecomputingMatricesFinished()
    
        #Solve
        self.reportSolvingStarted()
        Solver.Solve(self.pslg, slopeFunctions, self.parameters, G, A, BPrime, self.femFilename, self.releaseFilename)
        self.reportSolvingFinished()
    
        #Report finished
        self.reportProgamFinished()

    def reportProgamStarted(self):
        self.startTime = time.clock()
        print "Starting FEM computation " + time.strftime("on %d %b %Y at %H:%M:%S")

    def reportMeshLoadingStarted(self):
        print "Loading mesh from file [" + self.eleFilename + "]"

    def reportMeshLoadingFinished(self):
        print "Loading mesh from file finished..."
        print "Nodes: " + str(len(self.pslg.points))
        print "Segments: " + str(len(self.pslg.segments))
        print "Elements: " + str(len(self.pslg.elements))
        print ""
        
        print "Omega elements: " + str(len(self.parameters.omega))
        print "Omega area: " + str(self.parameters.omegaArea)
        print "Omega three elements: " + str(len(self.parameters.omegaThree))
        print "Omega three area: " + str(self.parameters.omegaThreeArea)
        print "Omega d segments: " + str(len(self.parameters.omegaD))
        print "Omega d length: " + str(self.parameters.omegaDLength)       
        print ""
        
        print "Mesh statistics..."
        angleMinMax = Statistics.ComputeElementAngleRange(self.parameters)
        print "Element angle min: " + str(angleMinMax[0])
        print "Element angle max: " + str(angleMinMax[1])
        segmentLengthMinMax = Statistics.ComputeSegmentLengthRange(self.parameters)
        print "Segment length min: " + str(segmentLengthMinMax[0][0])
        print "Min segment: " + str(segmentLengthMinMax[0][1]) + " -> " + str(segmentLengthMinMax[0][2])
        print "Segment length max: " + str(segmentLengthMinMax[1][0])
        print "Max segment: " + str(segmentLengthMinMax[1][1]) + " -> " + str(segmentLengthMinMax[1][2])
        print ""

    def reportBuildingShapeFunctionsStarted(self):
        print "Building shape functions..."

    def reportBuildingShapeFunctionsFinished(self):
        print "Building shape functions finished..."

    def reportPrecomputingMatricesStarted(self):
        print "Precomputing matrices..."

    def reportPrecomputingMatricesFinished(self):
        print "Precomputing matrices finished..."

    def reportSolvingStarted(self):
        print "Solving started..."

    def reportSolvingFinished(self):
        print "Solving finished..."

    def reportProgamFinished(self):
        self.stopTime = time.clock()
        print "Finished " + time.strftime("on %d %b %Y at %H:%M:%S")
        print "Total running time: " + str(self.stopTime - self.startTime) + "s"

if __name__ == '__main__':
    psyco.full() 
    parameters = Parameters.Parameters()
    fem = FEM(parameters)
    fem.run()
