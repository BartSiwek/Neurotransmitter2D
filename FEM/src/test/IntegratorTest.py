import unittest
import Integrator, Pslg, ElementAwarePslg, math

class IntegratorTest(unittest.TestCase):
    def testConstantFunction1(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 1
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 0.5, 9)
    
    def testConstantFunction2(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 4
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 2.0, 9)

    def testFirstDegreePolynomial1(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return x
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 1.0/6.0, 9)
        
    def testFirstDegreePolynomial2(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 4.0 * x
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 4.0/6.0, 9)        
        
    def testFirstDegreePolynomial3(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return y
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 1.0/6.0, 9)    

    def testFirstDegreePolynomial4(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 4.0 * y
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 4.0/6.0, 9)

    def testFirstDegreePolynomial5(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 2.0 * x + 3.0 * y + 4.0
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 2.0/6.0 + 3.0 / 6.0 + 2.0, 9)
        
    def testSecondDegreePolynomial1(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return x * x
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 1.0/12.0, 9)

    def testSecondDegreePolynomial2(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 3.0 * x * x
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 3.0/12.0, 9)

    def testSecondDegreePolynomial3(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return x * y
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 1.0/24.0, 9)
        
    def testSecondDegreePolynomial4(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 3.0 * x * y
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 3.0/24.0, 9)

    def testSecondDegreePolynomial5(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return y * y
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 1.0/12.0, 9)
        
    def testSecondDegreePolynomial6(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 3.0 * y * y
        
        result = Integrator.integrate2D(f, e)
        self.assertAlmostEqual(result, 3.0/12.0, 9)        
        
    def testSecondDegreePolynomial7(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 2.0 * x * x + 3.0 * x * y + 4.0 * y * y + 5.0 * x + 6.0 * y + 7.0
        
        result = Integrator.integrate2D(f, e)
        expected = 5.9583333333333339
        self.assertAlmostEqual(result, expected, 9)        
        
    def testTransformOrigin1(self):
        p1 = Pslg.GridPoint(0,0)
        p2 = Pslg.GridPoint(1,0)
        p3 = Pslg.GridPoint(0,1)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        values = Integrator.transformOrigin(e, 0, 0)
        self.assertAlmostEqual(values[0], 0)
        self.assertAlmostEqual(values[1], 0)
        
        values = Integrator.transformOrigin(e, 1, 0)
        self.assertAlmostEqual(values[0], 1)
        self.assertAlmostEqual(values[1], 0)
        
        values = Integrator.transformOrigin(e, 0, 1)
        self.assertAlmostEqual(values[0], 0)
        self.assertAlmostEqual(values[1], 1)
        
        values = Integrator.transformOrigin(e, 0.5, 0)
        self.assertAlmostEqual(values[0], 0.5)
        self.assertAlmostEqual(values[1], 0)
        
        values = Integrator.transformOrigin(e, 0, 0.5)
        self.assertAlmostEqual(values[0], 0)
        self.assertAlmostEqual(values[1], 0.5)
        
        values = Integrator.transformOrigin(e, 0.5, 0.5)
        self.assertAlmostEqual(values[0], 0.5)
        self.assertAlmostEqual(values[1], 0.5)
        
        values = Integrator.transformOrigin(e, 0.25, 0.5)
        self.assertAlmostEqual(values[0], 0.25)
        self.assertAlmostEqual(values[1], 0.5)

    def testTransformOrigin2(self):
        p1 = Pslg.GridPoint(3,4)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(3,4.5)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        values = Integrator.transformOrigin(e, 0, 0)
        self.assertAlmostEqual(values[0], 3)
        self.assertAlmostEqual(values[1], 4)
        
        values = Integrator.transformOrigin(e, 1, 0)
        self.assertAlmostEqual(values[0], 5)
        self.assertAlmostEqual(values[1], 4)
        
        values = Integrator.transformOrigin(e, 0, 1)
        self.assertAlmostEqual(values[0], 3)
        self.assertAlmostEqual(values[1], 4.5)
        
        values = Integrator.transformOrigin(e, 0.5, 0)
        self.assertAlmostEqual(values[0], 4)
        self.assertAlmostEqual(values[1], 4)
        
        values = Integrator.transformOrigin(e, 0, 0.5)
        self.assertAlmostEqual(values[0], 3)
        self.assertAlmostEqual(values[1], 4.25)
        
        values = Integrator.transformOrigin(e, 0.5, 0.5)
        self.assertAlmostEqual(values[0], 4)
        self.assertAlmostEqual(values[1], 4.25)
        
        values = Integrator.transformOrigin(e, 0.25, 0.5)
        self.assertAlmostEqual(values[0], 3.5)
        self.assertAlmostEqual(values[1], 4.25)

    def testTransformOrigin3(self):
        p1 = Pslg.GridPoint(4,4)
        p2 = Pslg.GridPoint(7,5)
        p3 = Pslg.GridPoint(5,7)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        values = Integrator.transformOrigin(e, 0, 0)
        self.assertAlmostEqual(values[0], 4)
        self.assertAlmostEqual(values[1], 4)
        
        values = Integrator.transformOrigin(e, 1, 0)
        self.assertAlmostEqual(values[0], 7)
        self.assertAlmostEqual(values[1], 5)
        
        values = Integrator.transformOrigin(e, 0, 1)
        self.assertAlmostEqual(values[0], 5)
        self.assertAlmostEqual(values[1], 7)
        
        values = Integrator.transformOrigin(e, 0.5, 0)
        self.assertAlmostEqual(values[0], 5.5)
        self.assertAlmostEqual(values[1], 4.5)
        
        values = Integrator.transformOrigin(e, 0, 0.5)
        self.assertAlmostEqual(values[0], 4.5)
        self.assertAlmostEqual(values[1], 5.5)
        
        values = Integrator.transformOrigin(e, 0.5, 0.5)
        self.assertAlmostEqual(values[0], 6)
        self.assertAlmostEqual(values[1], 6)
        
        values = Integrator.transformOrigin(e, 0.25, 0.5)
        self.assertAlmostEqual(values[0], 4 + 5.0 / 4.0)
        self.assertAlmostEqual(values[1], 4 + 7.0 / 4.0)

    def testIntegration1(self):
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(5,6)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 2.0 * x * x
        
        result = Integrator.integrate2D(f, e)
        expected = 99
        self.assertAlmostEqual(result, expected, 9)

    def testIntegration2(self):
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(5,6)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 3.0 * x * y
        
        result = Integrator.integrate2D(f, e)
        expected = 148.5
        self.assertAlmostEqual(result, expected, 9)
   
    def testIntegration3(self):
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(5,6)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 4.0 * y * y
        
        result = Integrator.integrate2D(f, e)
        expected = 200
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration4(self):
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(5,6)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 5.0 * x
        
        result = Integrator.integrate2D(f, e)
        expected = 60
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration5(self):
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(5,6)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 6.0 * y
        
        result = Integrator.integrate2D(f, e)
        expected = 72
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration6(self):
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(5,6)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 7.0
        
        result = Integrator.integrate2D(f, e)
        expected = 21
        self.assertAlmostEqual(result, expected, 9)    
        
    def testIntegration7(self):
        p1 = Pslg.GridPoint(2,2)
        p2 = Pslg.GridPoint(5,4)
        p3 = Pslg.GridPoint(5,6)
        e = ElementAwarePslg.Element(p1, p2, p3, 0, 0)
        
        def f(x, y):
            return 2.0 * x * x + 3.0 * x * y + 4.0 * y * y + 5.0 * x + 6.0 * y + 7.0
        
        result = Integrator.integrate2D(f, e)
        expected = 600.5
        self.assertAlmostEqual(result, expected, 9)    
        
    def testTransformSegemntParameter1(self):
        p1 = Pslg.GridPoint(1,2)
        p2 = Pslg.GridPoint(3,-2)
        s = Pslg.Segment(p1, p2)
        
        result = Integrator.transformSegementParameter(s, -1)
        expected = [1,2]
        self.assertAlmostEquals(result[0], expected[0], 9)
        self.assertAlmostEquals(result[1], expected[1], 9)
        
        result = Integrator.transformSegementParameter(s, -0.5)
        expected = [1.5,1]
        self.assertAlmostEquals(result[0], expected[0], 9)
        self.assertAlmostEquals(result[1], expected[1], 9)
        
        result = Integrator.transformSegementParameter(s, 0)
        expected = [2,0]
        self.assertAlmostEquals(result[0], expected[0], 9)
        self.assertAlmostEquals(result[1], expected[1], 9)
        
        result = Integrator.transformSegementParameter(s, 0.5)
        expected = [2.5,-1]
        self.assertAlmostEquals(result[0], expected[0], 9)
        self.assertAlmostEquals(result[1], expected[1], 9)
        
        result = Integrator.transformSegementParameter(s, 1)
        expected = [3,-2]
        self.assertAlmostEquals(result[0], expected[0], 9)
        self.assertAlmostEquals(result[1], expected[1], 9)
        
    def testGetTransformationFactor1(self):
        p1 = Pslg.GridPoint(1,2)
        p2 = Pslg.GridPoint(3,-2)
        s = Pslg.Segment(p1, p2)
        
        result = Integrator.getTransformationFactor(s)
        expected = math.sqrt(5)
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration1D1(self):
        p1 = Pslg.GridPoint(1,2)
        p2 = Pslg.GridPoint(3,-2)
        s = Pslg.Segment(p1, p2)
        
        def f(x, y):
            return 2 * x * x
        
        result = Integrator.integrate1D(f, s)
        expected = 52 * math.sqrt(5) / 3.0
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration1D2(self):
        p1 = Pslg.GridPoint(1,2)
        p2 = Pslg.GridPoint(3,-2)
        s = Pslg.Segment(p1, p2)
        
        def f(x, y):
            return 3 * x * y
        
        result = Integrator.integrate1D(f, s)
        expected = -12 * math.sqrt(5) / 3.0
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration1D3(self):
        p1 = Pslg.GridPoint(1,2)
        p2 = Pslg.GridPoint(3,-2)
        s = Pslg.Segment(p1, p2)
        
        def f(x, y):
            return 4 * y * y
        
        result = Integrator.integrate1D(f, s)
        expected = 32 * math.sqrt(5) / 3.0
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration1D4(self):
        p1 = Pslg.GridPoint(1,2)
        p2 = Pslg.GridPoint(3,-2)
        s = Pslg.Segment(p1, p2)
        
        def f(x, y):
            return 5 * x
        
        result = Integrator.integrate1D(f, s)
        expected = 20 * math.sqrt(5)
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration1D5(self):
        p1 = Pslg.GridPoint(1,2)
        p2 = Pslg.GridPoint(3,-2)
        s = Pslg.Segment(p1, p2)
        
        def f(x, y):
            return 6 * y
        
        result = Integrator.integrate1D(f, s)
        expected = 0
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration1D6(self):
        p1 = Pslg.GridPoint(1,2)
        p2 = Pslg.GridPoint(3,-2)
        s = Pslg.Segment(p1, p2)
        
        def f(x, y):
            return 7.0
        
        result = Integrator.integrate1D(f, s)
        expected = 14 * math.sqrt(5)
        self.assertAlmostEqual(result, expected, 9)
        
    def testIntegration1D7(self):
        p1 = Pslg.GridPoint(1,2)
        p2 = Pslg.GridPoint(3,-2)
        s = Pslg.Segment(p1, p2)
        
        def f(x, y):
            return 2.0 * x * x + 3.0 * x * y + 4.0 * y * y + 5.0 * x + 6.0 * y + 7.0
        
        result = Integrator.integrate1D(f, s)
        expected = 58 * math.sqrt(5)
        self.assertAlmostEqual(result, expected, 9)
        
if __name__ == '__main__':
    unittest.main()
                          