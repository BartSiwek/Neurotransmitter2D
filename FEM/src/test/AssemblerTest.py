import unittest, math, numpy
import Pslg, ElementAwarePslg, Parameters, ShapeFunctions
import Assembler

class AssemblerTest(unittest.TestCase):
    def testGMatrix1(self):
        #Define grid
        pslg = ElementAwarePslg.ElementAwarePslg()
        
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,1)
        p3 = Pslg.GridPoint(2,2)
        p4 = Pslg.GridPoint(0,2)
        p5 = Pslg.GridPoint(2,0)
        
        p1.index = 0
        p2.index = 1
        p3.index = 2
        p4.index = 3
        p5.index = 4
        
        e1 = ElementAwarePslg.Element(p4, p2, p1, Parameters.Parameters.omegaThreeIdentifier, 0)
        e2 = ElementAwarePslg.Element(p4, p2, p3, Parameters.Parameters.omegaThreeIdentifier, 1)
        e3 = ElementAwarePslg.Element(p2, p5, p3, 0, 2)
        e4 = ElementAwarePslg.Element(p1, p2, p5, 0, 3)
        
        pslg.points.extend([p1, p2, p3, p4, p5])
        pslg.elements.extend([e1, e2, e3, e4])
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
              
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
        
        #Get the matrices
        (G, A, BPrime) = Assembler.precomputeMatrices(shapeFunctions, parameters)
        
        #Test symetry
        for i in range(0, len(pslg.points)):
            for j in range(0, len(pslg.points)):
                self.assertAlmostEqual(G[i,j], G[j,i], 9)    
        
        #Test values
        self.assertAlmostEqual(G[0,0], 2.0/3.0, 9)
        self.assertAlmostEqual(G[0,1], 0.0, 9)
        self.assertAlmostEqual(G[0,2], 0.0, 9)
        self.assertAlmostEqual(G[0,3], 0.0, 9)
        self.assertAlmostEqual(G[0,4], 0.0, 9)
        
        self.assertAlmostEqual(G[1,0], 0.0, 9)
        self.assertAlmostEqual(G[1,1], 4.0/3.0, 9)
        self.assertAlmostEqual(G[1,2], 0.0, 9)
        self.assertAlmostEqual(G[1,3], 0.0, 9)
        self.assertAlmostEqual(G[1,4], 0.0, 9)
        
        self.assertAlmostEqual(G[2,0], 0.0, 9)
        self.assertAlmostEqual(G[2,1], 0.0, 9)
        self.assertAlmostEqual(G[2,2], 2.0/3.0, 9)
        self.assertAlmostEqual(G[2,3], 0.0, 9)
        self.assertAlmostEqual(G[2,4], 0.0, 9)
        
        self.assertAlmostEqual(G[3,0], 0.0, 9)
        self.assertAlmostEqual(G[3,1], 0.0, 9)
        self.assertAlmostEqual(G[3,2], 0.0, 9)
        self.assertAlmostEqual(G[3,3], 2.0/3.0, 9)
        self.assertAlmostEqual(G[3,4], 0.0, 9)
        
        self.assertAlmostEqual(G[4,0], 0.0, 9)
        self.assertAlmostEqual(G[4,1], 0.0, 9)
        self.assertAlmostEqual(G[4,2], 0.0, 9)
        self.assertAlmostEqual(G[4,3], 0.0, 9)
        self.assertAlmostEqual(G[4,4], 2.0/3.0, 9)
        
        return
    
    def testGMatrix2(self):
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
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
              
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
        
        #Get the matrices
        (G, A, BPrime) = Assembler.precomputeMatrices(shapeFunctions, parameters)
        
        #Test symetry
        for i in range(0, len(pslg.points)):
            for j in range(0, len(pslg.points)):
                self.assertAlmostEqual(G[i,j], G[j,i], 9)    
        
        #Test values
        self.assertAlmostEqual(G[0,0], 4.0/3.0, 9)
        self.assertAlmostEqual(G[0,1], 0.0, 9)
        self.assertAlmostEqual(G[0,2], 0.0, 9)
        self.assertAlmostEqual(G[0,3], 0.0, 9)
        self.assertAlmostEqual(G[0,4], 0.0, 9)
        
        self.assertAlmostEqual(G[1,0], 0.0, 9)
        self.assertAlmostEqual(G[1,1], 4.0/3.0, 9)
        self.assertAlmostEqual(G[1,2], 0.0, 9)
        self.assertAlmostEqual(G[1,3], 0.0, 9)
        self.assertAlmostEqual(G[1,4], 0.0, 9)
        
        self.assertAlmostEqual(G[2,0], 0.0, 9)
        self.assertAlmostEqual(G[2,1], 0.0, 9)
        self.assertAlmostEqual(G[2,2], 8.0/3.0, 9)
        self.assertAlmostEqual(G[2,3], 0.0, 9)
        self.assertAlmostEqual(G[2,4], 0.0, 9)
        
        self.assertAlmostEqual(G[3,0], 0.0, 9)
        self.assertAlmostEqual(G[3,1], 0.0, 9)
        self.assertAlmostEqual(G[3,2], 0.0, 9)
        self.assertAlmostEqual(G[3,3], 4.0/3.0, 9)
        self.assertAlmostEqual(G[3,4], 0.0, 9)
        
        self.assertAlmostEqual(G[4,0], 0.0, 9)
        self.assertAlmostEqual(G[4,1], 0.0, 9)
        self.assertAlmostEqual(G[4,2], 0.0, 9)
        self.assertAlmostEqual(G[4,3], 0.0, 9)
        self.assertAlmostEqual(G[4,4], 4.0/3.0, 9)
        
        return    
    
    def testAMatrix1(self):
        #Define grid
        pslg = ElementAwarePslg.ElementAwarePslg()
        
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,1)
        p3 = Pslg.GridPoint(2,2)
        p4 = Pslg.GridPoint(0,2)
        p5 = Pslg.GridPoint(2,0)
        
        p1.index = 0
        p2.index = 1
        p3.index = 2
        p4.index = 3
        p5.index = 4
        
        e1 = ElementAwarePslg.Element(p4, p2, p1, 1, 0)
        e2 = ElementAwarePslg.Element(p4, p2, p3, 2, 1)
        e3 = ElementAwarePslg.Element(p2, p5, p3, 3, 2)
        e4 = ElementAwarePslg.Element(p1, p2, p5, 4, 3)
        
        pslg.points.extend([p1, p2, p3, p4, p5])
        pslg.elements.extend([e1, e2, e3, e4])
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
        parameters.diffusionTensor = [[lambda x,y: 2, lambda x,y: 3],
                                      [lambda x,y: 5, lambda x,y: 7]]
              
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
                    
        #Get the matrices
        (G, A, BPrime) = Assembler.precomputeMatrices(shapeFunctions, parameters)
               
        self.assertAlmostEqual(A[0,0], -17.0/2.0, 9)
        self.assertAlmostEqual(A[0,1], 17.0/2.0, 9)
        self.assertAlmostEqual(A[0,2], 0, 9)
        self.assertAlmostEqual(A[0,3], 3.0/4.0, 9)
        self.assertAlmostEqual(A[0,4], -3.0/4.0, 9)
        
        self.assertAlmostEqual(A[1,0], 17.0/2.0, 9)
        self.assertAlmostEqual(A[1,1], -18, 9)
        self.assertAlmostEqual(A[1,2], 17.0/2.0, 9)
        self.assertAlmostEqual(A[1,3], 0.5, 9)
        self.assertAlmostEqual(A[1,4], 0.5, 9)
        
        self.assertAlmostEqual(A[2,0], 0, 9)
        self.assertAlmostEqual(A[2,1], 17.0/2.0, 9)
        self.assertAlmostEqual(A[2,2], -17.0/2.0, 9)
        self.assertAlmostEqual(A[2,3], -3.0/4.0, 9)
        self.assertAlmostEqual(A[2,4], 3.0/4.0, 9)
        
        self.assertAlmostEqual(A[3,0], 7.0/4.0, 9)
        self.assertAlmostEqual(A[3,1], 0.5, 9)
        self.assertAlmostEqual(A[3,2], -7.0/4.0, 9)
        self.assertAlmostEqual(A[3,3], -1.0/2.0, 9)
        self.assertAlmostEqual(A[3,4], 0, 9)
        
        self.assertAlmostEqual(A[4,0], -7.0/4.0, 9)
        self.assertAlmostEqual(A[4,1], 0.5, 9)
        self.assertAlmostEqual(A[4,2], 7.0/4.0, 9)
        self.assertAlmostEqual(A[4,3], 0, 9)
        self.assertAlmostEqual(A[4,4], -1.0/2.0, 9)
        
        return
    
    def testAMatrix2(self):
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
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
        
        #Tweak the parameters
        parameters.diffusionTensor = [[lambda x, y: 1.0, lambda x, y: 1.0],
                                      [lambda x, y: 1.0, lambda x, y: 1.0]]
              
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
        
        #Get the matrices
        (G, A, BPrime) = Assembler.precomputeMatrices(shapeFunctions, parameters)
        
        #Test symetry (this time it is symmetrical due the tensor = 1)
        for i in range(0, len(pslg.points)):
            for j in range(0, len(pslg.points)):
                self.assertAlmostEqual(A[i,j], A[j,i], 9)    
        
        #Test values
        self.assertAlmostEqual(A[0,0], -1.0, 9)
        self.assertAlmostEqual(A[0,1], -1.0/2.0, 9)
        self.assertAlmostEqual(A[0,2], 1.0, 9)
        self.assertAlmostEqual(A[0,3], 1.0/2.0, 9)
        self.assertAlmostEqual(A[0,4], 0.0, 9)
        
        self.assertAlmostEqual(A[1,0], -1.0/2.0, 9)
        self.assertAlmostEqual(A[1,1], -1.0, 9)
        self.assertAlmostEqual(A[1,2], 1.0, 9)
        self.assertAlmostEqual(A[1,3], 0.0, 9)
        self.assertAlmostEqual(A[1,4], 1.0/2.0, 9)
        
        self.assertAlmostEqual(A[2,0], 1.0, 9)
        self.assertAlmostEqual(A[2,1], 1.0, 9)
        self.assertAlmostEqual(A[2,2], -4.0, 9)
        self.assertAlmostEqual(A[2,3], 1.0, 9)
        self.assertAlmostEqual(A[2,4], 1.0, 9)
        
        self.assertAlmostEqual(A[3,0], 1.0/2.0, 9)
        self.assertAlmostEqual(A[3,1], 0.0, 9)
        self.assertAlmostEqual(A[3,2], 1.0, 9)
        self.assertAlmostEqual(A[3,3], -1.0, 9)
        self.assertAlmostEqual(A[3,4], -1.0/2.0, 9)
        
        self.assertAlmostEqual(A[4,0], 0.0, 9)
        self.assertAlmostEqual(A[4,1], 1.0/2.0, 9)
        self.assertAlmostEqual(A[4,2], 1.0, 9)
        self.assertAlmostEqual(A[4,3], -1.0/2.0, 9)
        self.assertAlmostEqual(A[4,4], -1.0, 9)
        
        return    
    
    def testBPrimeMatrix1(self):
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
        
        e1 = ElementAwarePslg.Element(x1, x2, x4, 1, 0)
        e2 = ElementAwarePslg.Element(x1, x2, x5, 2, 1)
        e3 = ElementAwarePslg.Element(x4, x2, x3, 3, 2)
        e4 = ElementAwarePslg.Element(x3, x2, x5, 4, 3)
        
        pslg.points.extend([x1, x2, x3, x4, x5])
        pslg.segments.extend([s1, s2, s3, s4, s5, s6, s7, s8])
        pslg.elements.extend([e1, e2, e3, e4])
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
              
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
                    
        #Get the matrices
        (G, A, BPrime) = Assembler.precomputeMatrices(shapeFunctions, parameters)
               
        #Test symetry
        for i in range(0, len(pslg.points)):
            for j in range(0, len(pslg.points)):
                self.assertAlmostEqual(BPrime[i,j], BPrime[j,i], 9)
               
        self.assertAlmostEqual(BPrime[0,0], -2.0 * math.sqrt(2.0)/3.0, 9)
        self.assertAlmostEqual(BPrime[0,1], 0, 9)
        self.assertAlmostEqual(BPrime[0,2], 0, 9)
        self.assertAlmostEqual(BPrime[0,3], 0, 9)
        self.assertAlmostEqual(BPrime[0,4], -math.sqrt(2.0)/3.0, 9)
        
        self.assertAlmostEqual(BPrime[1,0], 0, 9)
        self.assertAlmostEqual(BPrime[1,1], 0, 9)
        self.assertAlmostEqual(BPrime[1,2], 0, 9)
        self.assertAlmostEqual(BPrime[1,3], 0, 9)
        self.assertAlmostEqual(BPrime[1,4], 0, 9)
        
        self.assertAlmostEqual(BPrime[2,0], 0, 9)
        self.assertAlmostEqual(BPrime[2,1], 0, 9)
        self.assertAlmostEqual(BPrime[2,2], -2.0 * math.sqrt(2.0) / 3.0, 9)
        self.assertAlmostEqual(BPrime[2,3], 0, 9)
        self.assertAlmostEqual(BPrime[2,4], -math.sqrt(2.0) / 3.0, 9)
        
        self.assertAlmostEqual(BPrime[3,0], 0, 9)
        self.assertAlmostEqual(BPrime[3,1], 0, 9)
        self.assertAlmostEqual(BPrime[3,2], 0, 9)
        self.assertAlmostEqual(BPrime[3,3], 0, 9)
        self.assertAlmostEqual(BPrime[3,4], 0, 9)
        
        self.assertAlmostEqual(BPrime[4,0], -math.sqrt(2.0) / 3.0, 9)
        self.assertAlmostEqual(BPrime[4,1], 0, 9)
        self.assertAlmostEqual(BPrime[4,2], -math.sqrt(2.0) / 3.0, 9)
        self.assertAlmostEqual(BPrime[4,3], 0, 9)
        self.assertAlmostEqual(BPrime[4,4], -4.0 * math.sqrt(2.0) / 3.0, 9)
        
        return    
    
    def testBPrimeMatrix2(self):
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
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
              
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
        
        #Get the matrices
        (G, A, BPrime) = Assembler.precomputeMatrices(shapeFunctions, parameters)
        
        #Test symetry
        for i in range(0, len(pslg.points)):
            for j in range(0, len(pslg.points)):
                self.assertAlmostEqual(BPrime[i,j], BPrime[j,i], 9)    
        
        #Test values
        self.assertAlmostEqual(BPrime[0,0], -2.0 * math.sqrt(2.0) / 3.0, 9)
        self.assertAlmostEqual(BPrime[0,1], 0.0, 9)
        self.assertAlmostEqual(BPrime[0,2], 0.0, 9)
        self.assertAlmostEqual(BPrime[0,3], -math.sqrt(2.0) / 3.0, 9)
        self.assertAlmostEqual(BPrime[0,4], 0.0, 9)
        
        self.assertAlmostEqual(BPrime[1,0], 0.0, 9)
        self.assertAlmostEqual(BPrime[1,1], 0.0, 9)
        self.assertAlmostEqual(BPrime[1,2], 0.0, 9)
        self.assertAlmostEqual(BPrime[1,3], 0.0, 9)
        self.assertAlmostEqual(BPrime[1,4], 0.0, 9)
        
        self.assertAlmostEqual(BPrime[2,0], 0.0, 9)
        self.assertAlmostEqual(BPrime[2,1], 0.0, 9)
        self.assertAlmostEqual(BPrime[2,2], 0.0, 9)
        self.assertAlmostEqual(BPrime[2,3], 0.0, 9)
        self.assertAlmostEqual(BPrime[2,4], 0.0, 9)
        
        self.assertAlmostEqual(BPrime[3,0], -math.sqrt(2.0) / 3.0, 9)
        self.assertAlmostEqual(BPrime[3,1], 0.0, 9)
        self.assertAlmostEqual(BPrime[3,2], 0.0, 9)
        self.assertAlmostEqual(BPrime[3,3], -4.0 * math.sqrt(2.0) / 3.0, 9)
        self.assertAlmostEqual(BPrime[3,4], -math.sqrt(2.0) / 3.0, 9)
        
        self.assertAlmostEqual(BPrime[4,0], 0.0, 9)
        self.assertAlmostEqual(BPrime[4,1], 0.0, 9)
        self.assertAlmostEqual(BPrime[4,2], 0.0, 9)
        self.assertAlmostEqual(BPrime[4,3], -math.sqrt(2.0) / 3.0, 9)
        self.assertAlmostEqual(BPrime[4,4], -2.0 * math.sqrt(2.0) / 3.0, 9)
        
        return    
            
    def testComputeProductionVector1(self):
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
        
        #Create the coefficient vector
        z = numpy.matrix([1, 1, -1, 100, 1]).transpose()
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
              
        #Tweak the parameters
        parameters.productionEffciency = lambda x,y: 1.0
        parameters.productionThreshold = 1.0        
              
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
                    
        #Get the matrices
        P = Assembler.computeProductionVector(z, shapeFunctions, parameters)
               
        #Test symetry                      
        self.assertAlmostEqual(P[0,0], 0, 9)
        self.assertAlmostEqual(P[1,0], 1.0/3.0, 9)
        self.assertAlmostEqual(P[2,0], 2.0/3.0, 9)
        self.assertAlmostEqual(P[3,0], 0, 9)
        self.assertAlmostEqual(P[4,0], 1.0/3.0, 9)
        
        return

    def testComputeProductionVector2(self):
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
        z = numpy.matrix([0, 0, 0, 0, 0]).transpose()
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
              
        #Tweak the parameters
        parameters.productionEffciency = lambda x,y: 1.0
        parameters.productionThreshold = 1.0
                      
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
        
        #Get the matrices
        P = Assembler.computeProductionVector(z, shapeFunctions, parameters)
        
        #Test values
        expected = numpy.matrix([2.0/3.0, 4.0/3.0, 4.0/3.0, 0, 2.0/3.0]).transpose()
        self.assertTrue((abs(P - expected) < 1E-10).all())
        
        return

    def testComputeProductionVector3(self):
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
        z = numpy.matrix([1.0/11.0, 15.0/44.0, 1.0/8.0, -1.0/11.0, 7.0/44.0]).transpose()
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
              
        #Tweak the parameters
        parameters.productionEffciency = lambda x,y: 1.0
        parameters.productionThreshold = 1.0
                      
        #Get shape functions
        shapeFunctions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
        
        #Get the matrices
        P = Assembler.computeProductionVector(z, shapeFunctions, parameters)
        
        #Test values
        expected = numpy.matrix([295.0/528.0, 45.0/44.0, 289.0/264.0, 0, 283.0/528.0]).transpose()
        self.assertTrue((abs(P - expected) < 1E-10).all())
        
        return
        
if __name__ == '__main__':
    unittest.main()