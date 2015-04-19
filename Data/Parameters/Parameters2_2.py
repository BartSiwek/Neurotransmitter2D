class Parameters:
    #Omega three section identifier
    omegaThreeIdentifier = 1

    #Omega d (border) segment identifier
    omegaDIdentifier = 2

    #Define the filename root to use
    filenameRoot = "Kolbka2"
        
    #Define the experiment number
    experimentNumber = "2"

    #Constructor
    def __init__(self):
        self.omega = None
        self.omegaArea = None
        self.omegaThree = None
        self.omegaThreeArea = None
        self.omegaD = None
        self.omegaDLength = None
        self.n = None        
        self.diffusionTensor = None
        self.releaseStart = None
        self.releaseDuration = None
        self.productionThreshold = None
        self.deltaT = None
        self.tEnd = None
        self.maxDiff = None
        self.maxIterativeDiff = None
        self.reportEpoch = None
   
    def initialize(self, pslg):
        #Space scale factor     
        scaleFactor = 5.0
          
        #Omega three and omega
        self.omegaThree = []
        self.omegaThreeArea = 0.0
        self.omega = []
        self.omegaArea = 0.0
        for element in pslg.elements:
            if element.id == Parameters.omegaThreeIdentifier:
                self.omegaThree.append(element)
                self.omegaThreeArea += element.getArea()
            self.omega.append(element)
            self.omegaArea += element.getArea()

        #OmegaD
        self.omegaD = []
        self.omegaDLength = 0.0
        for segment in pslg.segments:
            if segment.getBoundaryMarker() == Parameters.omegaDIdentifier:
                for element in pslg.elements:
                    if element.isSideOf(segment):
                        self.omegaD.append((segment, element))
                        self.omegaDLength += segment.getLength()
        
        #Initial density function
        initialDensityValue = 84000.0 / self.omegaArea
        print "Initial density value: " + str(initialDensityValue)
        def initialDensity(x, y):
            return initialDensityValue
        self.initialDensity = initialDensity
        
        #Release efficiency function
        releaseEfficiencyValue = scaleFactor * 300.0 * self.omegaArea / (84000.0 * self.omegaDLength * 0.0004)
        print "Release efficiency value: " + str(releaseEfficiencyValue)
        def releaseEfficiency(t):
            if(t % 1.0 < 0.5):
                if(0.0123 + 1E-9 < (t % 0.025) and (t % 0.025) <= 0.0127 + 1E-9):
                    return releaseEfficiencyValue
                else:
                    return 0.0
            else:
                if(0.0248 + 1E-9 < (t % 0.05) and (t % 0.05) <= 0.0252 + 1E-9):
                    return releaseEfficiencyValue
                else:
                    return 0.0            
        self.releaseEfficiency = releaseEfficiency
        
        #Production effciency
        productionEffciencyValue = 1E-3 * releaseEfficiencyValue * self.omegaDLength / self.omegaThreeArea
        print "Production effciency value: " + str(productionEffciencyValue)
        def productionEffciency(x, y):
            return productionEffciencyValue
        self.productionEffciency = productionEffciency
        
        #Diffusion tensor [[x,x], [x,y], [y,x], [y,y]]
        diffusionValue = 1E-2 * 300.0 / (scaleFactor**2.0)
        print "Diffusion value: " + str(diffusionValue)
        self.diffusionTensor = [[lambda x, y:  diffusionValue, lambda x, y:  0.0 ],
                                [lambda x, y:  0.0,            lambda x, y:  diffusionValue]]
        
        #Release start
        self.releaseStart = None
        
        #Release duration
        self.releaseDuration = None

        #Production threshold
        self.productionThreshold = 70000.0 / self.omegaThreeArea
        
        #Time step
        self.deltaT = 1E-4
        
        #End time 
        self.tEnd = 5.0
        
        #Max solving difference
        self.maxDiff = 1E-9
        
        #Max solving difference for iterative method
        self.maxIterativeDiff = 1E-30
                
        #Set the number of elements
        self.n = len(pslg.points)
        
        #Epoch for reporting errors
        self.reportEpoch = 100
        
        return