import unittest, numpy, scipy, scipy.sparse
import Pslg, ElementAwarePslg, Parameters, ShapeFunctions, Assembler
import Solver

class SolverTest(unittest.TestCase):
    def testSolveInTime1(self):
        #Define grid
        pslg = ElementAwarePslg.ElementAwarePslg()
        
        x1 = Pslg.GridPoint(0,-2)
        x2 = Pslg.GridPoint(0,0)
        x3 = Pslg.GridPoint(0,2)
        x4 = Pslg.GridPoint(-2,0)
        x5 = Pslg.GridPoint(2,0)
        
        x1.index = 0
        x2.index = 1
        x3.index = 2
        x4.index = 3
        x5.index = 4
        
        x1.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        x3.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        x5.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        
        s1 = Pslg.Segment(x1, x5)
        s2 = Pslg.Segment(x5, x3)
        s3 = Pslg.Segment(x3, x4)
        s4 = Pslg.Segment(x4, x1)
        s5 = Pslg.Segment(x4, x2)
        s6 = Pslg.Segment(x2, x5)
        s7 = Pslg.Segment(x3, x2)
        s8 = Pslg.Segment(x2, x1)
        
        e1 = ElementAwarePslg.Element(x1, x2, x4, 0, 0)
        e2 = ElementAwarePslg.Element(x1, x2, x5, Parameters.Parameters.omegaThreeIdentifier, 1)
        e3 = ElementAwarePslg.Element(x4, x2, x3, 0, 2)
        e4 = ElementAwarePslg.Element(x3, x2, x5, Parameters.Parameters.omegaThreeIdentifier, 3)
        
        pslg.points.extend([x1, x2, x3, x4, x5])
        pslg.segments.extend([s1, s2, s3, s4, s5, s6, s7, s8])
        pslg.elements.extend([e1, e2, e3, e4])
               
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
        
        #Tweak the parameters
        parameters.diffusionTensor = [[lambda x, y: 1.0, lambda x, y: 1.0],
                                      [lambda x, y: 1.0, lambda x, y: 1.0]]        
        parameters.productionEffciency = lambda x,y: 1.0
        parameters.productionThreshold = 1.0
        parameters.releaseEfficiency = lambda t: 0.0
        
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
        
        #Prepare matrices
        G = scipy.sparse.csc_matrix(scipy.diag([1,1,1,1,1]))
        BPrime = scipy.sparse.csc_matrix(scipy.zeros((5,5)))
        
        #Prepare vector
        zt = numpy.matrix([2, 2, 2, 2, 2]).transpose()
        
        #Set time
        t = 0
        
        #Solve
        zNew = Solver.SolveInTime(shapeFunctions, parameters, G, G, BPrime, zt, t)
    
        #Assert
        for i in range(0,5):
            self.assertEqual(zt[i,0], zNew[i,0])
                
    def testSolveSingleStep1(self):
        #Define grid
        pslg = ElementAwarePslg.ElementAwarePslg()
        
        x1 = Pslg.GridPoint(0,-2)
        x2 = Pslg.GridPoint(-2,0)
        x3 = Pslg.GridPoint(0,0)
        x4 = Pslg.GridPoint(2,0)
        x5 = Pslg.GridPoint(0,2)
        
        x1.index = 0
        x2.index = 1
        x3.index = 2
        x4.index = 3
        x5.index = 4
        
        x1.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        x4.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        x5.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        
        s1 = Pslg.Segment(x1, x4)
        s2 = Pslg.Segment(x4, x5)
        s3 = Pslg.Segment(x5, x2)
        s4 = Pslg.Segment(x2, x1)
        s5 = Pslg.Segment(x1, x3)
        s6 = Pslg.Segment(x3, x5)
        s7 = Pslg.Segment(x2, x3)
        s8 = Pslg.Segment(x3, x4)        
        
        e1 = ElementAwarePslg.Element(x2, x3, x5, Parameters.Parameters.omegaThreeIdentifier, 0)
        e2 = ElementAwarePslg.Element(x3, x4, x5, 0, 1)
        e3 = ElementAwarePslg.Element(x2, x1, x3, Parameters.Parameters.omegaThreeIdentifier, 2)
        e4 = ElementAwarePslg.Element(x3, x1, x4, 0, 3)
        
        pslg.points.extend([x1, x2, x3, x4, x5])
        pslg.segments.extend([s1, s2, s3, s4, s5, s6, s7, s8])
        pslg.elements.extend([e1, e2, e3, e4])
        
        #Create the coefficient vector
        zOriginal = numpy.matrix([0, 0, 0, 0, 0]).transpose()
        zPrev = numpy.matrix([0, 0, 0, 0, 0]).transpose() 
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
              
        #Tweak the parameters
        parameters.diffusionTensor = [[lambda x, y: 1.0, lambda x, y: 1.0],
                                      [lambda x, y: 1.0, lambda x, y: 1.0]]        
        parameters.productionEffciency = lambda x,y: 1.0
        parameters.productionThreshold = 1.0
        parameters.releaseEfficiency = lambda t: 0.0
        parameters.initialDensity = lambda x,y: 0.0
        
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
        
        #Get the matrices
        (G, A, BPrime) = Assembler.precomputeMatrices(shapeFunctions, parameters)
        P = Assembler.computeProductionVector(zOriginal, shapeFunctions, parameters)
        
        #Set time
        parameters.deltaT = 0.01
        parameters.tEnd = 1.0
        t = 0
        
        #Compute parts of equation
        LeftSide = G - parameters.deltaT / 2.0 * (A + parameters.releaseEfficiency(t + parameters.deltaT) * BPrime)
        MostOfRightSide = (G + parameters.deltaT / 2.0 * (A + parameters.releaseEfficiency(t) * BPrime)) * zOriginal + parameters.deltaT / 2.0 * P
                
        #Perform test
        zNew = Solver.SolveSingleStep(shapeFunctions,
                                      parameters,
                                      parameters.deltaT,
                                      LeftSide,
                                      MostOfRightSide,
                                      zPrev)
        
        #Test values
        expected = numpy.matrix([1.0/11.0, 15.0/44.0, 1.0/8.0, -1.0/11.0, 7.0/44.0]).transpose()       
        self.assertTrue((abs(zNew - expected) < 1E-10).all())
            
if __name__ == '__main__':
    unittest.main()