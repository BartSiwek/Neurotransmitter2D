import math, unittest
import Pslg, ElementAwarePslg

class ElementAwarePslgTest(unittest.TestCase):
    def testAreaComputation1(self):       
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
                
        result = e.getArea()
        self.assertAlmostEqual(result, 0.5, 9)

    def testAreaComputation2(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(3,0)
        p3 = Pslg.GridPoint(0,4)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
               
        result = e.getArea()
        self.assertAlmostEqual(result, 6.0, 9)

    def testAreaComputation3(self):        
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0.5, math.sqrt(3)/2.0)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
                
        result = e.getArea()
        self.assertAlmostEqual(result, math.sqrt(3)/4.0, 9)

    def testAreaComputation4(self):        
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(5,6)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
                
        result = e.getArea()
        self.assertAlmostEqual(result, 3, 9)

    def testIsSideOf1(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(0,1)
        p3 = Pslg.GridPoint(1,0)
        
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        s1 = Pslg.Segment(p1, p2)
        s2 = Pslg.Segment(p2, p3)
        s3 = Pslg.Segment(p3, p1)
        
        self.assertTrue(e.isSideOf(s1))
        self.assertTrue(e.isSideOf(s2))
        self.assertTrue(e.isSideOf(s3))
        
        s1 = Pslg.Segment(p2, p1)
        s2 = Pslg.Segment(p3, p2)
        s3 = Pslg.Segment(p1, p3)
        
        self.assertTrue(e.isSideOf(s1))
        self.assertTrue(e.isSideOf(s2))
        self.assertTrue(e.isSideOf(s3))

    def testIsSideOf2(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(0,1)
        p3 = Pslg.GridPoint(1,0)
        
        q1 = Pslg.GridPoint(1,1)
        q2 = Pslg.GridPoint(-1,-1)
        
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        s1 = Pslg.Segment(q1, q2)
        
        self.assertFalse(e.isSideOf(s1))
        
        s1 = Pslg.Segment(p1, q1)
        s2 = Pslg.Segment(p2, q1)
        s3 = Pslg.Segment(p3, q1)
        
        self.assertFalse(e.isSideOf(s1))
        self.assertFalse(e.isSideOf(s2))
        self.assertFalse(e.isSideOf(s3))
        
        s1 = Pslg.Segment(q2, p1)
        s2 = Pslg.Segment(q2, p2)
        s3 = Pslg.Segment(q2, p3)
        
        self.assertFalse(e.isSideOf(s1))
        self.assertFalse(e.isSideOf(s2))
        self.assertFalse(e.isSideOf(s3))

    def testSegmentLength(self):
        p1 = Pslg.Point(1.0, 2.0)
        p2 = Pslg.Point(-2.0, 1.0)
        s = Pslg.Segment(p1, p2)
        
        length = s.getLength()
        expected = 3.1622776601
        self.assertAlmostEqual(length, expected)

if __name__ == '__main__':
    unittest.main()