'''
Created by: Shiyao Wang
Time: Nov 11, 2020
Purpose: To test the class Cell
'''


from coordinate import Coordinate
from piece import Piece
from cell import Cell 
import unittest


class CellTest(unittest.TestCase):


    def test_init(self):
        cell = Cell(coord = Coordinate(6, 5))
        self.assertEqual(cell.bottom_left, Coordinate(0, 0))
        self.assertEqual(cell.occupied, 0)
        self.assertEqual(cell.edge, -1)
        self.assertEqual(cell.color, 'white')


    def test_str(self):
        cell = Cell(coord = Coordinate(6, 5))
        self.assertEqual(cell.__str__(), 'this cell x: 6 y: 5 contains piece: 0')
        cell.occupied = Piece(player = 0)
        self.assertEqual(cell.__str__(), 'this cell x: 6 y: 5 contains piece: player: 0, which is non-king.')
        cell.occupied.player = 1
        cell.occupied.is_king = True
        self.assertEqual(cell.__str__(), 'this cell x: 6 y: 5 contains piece: player: 1, which is king.')


    def test_eq(self):
        cell1 = Cell(coord = Coordinate(6, 5))
        cell2 = Cell(coord = Coordinate(6, 5))
        cell3 = Cell(coord = Coordinate(6, 6))
        self.assertEqual(cell1, cell2)
        self.assertFalse(cell1 == cell3)
        

    def test_is_click_in(self):
        cell = Cell(coord = Coordinate(6, 5), bottom_left = Coordinate(0, 0), edge = 100)
        self.assertEqual(cell.is_click_in(50, 60), True)
        self.assertEqual(cell.is_click_in(101, 60), False)


    def test_is_adjacent(self):
        cell1 = Cell(coord = Coordinate(6, 5))
        cell2 = Cell(coord = Coordinate(5, 4))
        cell3 = Cell(coord = Coordinate(4, 4))
        self.assertEqual(cell1.is_adjacent(cell2), True)
        self.assertEqual(cell1.is_adjacent(cell3), False)


    def test_all_adjacent(self):
        cell1 = Cell(coord = Coordinate(6, 5))
        cell2 = Cell(coord = Coordinate(5, 4))
        cell3 = Cell(coord = Coordinate(4, 4))
        cell4 = Cell(coord = Coordinate(7, 4))
        cell_list1 = [cell2, cell3, cell4]
        cell_list2 = [cell2, cell4]
        self.assertEqual(cell1.all_adjacent(cell_list1), False)
        self.assertEqual(cell1.all_adjacent(cell_list2), True)


    def test_cell_key(self):
        cell = Cell(coord = Coordinate(6, 5))
        self.assertEqual(cell.generate_cell_key(), (6, 5))


    def test_coords_to_search(self):
        cell1 = Cell(coord = Coordinate(6, 5))
        cell1.occupied = Piece(player = 0)
        cell2 = Cell(coord = Coordinate(3, 7))
        cell2.occupied = Piece(player = 1)
        self.assertEqual(cell1.get_coords_to_search(), [[5, 7],[6]])
        self.assertEqual(cell2.get_coords_to_search(), [[2, 4],[6]])


def main():
    unittest.main()


main()

