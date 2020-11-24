'''
Created by: Shiyao Wang
Time: Nov 11, 2020
Purpose: To test the class Piece
'''


from piece import Piece
import unittest


class PieceTest(unittest.TestCase):


    def test_init(self):
        piece = Piece(player = 0, colors = ['black', 'red'])
        self.assertEqual(piece.player, 0)
        self.assertFalse(piece.is_king)
        self.assertEqual(piece.color, 'black')
        self.assertEqual(piece.radius, -1)
        self.assertEqual(piece.crown_size, -1)
        self.assertEqual(piece.crown_color, 'gold')


    def test_str(self):
        piece = Piece(player = 0)
        self.assertEqual(piece.__str__(), 'player: 0, which is non-king.')
        piece.is_king = True
        self.assertEqual(piece.__str__(), 'player: 0, which is king.')


    def test_eq(self):
        piece1 = Piece(player = 0)
        piece2 = Piece(player = 0)
        piece3 = Piece(player = 1)
        self.assertEqual(piece1, piece2)
        self.assertFalse(piece1 == piece3)


    def test_crown(self):
        piece = Piece(player = 0)
        self.assertFalse(piece.is_king)
        piece.crown()
        self.assertTrue(piece.is_king)


def main():
    unittest.main()

    
main()
