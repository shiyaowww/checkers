'''
Created by: Shiyao Wang
Time: Nov 12, 2020
Purpose: To test the class coordinate
'''

from coordinate import Coordinate
import unittest


class CoordTest(unittest.TestCase):


    def test_init(self):
        coord = Coordinate(1, 2)
        self.assertEqual(coord.x, 1)
        self.assertEqual(coord.y, 2)


    def test_str(self):
        coord = Coordinate(1, 2)
        self.assertEqual(coord.__str__(), 'x: 1 y: 2')

    
    def test_eq(self):
        coord1 = Coordinate(1, 2)
        coord2 = Coordinate(1, 2)
        coord3 = Coordinate(1, 1)
        self.assertEqual(coord1, coord2)
        self.assertFalse(coord1 == coord3)


    def test_increment_x(self):
        coord = Coordinate(1, 2)
        self.assertEqual(coord.x, 1)
        coord.increment_x()
        self.assertEqual(coord.x, 2)


    def test_increment_y(self):
        coord = Coordinate(1, 2)
        self.assertEqual(coord.y, 2)
        coord.increment_y()
        self.assertEqual(coord.y, 3)
    

    def test_add_x(self):
        coord = Coordinate(1, 2)
        self.assertEqual(coord.x, 1)
        coord.add_x(2)
        self.assertEqual(coord.x, 3)


    def test_add_y(self):
        coord = Coordinate(1, 2)
        self.assertEqual(coord.y, 2)
        coord.add_y(2)
        self.assertEqual(coord.y, 4)


    def test_add(self):
        coord1 = Coordinate(1, 2)
        coord2 = Coordinate(9, 8)
        coord1.add(coord2)
        self.assertEqual(coord1.x, 10)
        self.assertEqual(coord1.y, 10)
    

def main():
    unittest.main()


main()