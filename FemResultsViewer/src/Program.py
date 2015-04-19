import matplotlib
matplotlib.use("GTK")
import scipy, numpy, pylab, time, matplotlib.mlab, matplotlib.pyplot, matplotlib.cm
import os, gtk, gobject, bisect, psyco
import FemIo, FilenameComposer

class FemResultsViewer:
    RootFilename = "Kolbka2"
    ExperimentNumber = "2"
    
    XSaptialDelta = 0.002
    YSaptialDelta = 0.002
    Dpi = 120
    TimeStep = 1E-4
    EndTime = None
    StartImage = 0
    
    def __init__(self):
        self.simulationDir = FilenameComposer.GetResultsGraphicsDir(FemResultsViewer.RootFilename, FemResultsViewer.ExperimentNumber)
        self.eleFilename = FilenameComposer.GetMeshFilename(FemResultsViewer.RootFilename) 
        self.femFilename = FilenameComposer.GetResultsFilename(FemResultsViewer.RootFilename, FemResultsViewer.ExperimentNumber)
    
    def run(self):
        self.ReportMeshLoadingStarted()
        self.pslg = FemIo.loadEle(self.eleFilename)
        self.ReportMeshLoadingFinished()
        self.ReportFemResultsLoadingStarted()
        self.results = FemIo.loadFem(self.femFilename)
        self.ReportFemResultsLoadingFinished()
        
        #Compute grid points
        self.ReportGridPreparingStarted()
        xGridPoints = numpy.arange(0.0, 1.0 + FemResultsViewer.XSaptialDelta, FemResultsViewer.XSaptialDelta)
        yGridPoints = numpy.arange(0.0, 1.0 + FemResultsViewer.YSaptialDelta, FemResultsViewer.YSaptialDelta)        
        x, y = numpy.meshgrid(xGridPoints, yGridPoints)
        self.ReportGridPreparingFinished()
        
        #Compute display data
        self.ReportComputingGridValuesStarted()
        self.ComputeDisplayData(x,y)
        self.ReportComputingGridValuesFinished()
        
        #Make movie
        self.ReportMovieMakingStarted()
        self.MakeMovie()
        self.ReportMovieMakingFinished()  
        
        #Return
        return
    
    def MakeMovie(self):
        os.chdir(self.simulationDir)
        os.system("mencoder mf://tmp*.png -mf type=png:fps=100 -ovc lavc -of lavf -lavcopts vcodec=mpeg4 -oac copy -o simulation.avi")
        return
    
    def ComputeDisplayData(self, xGrid, yGrid):
        #Compute times
        if(FemResultsViewer.TimeStep is None):
            FemResultsViewer.TimeStep = self.results[1][0]
        if(FemResultsViewer.EndTime is None):
            FemResultsViewer.EndTime = self.results[-1][0] + FemResultsViewer.TimeStep 
        
        #Compute the sizes
        xSize = len(xGrid[0])        
        ySize = len(xGrid)
        timeSteps = int(FemResultsViewer.EndTime/FemResultsViewer.TimeStep)
        
        #Compute point element assignment
        self.ReportComputingPointElementAssignmentStarted()
        pointElementAssignment = [[None for k in range(0,xSize)] for j in range(0,ySize)]
        for element in self.pslg.elements:
            xMin = yMin =  1000000000000
            xMax = yMax = -1000000000000
            for point in element.points:
                xMin = min(xMin, point.x)
                yMin = min(yMin, point.y)
                xMax = max(xMax, point.x)
                yMax = max(yMax, point.y)
            rectangle = self.GetBoundingRectangle(xMin, yMin, xMax, yMax)
            for xIndex in range(rectangle[0], rectangle[2]+1):
                for yIndex in range(rectangle[1], rectangle[3]+1):
                    if(pointElementAssignment[yIndex][xIndex] is None and self.CheckPointInElement(element, xGrid[yIndex][xIndex], yGrid[yIndex][xIndex])):
                        pointElementAssignment[yIndex][xIndex] = element
        self.ReportComputingPointElementAssignmentFinished()
        
        #Compute time coefficients
        self.ReportCachingResultsInTimeStarted()
        coeffs = []
        for tIndex in range(0,timeSteps):
            t = tIndex*FemResultsViewer.TimeStep
            coeffs.append(self.FindCoeffInTime(t))
        self.ReportCachingResultsInTimeFinished()
        
        #Compute min/max values
        displayMax = -1000000000000
        displayMin =  1000000000000
        
        #Compute min/max values
        self.ReportComputingMinMaxStarted()
        percent = 0
        for tIndex in range(0,timeSteps):
            coeff = coeffs[tIndex]
            for coeffValue in coeff:
                displayMax = max(displayMax, coeffValue)
                displayMin = min(displayMin, coeffValue)
        self.ReportComputingMinMaxFinished(displayMin, displayMax)
                
        #Compute grid values
        self.ReportRenderingStarted()
        for tIndex in range(FemResultsViewer.StartImage,timeSteps):
            displayData = [[0.0 for k in range(0,xSize)] for j in range(0,ySize)]
            coeff = coeffs[tIndex]
            for xIndex in range(0,xSize):
                for yIndex in range(0,ySize):                        
                    x,y = xGrid[yIndex][xIndex], yGrid[yIndex][xIndex]
                    e = pointElementAssignment[yIndex][xIndex]
                    value = self.GetValue(coeff, e, x, y)
                    displayData[yIndex][xIndex] = value
            self.RenderFrame(displayData, displayMin, displayMax, tIndex)
        self.ReportRenderingFinished()
        
        #Return
        return
        
    def RenderFrame(self, currentFrameData, min, max, frameNumber):
        #Report
        self.ReportRenderingFrame(frameNumber)
        
        #Render
        figure = matplotlib.pyplot.figure(1)
        axes = figure.gca()
        image = matplotlib.pyplot.imshow(currentFrameData, 
                                         interpolation='bilinear', 
                                         origin='lower',
                                         cmap=matplotlib.cm.hot, 
                                         extent=(0,1,0,1),
                                         axes=axes,
                                         animated=True,
                                         vmin=min,
                                         vmax=max)
        colorbar = matplotlib.pyplot.colorbar(image, 
                                              orientation='horizontal')
        
        #Save & clean up
        filename = self.simulationDir + ("\\tmp%06d.png" % (frameNumber + 1))
        figure.savefig(filename, dpi=FemResultsViewer.Dpi)
        figure.clf()
        return
        
    def GetBoundingRectangle(self, xMin, yMin, xMax, yMax):
        #Get indexes
        xMinIndex = int(xMin/FemResultsViewer.XSaptialDelta)
        yMinIndex = int(yMin/FemResultsViewer.YSaptialDelta)
        xMaxIndex = int(xMax/FemResultsViewer.XSaptialDelta + 1.0)
        yMaxIndex = int(yMax/FemResultsViewer.YSaptialDelta + 1.0)
        
        #Get nearest
        xMax = xMaxIndex * FemResultsViewer.XSaptialDelta
        yMax = yMaxIndex * FemResultsViewer.YSaptialDelta
        
        #Make sure the uppor bound is valid
        if(xMax > 1.0):
            xMaxIndex -= 1
        if(yMax > 1.0):
            yMaxIndex -= 1
        
        return (xMinIndex, yMinIndex, xMaxIndex, yMaxIndex)
        
    def CheckPointInElement(self, element, x, y):
        u, v = self.FindTriangleCoords(element, x, y)
        return (u >= 0.0) and (v >= 0.0) and (u + v <= 1.0)
                        
    def FindCoeffInTime(self, t):
        coeff = None
        for tIndex in range(0, len(self.results)-1):
            currentCoeff = self.results[tIndex]
            nextCoeff = self.results[tIndex+1]
            if (currentCoeff[0] <= t and t <= nextCoeff[0]):
                timeDiff = nextCoeff[0] - currentCoeff[0]
                timeShift = t - currentCoeff[0]
                percent = timeShift / timeDiff
                coeff = [(1 - percent) * currentCoeff[1][i] + percent * nextCoeff[1][i] for i in range(0,len(currentCoeff[1]))]
                break
        return coeff
        
    def GetValue(self, coeff, e, x, y):
        if(e is None):
            return 0.0
               
        if(coeff is None):
            return 0.0
        
        u,v = self.FindTriangleCoords(e, x, y)
        value = (1.0 - u - v) * coeff[e.x1.index] + u * coeff[e.x2.index] + v * coeff[e.x3.index]
        return value
        
    def FindTriangleCoords(self, element, x, y):
        v0 = (element.x2.x - element.x1.x, element.x2.y - element.x1.y)
        v1 = (element.x3.x - element.x1.x, element.x3.y - element.x1.y)
        v2 = (x            - element.x1.x,            y - element.x1.y)
            
        dot00 = self.DotProduct(v0, v0)
        dot01 = self.DotProduct(v0, v1)
        dot02 = self.DotProduct(v0, v2)
        dot11 = self.DotProduct(v1, v1)
        dot12 = self.DotProduct(v1, v2)
            
        invDenom = 1.0 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * invDenom 
        v = (dot00 * dot12 - dot01 * dot02) * invDenom
        
        return u, v
        
    def DotProduct(self, u, v):
        return u[0] * v[0] + u[1] * v[1]
        
    def ReportMeshLoadingStarted(self):
        print "Loading mesh from file [" + self.eleFilename + "]"
        
    def ReportMeshLoadingFinished(self):
        print "Loading mesh from file finished..."
        print "Nodes: " + str(len(self.pslg.points))
        print "Segments: " + str(len(self.pslg.segments))
        print "Elements: " + str(len(self.pslg.elements))
        
    def ReportFemResultsLoadingStarted(self):
        print "Loading FEM results from file [" + self.femFilename + "]"
        
    def ReportFemResultsLoadingFinished(self):
        print "Loading FEM results from file finished..."
        print "Time steps: " + str(len(self.results))
        print "Start time: " + str(self.results[0][0])
        print "End time: " + str(self.results[-1][0])
        print "Variables: " + str(len(self.results[0][1]))
        
    def ReportGridPreparingStarted(self):
        print "Preparing grid..."
        
    def ReportGridPreparingFinished(self):
        print "Preparing finished..."        
    
    def ReportComputingGridValuesStarted(self):
        print "Computing grid values..."
        
    def ReportComputingPointElementAssignmentStarted(self):
        print "Computing point element assignment started..."
        
    def ReportComputingPointElementAssignmentFinished(self):
        print "Computing point element assignment finished..."                
        
    def ReportCachingResultsInTimeStarted(self):
        print "Caching results in time started..."
        print "Animation start time: " + str(0.0)
        print "Animation time step: " + str(FemResultsViewer.TimeStep)
        print "Animation x spatial step: " + str(FemResultsViewer.XSaptialDelta)
        print "Animation y spatial step: " + str(FemResultsViewer.YSaptialDelta)
        
    def ReportCachingResultsInTimeFinished(self):
        print "Caching results in time finished..."        
        
    def ReportComputingMinMaxStarted(self):
        print "Computing min/max density values started..."
        
    def ReportComputingMinMaxFinished(self, min, max):
        print "Computing min/max density values started..."
        print "Min: " + str(min)
        print "Max: " + str(max)
        
    def ReportRenderingStarted(self):
        print "Rendering started..."
        
    def ReportRenderingFrame(self, frameNumber):
        print "Rendering frame #%06d..." % (frameNumber + 1)        

    def ReportRenderingFinished(self):
        print "Rendering finished..."
        
    def ReportComputingGridValuesFinished(self):
        print "Computing grid values finished..."
    
    def ReportMovieMakingStarted(self):
        print "Making movie [simulation.mpg] started..."
        
    def ReportMovieMakingFinished(self):
        print "Making movie [simulation.mpg] finished..."   
                
if __name__ == '__main__':
    psyco.full()
    viewer = FemResultsViewer()
    viewer.run()