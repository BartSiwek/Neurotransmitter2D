import unittest
import Pslg, ElementAwarePslg
import Parameters

class ParametersTest(unittest.TestCase):
    def testInitialization1(self):
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
        
        s1 = Pslg.Segment(p1, p4)
        s2 = Pslg.Segment(p4, p3)
        s3 = Pslg.Segment(p3, p5)
        s4 = Pslg.Segment(p5, p1)
        s5 = Pslg.Segment(p1, p2)
        s6 = Pslg.Segment(p2, p4)
        s7 = Pslg.Segment(p5, p2)
        s8 = Pslg.Segment(p2, p3)
        
        e1 = ElementAwarePslg.Element(p4, p2, p1, Parameters.Parameters.omegaThreeIdentifier, 0)
        e2 = ElementAwarePslg.Element(p4, p2, p3, Parameters.Parameters.omegaThreeIdentifier, 1)
        e3 = ElementAwarePslg.Element(p2, p5, p3, 0, 2)
        e4 = ElementAwarePslg.Element(p1, p2, p5, 0, 3)
        
        pslg.points.extend([p1, p2, p3, p4, p5])
        pslg.segments.extend([s1, s2, s3, s4, s5, s6, s7, s8])
        pslg.elements.extend([e1, e2, e3, e4])
        
        #Assign boundary markers
        p1.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        p2.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        p5.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
        
        #Assert
        self.assertEqual(len(parameters.omegaD), 5)
        self.assertEqual(len(filter(lambda x: x == (s4, e4), parameters.omegaD)), 1)
        self.assertEqual(len(filter(lambda x: x == (s5, e1), parameters.omegaD)), 1)
        self.assertEqual(len(filter(lambda x: x == (s5, e4), parameters.omegaD)), 1)
        self.assertEqual(len(filter(lambda x: x == (s7, e3), parameters.omegaD)), 1)
        self.assertEqual(len(filter(lambda x: x == (s7, e4), parameters.omegaD)), 1)
            
    def testInitialization2(self):
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
        
        s1 = Pslg.Segment(p1, p4)
        s2 = Pslg.Segment(p4, p3)
        s3 = Pslg.Segment(p3, p5)
        s4 = Pslg.Segment(p5, p1)
        s5 = Pslg.Segment(p1, p2)
        s6 = Pslg.Segment(p2, p4)
        s7 = Pslg.Segment(p5, p2)
        s8 = Pslg.Segment(p2, p3)
        
        e1 = ElementAwarePslg.Element(p4, p2, p1, Parameters.Parameters.omegaThreeIdentifier, 0)
        e2 = ElementAwarePslg.Element(p4, p2, p3, Parameters.Parameters.omegaThreeIdentifier, 1)
        e3 = ElementAwarePslg.Element(p2, p5, p3, 0, 2)
        e4 = ElementAwarePslg.Element(p1, p2, p5, 0, 3)
        
        pslg.points.extend([p1, p2, p3, p4, p5])
        pslg.segments.extend([s1, s2, s3, s4, s5, s6, s7, s8])
        pslg.elements.extend([e1, e2, e3, e4])
        
        #Assign boundary markers
        p1.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        p3.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        p5.boundaryMarker = Parameters.Parameters.omegaDIdentifier
        
        #Create parameters
        parameters = Parameters.Parameters()
        parameters.initialize(pslg)
        
        #Assert
        self.assertEqual(len(parameters.omegaD), 2)
        self.assertEqual(len(filter(lambda x: x == (s4, e4), parameters.omegaD)), 1)
        self.assertEqual(len(filter(lambda x: x == (s3, e3), parameters.omegaD)), 1)    
            
if __name__ == '__main__':
    unittest.main()