import unittest
import Pslg, ElementAwarePslg
import Program

class AssemblerTest(unittest.TestCase):
    def testCheckPointInElement(self):
        #Arrange
        x1 = Pslg.GridPoint(0,0)
        x2 = Pslg.GridPoint(2,0)
        x3 = Pslg.GridPoint(1,1)
        e = ElementAwarePslg.Element(x1, x2, x3, 0)
        program = Program.FemResultsViewer(None, None)
        
        #Act & Assert
        self.assertTrue(program.CheckPointInElement(e, 0, 0))
        self.assertTrue(program.CheckPointInElement(e, 2, 0))
        self.assertTrue(program.CheckPointInElement(e, 1, 1))
        self.assertTrue(program.CheckPointInElement(e, 1, 0))
        self.assertTrue(program.CheckPointInElement(e, 1.5, 0.5))
        self.assertTrue(program.CheckPointInElement(e, 0.5, 0.5))
        self.assertTrue(program.CheckPointInElement(e, 1, 0.5))
    
    def testFindCoeffInTime(self):
        #Arrange
        program = Program.FemResultsViewer(None, None)
        program.results = [(0.25, [0.1, 0.1, 0.1]),
                           (0.5, [0.2, 0.2, 0.2]),
                           (0.75, [0.3, 0.3, 0.3]),
                           ]
        
        #Act & Assert
        coeff = program.FindCoeffInTime(0.0)
        self.assertEqual(coeff, None)
        
        coeff = program.FindCoeffInTime(0.25)
        self.assertEqual(coeff[0], 0.1)
        self.assertEqual(coeff[1], 0.1)
        self.assertEqual(coeff[2], 0.1)
        
        coeff = program.FindCoeffInTime(0.5)
        self.assertEqual(coeff[0], 0.2)
        self.assertEqual(coeff[1], 0.2)
        self.assertEqual(coeff[2], 0.2)
        
        coeff = program.FindCoeffInTime(0.75)
        self.assertEqual(coeff[0], 0.3)
        self.assertEqual(coeff[1], 0.3)
        self.assertEqual(coeff[2], 0.3)
        
        coeff = program.FindCoeffInTime(1.0)
        self.assertEqual(coeff, None)
        
        coeff = program.FindCoeffInTime(0.3)
        left = (4.0/5.0)
        right = (1.0/5.0)
        self.assertAlmostEquals(coeff[0], left * 0.1 + right * 0.2, 9)
        self.assertAlmostEquals(coeff[1], left * 0.1 + right * 0.2, 9)
        self.assertAlmostEquals(coeff[2], left * 0.1 + right * 0.2, 9)
        
        coeff = program.FindCoeffInTime(0.35)
        left = (3.0/5.0)
        right = (2.0/5.0)
        self.assertAlmostEquals(coeff[0], left * 0.1 + right * 0.2, 9)
        self.assertAlmostEquals(coeff[1], left * 0.1 + right * 0.2, 9)
        self.assertAlmostEquals(coeff[2], left * 0.1 + right * 0.2, 9)
        
        coeff = program.FindCoeffInTime(0.4)
        left = (2.0/5.0)
        right = (3.0/5.0)
        self.assertAlmostEquals(coeff[0], left * 0.1 + right * 0.2, 9)
        self.assertAlmostEquals(coeff[1], left * 0.1 + right * 0.2, 9)
        self.assertAlmostEquals(coeff[2], left * 0.1 + right * 0.2, 9)
        
        coeff = program.FindCoeffInTime(0.45)
        left = (1.0/5.0)
        right = (4.0/5.0)
        self.assertAlmostEquals(coeff[0], left * 0.1 + right * 0.2, 9)
        self.assertAlmostEquals(coeff[1], left * 0.1 + right * 0.2, 9)
        self.assertAlmostEquals(coeff[2], left * 0.1 + right * 0.2, 9)
        
        coeff = program.FindCoeffInTime(0.55)
        left = (4.0/5.0)
        right = (1.0/5.0)
        self.assertAlmostEquals(coeff[0], left * 0.2 + right * 0.3, 9)
        self.assertAlmostEquals(coeff[1], left * 0.2 + right * 0.3, 9)
        self.assertAlmostEquals(coeff[2], left * 0.2 + right * 0.3, 9)        
        
        coeff = program.FindCoeffInTime(0.6)
        left = (3.0/5.0)
        right = (2.0/5.0)
        self.assertAlmostEquals(coeff[0], left * 0.2 + right * 0.3, 9)
        self.assertAlmostEquals(coeff[1], left * 0.2 + right * 0.3, 9)
        self.assertAlmostEquals(coeff[2], left * 0.2 + right * 0.3, 9)
        
        coeff = program.FindCoeffInTime(0.65)
        left = (2.0/5.0)
        right = (3.0/5.0)
        self.assertAlmostEquals(coeff[0], left * 0.2 + right * 0.3, 9)
        self.assertAlmostEquals(coeff[1], left * 0.2 + right * 0.3, 9)
        self.assertAlmostEquals(coeff[2], left * 0.2 + right * 0.3, 9)
        
        coeff = program.FindCoeffInTime(0.7)
        left = (1.0/5.0)
        right = (4.0/5.0)
        self.assertAlmostEquals(coeff[0], left * 0.2 + right * 0.3, 9)
        self.assertAlmostEquals(coeff[1], left * 0.2 + right * 0.3, 9)
        self.assertAlmostEquals(coeff[2], left * 0.2 + right * 0.3, 9)

if __name__ == '__main__':
    unittest.main()