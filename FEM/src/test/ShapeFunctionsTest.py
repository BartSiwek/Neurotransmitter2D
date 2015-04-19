import unittest
import Pslg, ElementAwarePslg
import ShapeFunctions

class ShapeFunctionsTest(unittest.TestCase):
    def testSlopeFunction1(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        
        slope = ShapeFunctions.SlopeFunction(p1, p2, p3)
        
        result = slope.evaluate(0, 0)
        expected = 1
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(1, 0)
        expected = 0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(0, 1)
        expected = 0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(0.5, 0.5)
        expected = 0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(0.5, 0)
        expected = 0.5
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(0, 0.5)
        expected = 0.5
        self.assertAlmostEqual(result, expected, 9)

        result = slope.evaluate(0.25, 0.25)
        expected = 0.5
        self.assertAlmostEqual(result, expected, 9)

    def testSlopeFunction2(self):
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(5,6)
        
        slope = ShapeFunctions.SlopeFunction(p1, p2, p3)
        
        result = slope.evaluate(2, 2)
        expected = 1
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(5, 4)
        expected = 0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(5, 6)
        expected = 0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(5, 5)
        expected = 0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(3.5, 3)
        expected = 0.5
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluate(3.5, 4)
        expected = 0.5
        self.assertAlmostEqual(result, expected, 9)

        result = slope.evaluate(3.5, 3.5)
        expected = 0.5
        self.assertAlmostEqual(result, expected, 9)

    def testSlopeFunction3(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(0,1)
        p3 = Pslg.GridPoint(1,0)
        
        slope = ShapeFunctions.SlopeFunction(p1, p2, p3)
        
        result = slope.evaluateXDerivate(None, None)
        expected = -1.0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluateYDerivate(None, None)
        expected = -1.0
        self.assertAlmostEqual(result, expected, 9)

    def testSlopeFunction4(self):
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(4,5)
        p3 = Pslg.GridPoint(6,5)
        
        slope = ShapeFunctions.SlopeFunction(p1, p2, p3)
        
        result = slope.evaluateXDerivate(None, None)
        expected = 0.0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluateYDerivate(None, None)
        expected = -1.0 / 3.0
        self.assertAlmostEqual(result, expected, 9)
        
    def testSlopeFunction5(self):
        #Sub test 1
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(4,3)
        p3 = Pslg.GridPoint(3,4)

        slope = ShapeFunctions.SlopeFunction(p1, p2, p3)
        
        result = slope.evaluateXDerivate(None, None)
        expected = -1.0 / 3.0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluateYDerivate(None, None)
        expected = -1.0 / 3.0
        self.assertAlmostEqual(result, expected, 9)
        
        #Sub test 2
        p2, p3 = p3, p2
        slope = ShapeFunctions.SlopeFunction(p1, p2, p3)
        
        result = slope.evaluateXDerivate(None, None)
        expected = -1.0 / 3.0
        self.assertAlmostEqual(result, expected, 9)
        
        result = slope.evaluateYDerivate(None, None)
        expected = -1.0 / 3.0
        self.assertAlmostEqual(result, expected, 9)    

    def testGetDerivates(self):
        #Sub test 1
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(4,3)
        p3 = Pslg.GridPoint(3,4)

        slope = ShapeFunctions.SlopeFunction(p1, p2, p3)
        functions = slope.getDerivates()
        
        self.assertEqual(len(functions), 2)
        self.assertEqual(functions[0], slope.evaluateXDerivate)
        self.assertEqual(functions[1], slope.evaluateYDerivate)
        
    def testBuildShapeFunctionsForPslg(self):
        fake1 = Pslg.GridPoint(-1, -1)
        fake2 = Pslg.GridPoint(1, -1)
        pslg = ElementAwarePslg.ElementAwarePslg()
        
        for x in range(0,10):
            pslg.points.append(Pslg.GridPoint(x, 1))
            pslg.elements.append(ElementAwarePslg.Element(pslg.points[x], fake1, fake2, 0, x))
            
        functions = ShapeFunctions.buildShapeFunctionsForPslg(pslg)
        
        for x in range(0,10):
            s1 = functions[x][0]
            s2 = functions[x][1]
            s3 = functions[x][2]
            self.assertAlmostEquals(s1.evaluate(x, 1), 1, 9)
            self.assertAlmostEquals(s1.evaluate(fake1.x, fake1.y), 0, 9)
            self.assertAlmostEquals(s1.evaluate(fake2.x, fake2.y), 0, 9)
            self.assertAlmostEquals(s2.evaluate(x, 1), 0, 9)
            self.assertAlmostEquals(s2.evaluate(fake1.x, fake1.y), 1, 9)
            self.assertAlmostEquals(s2.evaluate(fake2.x, fake2.y), 0, 9)
            self.assertAlmostEquals(s3.evaluate(x, 1), 0, 9)
            self.assertAlmostEquals(s3.evaluate(fake1.x, fake1.y), 0, 9)
            self.assertAlmostEquals(s3.evaluate(fake2.x, fake2.y), 1, 9)
            
if __name__ == '__main__':
    unittest.main()