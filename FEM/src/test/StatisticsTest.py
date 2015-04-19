import unittest, math
import Pslg, ElementAwarePslg
import Statistics

class ParametersTest(unittest.TestCase):
    def testComputeElementAngleRange(self):
        #Angle of zero
        a = Pslg.GridPoint(0,0)
        b = Pslg.GridPoint(1,0)
        c = Pslg.GridPoint(1,0)
        
        angle = Statistics.ComputeAngleBetweenPoints(a, b, c)
        
        expected = 0.0 * math.pi
        self.assertAlmostEquals(angle, expected, 9)
        
        #Angle of 45 degrees
        a = Pslg.GridPoint(0,0)
        b = Pslg.GridPoint(1,1)
        c = Pslg.GridPoint(1,0)
        
        angle = Statistics.ComputeAngleBetweenPoints(a, b, c)

        expected = 0.25 * math.pi        
        self.assertAlmostEquals(angle, expected, 9)
        
        #Angle of 45 degrees
        a = Pslg.GridPoint(0,0)
        b = Pslg.GridPoint(1,-1)
        c = Pslg.GridPoint(1,0)
        
        angle = Statistics.ComputeAngleBetweenPoints(a, b, c)

        expected = 0.25 * math.pi        
        self.assertAlmostEquals(angle, expected, 9)        
        
        #Angle of 90 degrees
        a = Pslg.GridPoint(0,0)
        b = Pslg.GridPoint(0,1)
        c = Pslg.GridPoint(1,0)
        
        angle = Statistics.ComputeAngleBetweenPoints(a, b, c)

        expected = 0.5 * math.pi        
        self.assertAlmostEquals(angle, expected, 9)
    
        #Angle of 90 degrees
        a = Pslg.GridPoint(0,0)
        b = Pslg.GridPoint(0,-1)
        c = Pslg.GridPoint(1,0)
        
        angle = Statistics.ComputeAngleBetweenPoints(a, b, c)

        expected = 0.5 * math.pi        
        self.assertAlmostEquals(angle, expected, 9)        

        #Angle of 135 degrees
        a = Pslg.GridPoint(0,0)
        b = Pslg.GridPoint(-1,1)
        c = Pslg.GridPoint(1,0)
        
        angle = Statistics.ComputeAngleBetweenPoints(a, b, c)

        expected = 0.75 * math.pi        
        self.assertAlmostEquals(angle, expected, 9)
    
        #Angle of 135 degrees
        a = Pslg.GridPoint(0,0)
        b = Pslg.GridPoint(-1,-1)
        c = Pslg.GridPoint(1,0)
        
        angle = Statistics.ComputeAngleBetweenPoints(a, b, c)

        expected = 0.75 * math.pi        
        self.assertAlmostEquals(angle, expected, 9)
        
        #Angle of 180 degrees
        a = Pslg.GridPoint(0,0)
        b = Pslg.GridPoint(-1,0)
        c = Pslg.GridPoint(1,0)
        
        angle = Statistics.ComputeAngleBetweenPoints(a, b, c)

        expected = 1.0 * math.pi        
        self.assertAlmostEquals(angle, expected, 9)        
    
if __name__ == '__main__':
    unittest.main()
