import unittest
import Function

class FunctionHelperTest(unittest.TestCase):
    def testAddFunctions1(self):
        f = lambda x,y: 2
        g = lambda x,y: 2
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.FunctionWrapper(g, "g")
        hw = fw + gw
        self.assertAlmostEqual(hw(-1,-1), 4, 9)
        self.assertAlmostEqual(hw( 0,-1), 4, 9)
        self.assertAlmostEqual(hw( 1,-1), 4, 9)
        self.assertAlmostEqual(hw(-1, 0), 4, 9)
        self.assertAlmostEqual(hw( 0, 0), 4, 9)
        self.assertAlmostEqual(hw( 1, 0), 4, 9)
        self.assertAlmostEqual(hw(-1, 1), 4, 9)
        self.assertAlmostEqual(hw( 0, 1), 4, 9)
        self.assertAlmostEqual(hw( 1, 1), 4, 9)
        self.assertEqual(str(hw), "f + g")
        
    def testAddFunctions2(self):
        f = lambda x,y: 2 * x
        g = lambda x,y: 2 * y
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.FunctionWrapper(g, "g")
        hw = fw + gw
        self.assertAlmostEqual(hw(-1,-1), -4, 9)
        self.assertAlmostEqual(hw( 0,-1), -2, 9)
        self.assertAlmostEqual(hw( 1,-1),  0, 9)
        self.assertAlmostEqual(hw(-1, 0), -2, 9)
        self.assertAlmostEqual(hw( 0, 0),  0, 9)
        self.assertAlmostEqual(hw( 1, 0),  2, 9)
        self.assertAlmostEqual(hw(-1, 1),  0, 9)
        self.assertAlmostEqual(hw( 0, 1),  2, 9)
        self.assertAlmostEqual(hw( 1, 1),  4, 9)    
        self.assertEqual(str(hw), "f + g")
        
    def testAddFunctions3(self):
        f = lambda x,y: 2 * x * y
        g = lambda x,y: 2 * y * y
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.FunctionWrapper(g, "g")
        hw = fw + gw
        self.assertAlmostEqual(hw(-1,-1),  4, 9)
        self.assertAlmostEqual(hw( 0,-1),  2, 9)
        self.assertAlmostEqual(hw( 1,-1),  0, 9)
        self.assertAlmostEqual(hw(-1, 0),  0, 9)
        self.assertAlmostEqual(hw( 0, 0),  0, 9)
        self.assertAlmostEqual(hw( 1, 0),  0, 9)
        self.assertAlmostEqual(hw(-1, 1),  0, 9)
        self.assertAlmostEqual(hw( 0, 1),  2, 9)
        self.assertAlmostEqual(hw( 1, 1),  4, 9)    
        self.assertEqual(str(hw), "f + g")

    def testMultiplyFunctions1(self):
        f = lambda x,y: 2
        g = lambda x,y: 3
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.FunctionWrapper(g, "g")
        hw = fw * gw
        self.assertAlmostEqual(hw(-1,-1), 6, 9)
        self.assertAlmostEqual(hw( 0,-1), 6, 9)
        self.assertAlmostEqual(hw( 1,-1), 6, 9)
        self.assertAlmostEqual(hw(-1, 0), 6, 9)
        self.assertAlmostEqual(hw( 0, 0), 6, 9)
        self.assertAlmostEqual(hw( 1, 0), 6, 9)
        self.assertAlmostEqual(hw(-1, 1), 6, 9)
        self.assertAlmostEqual(hw( 0, 1), 6, 9)
        self.assertAlmostEqual(hw( 1, 1), 6, 9)
        self.assertEqual(str(hw), "(f) * (g)")
        
    def testMultiplyFunctions2(self):
        f = lambda x,y: 2 * x
        g = lambda x,y: 2 * y
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.FunctionWrapper(g, "g")
        hw = fw * gw
        self.assertAlmostEqual(hw(-1,-1),  4, 9)
        self.assertAlmostEqual(hw( 0,-1),  0, 9)
        self.assertAlmostEqual(hw( 1,-1), -4, 9)
        self.assertAlmostEqual(hw(-1, 0),  0, 9)
        self.assertAlmostEqual(hw( 0, 0),  0, 9)
        self.assertAlmostEqual(hw( 1, 0),  0, 9)
        self.assertAlmostEqual(hw(-1, 1), -4, 9)
        self.assertAlmostEqual(hw( 0, 1),  0, 9)
        self.assertAlmostEqual(hw( 1, 1),  4, 9)    
        self.assertEqual(str(hw), "(f) * (g)")
        
    def testMultiplyFunctions3(self):
        f = lambda x,y: 2 * x * y
        g = lambda x,y: 2 * y * y
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.FunctionWrapper(g, "g")
        hw = fw * gw
        self.assertAlmostEqual(hw(-1,-1),  4, 9)
        self.assertAlmostEqual(hw( 0,-1),  0, 9)
        self.assertAlmostEqual(hw( 1,-1), -4, 9)
        self.assertAlmostEqual(hw(-1, 0),  0, 9)
        self.assertAlmostEqual(hw( 0, 0),  0, 9)
        self.assertAlmostEqual(hw( 1, 0),  0, 9)
        self.assertAlmostEqual(hw(-1, 1), -4, 9)
        self.assertAlmostEqual(hw( 0, 1),  0, 9)
        self.assertAlmostEqual(hw( 1, 1),  4, 9) 
        self.assertEqual(str(hw), "(f) * (g)")
        
    def testSubstractFunctions1(self):
        f = lambda x,y: 2
        g = lambda x,y: 2
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.FunctionWrapper(g, "g")
        hw = fw - gw
        self.assertAlmostEqual(hw(-1,-1), 0, 9)
        self.assertAlmostEqual(hw( 0,-1), 0, 9)
        self.assertAlmostEqual(hw( 1,-1), 0, 9)
        self.assertAlmostEqual(hw(-1, 0), 0, 9)
        self.assertAlmostEqual(hw( 0, 0), 0, 9)
        self.assertAlmostEqual(hw( 1, 0), 0, 9)
        self.assertAlmostEqual(hw(-1, 1), 0, 9)
        self.assertAlmostEqual(hw( 0, 1), 0, 9)
        self.assertAlmostEqual(hw( 1, 1), 0, 9)
        self.assertEqual(str(hw), "(f) - (g)")
        
    def testSubstractFunctions2(self):
        f = lambda x,y: 2 * x
        g = lambda x,y: 2 * y
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.FunctionWrapper(g, "g")
        hw = fw - gw
        self.assertAlmostEqual(hw(-1,-1),  0, 9)
        self.assertAlmostEqual(hw( 0,-1),  2, 9)
        self.assertAlmostEqual(hw( 1,-1),  4, 9)
        self.assertAlmostEqual(hw(-1, 0), -2, 9)
        self.assertAlmostEqual(hw( 0, 0),  0, 9)
        self.assertAlmostEqual(hw( 1, 0),  2, 9)
        self.assertAlmostEqual(hw(-1, 1), -4, 9)
        self.assertAlmostEqual(hw( 0, 1), -2, 9)
        self.assertAlmostEqual(hw( 1, 1),  0, 9)    
        self.assertEqual(str(hw), "(f) - (g)")
        
    def testSubstractFunctions3(self):
        f = lambda x,y: 2 * x * y
        g = lambda x,y: 2 * y * y
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.FunctionWrapper(g, "g")
        hw = fw - gw
        self.assertAlmostEqual(hw(-1,-1),  0, 9)
        self.assertAlmostEqual(hw( 0,-1), -2, 9)
        self.assertAlmostEqual(hw( 1,-1), -4, 9)
        self.assertAlmostEqual(hw(-1, 0),  0, 9)
        self.assertAlmostEqual(hw( 0, 0),  0, 9)
        self.assertAlmostEqual(hw( 1, 0),  0, 9)
        self.assertAlmostEqual(hw(-1, 1), -4, 9)
        self.assertAlmostEqual(hw( 0, 1), -2, 9)
        self.assertAlmostEqual(hw( 1, 1),  0, 9)    
        self.assertEqual(str(hw), "(f) - (g)")
    
    def testBuildConstantFunction1(self):
        f = Function.ConstantFunction(1)
            
        self.assertAlmostEqual(f(-1,-1),  1, 9)
        self.assertAlmostEqual(f( 0, 0),  1, 9)
        self.assertAlmostEqual(f( 1, 2),  1, 9)
        self.assertEqual(str(f), "1.0")
        
    def testBuildConstantFunction2(self):
        f = Function.ConstantFunction(-2)
            
        self.assertAlmostEqual(f(-1,-1), -2, 9)
        self.assertAlmostEqual(f( 0, 0), -2, 9)
        self.assertAlmostEqual(f( 1, 2), -2, 9)
        self.assertEqual(str(f), "-2.0")
    
    def testBuildPositivePart1(self):
        f = lambda x,y: x - y
        fw = Function.FunctionWrapper(f, "f")
        gw = Function.PositivePartFunction(fw)
        
        self.assertAlmostEqual(gw(-1,-1),  0, 9)
        self.assertAlmostEqual(gw( 0,-1),  1, 9)
        self.assertAlmostEqual(gw( 1,-1),  2, 9)
        self.assertAlmostEqual(gw(-1, 0),  0, 9)
        self.assertAlmostEqual(gw( 0, 0),  0, 9)
        self.assertAlmostEqual(gw( 1, 0),  1, 9)
        self.assertAlmostEqual(gw(-1, 1),  0, 9)
        self.assertAlmostEqual(gw( 0, 1),  0, 9)
        self.assertAlmostEqual(gw( 1, 1),  0, 9)
        self.assertEqual(str(gw), "(f)^+")
        
if __name__ == '__main__':
    unittest.main()
                          