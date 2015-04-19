import unittest
import GaussPointFactory

class GaussPointFactoryTest(unittest.TestCase):
    def testGaussPoints2D(self):
        points = GaussPointFactory.getGaussPoints2D()

        sum = 0
        for point in points:
            sum += point[0]
            self.assertTrue(0 <= point[1] and point[1] <= 1)
            self.assertTrue(0 <= point[2] and point[2] <= 1)
        self.assertAlmostEqual(sum, 1.0, 9)

    def testGaussPoints1D(self):
        points = GaussPointFactory.getGaussPoints1D()
        expected = [(0.5555555555555556, -0.7745966692414834),
                    (0.8888888888888889,  0.0),
                    (0.5555555555555556,  0.7745966692414834)]
        
        self.assertEqual(len(points), len(expected), "Invalid number of Gauss points")
        for i in range(0,len(points)):
            for j in range(0,2):
                self.assertAlmostEqual(points[i][j], expected[i][j], 9, "Invalid Gauss point")
        
if __name__ == '__main__':
    unittest.main()
                          