'''
Created by: Shiyao Wang
Time: Nov 11, 2020
Purpose: To test the class state
'''

from coordinate import Coordinate
from piece import Piece
from cell import Cell 
from state import State
import unittest


class CellTest(unittest.TestCase):


    def test_init(self):
        state = State()
        self.assertEqual(state.num_cells, 8)
        self.assertEqual(state.cell_size, 50)
        self.assertEqual(state.piece_radius, 24)
        self.assertEqual(state.piece_colors, ('black', 'dark red'))
        self.assertEqual(state.cell_colors, ('light gray', 'white'))
        self.assertEqual(state.board_color, 'white')
        self.assertEqual(state.board_size, 400)
        self.assertEqual(state.window_size, 450)
        self.assertEqual(state.checkerboard, [[0 for i in range(state.num_cells)] for j in range(state.num_cells)])
        self.assertEqual(state.cell_focused.occupied, 0)
        self.assertEqual(state.cell_focused.coord, Coordinate())
        self.assertEqual(state.valid_moves, {})
        self.assertEqual(state.turn, 0)
        self.assertEqual(state.piece_or_cell, 0)
        self.assertEqual(state.is_capture, 0)
        self.assertEqual(state.move_count, 1)


    def test_render_board(self):
        state = State()
        state.render_board()
        self.assertEqual(state.checkerboard[0][1].coord.x, 0)
        self.assertEqual(state.checkerboard[0][1].coord.y, 1)


    def test_init_pieces(self):
        state = State()
        state.render_board()
        state.init_pieces()
        piece_set = True
        for col in range(8):
            for row in range(8):
                if col % 2 != row % 2:
                    if row < state.num_cells / 2 - 1:
                        piece_set *= state.checkerboard[col][row].occupied.player == 0
                    elif row > state.num_cells / 2:
                        piece_set *= state.checkerboard[col][row].occupied.player == 1
                else:
                    piece_set *= not state.checkerboard[col][row].occupied
        self.assertTrue(piece_set)


    def test_update_states(self):
        state = State()
        state.render_board()
        state.init_pieces()
        self.assertEqual(state.turn, 0)
        self.assertEqual(state.is_capture, 0)
        self.assertEqual(state.piece_or_cell, 0)
        self.assertEqual(state.move_count, 1)
        state.update_state()
        self.assertEqual(state.turn, 1)
        self.assertEqual(state.move_count, 2)


    def test_move_piece(self):
        state = State()
        state.render_board()
        state.init_pieces()
        self.assertEqual(state.checkerboard[0][0].occupied, 0)
        self.assertEqual(state.checkerboard[7][7].occupied, 0)
        state.move_piece(state.checkerboard[0][1], state.checkerboard[0][0])
        state.move_piece(state.checkerboard[7][6], state.checkerboard[7][7])
        self.assertEqual(state.checkerboard[0][0].occupied.player, 0)
        self.assertEqual(state.checkerboard[7][7].occupied.player, 1)


    def test_capture_and_continue(self):
        state = State()
        state.render_board()
        state.init_pieces()
        state.cell_focused = state.checkerboard[0][0]
        cell = state.checkerboard[2][2]
        state.capture_and_continue(cell)
        self.assertEqual(state.cell_focused, state.checkerboard[2][2])


    def test_sample_piece(self):
        state = State()
        state.render_board()
        state.init_pieces()
        state.valid_moves = {(1, 2):[state.checkerboard[0][3], state.checkerboard[2][3]]}
        piece_cell = state.sample_piece()
        self.assertEqual(piece_cell.generate_cell_key()[0], 1)
        self.assertEqual(piece_cell.generate_cell_key()[1], 2)
    
    
    def test_sample_cell(self):
        state = State()
        state.render_board()
        state.init_pieces()
        state.cell_focused = state.checkerboard[1][2]
        state.valid_moves = {(1, 2):[state.checkerboard[0][3], state.checkerboard[2][3]]}
        cell = state.sample_cell()
        self.assertIn(cell.generate_cell_key()[0], [0, 2])
        self.assertEqual(cell.generate_cell_key()[1], 3)

    
    def test_add_jumps_only(self):
        state = State()
        state.render_board()
        state.init_pieces()
        state.cell_focused = state.checkerboard[1][2]
        moves = [state.checkerboard[3][4], state.checkerboard[0][3]]
        state.add_jumps_only(state.cell_focused, moves)
        self.assertEqual(state.valid_moves[(1, 2)], [state.checkerboard[3][4]])


    def test_update_valid_moves_to_jumps(self):
        state = State()
        state.render_board()
        state.init_pieces()
        state.valid_moves = {}
        cell = state.checkerboard[3][2]
        valid_jumps = [state.checkerboard[1][4], state.checkerboard[5][4]]
        state.update_valid_moves_to_jumps(cell, valid_jumps)
        self.assertEqual(state.valid_moves, {(3, 2):[state.checkerboard[1][4], state.checkerboard[5][4]]})


    def test_search_jump(self):
        state = State()
        state.render_board()
        state.checkerboard[3][2].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[2][3].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[4][3].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        jumps = []
        state.search_jump(2, 3, state.checkerboard[3][2], jumps)
        state.search_jump(4, 3, state.checkerboard[3][2], jumps)
        self.assertEqual(jumps, [state.checkerboard[1][4], state.checkerboard[5][4]])
        state.checkerboard[4][3].occupied = 0
        jumps = []
        state.search_jump(2, 3, state.checkerboard[3][2], jumps)
        state.search_jump(4, 3, state.checkerboard[3][2], jumps)
        self.assertEqual(jumps, [state.checkerboard[1][4]])
        state.checkerboard[1][2].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[0][3].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        jumps = []
        state.search_jump(0, 3, state.checkerboard[1][2], jumps)
        state.search_jump(2, 3, state.checkerboard[1][2], jumps)
        self.assertEqual(jumps, [state.checkerboard[3][4]])


    def test_search_next_moves(self):
        state = State()
        state.render_board()
        state.checkerboard[3][2].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[2][3].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[4][3].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        moves = state.search_next_moves(state.checkerboard[3][2])
        self.assertEqual(moves, [state.checkerboard[5][4]])
        state.checkerboard[2][3].occupied = 0
        moves = state.search_next_moves(state.checkerboard[3][2])
        self.assertEqual(moves, [state.checkerboard[2][3], state.checkerboard[5][4]])


    def test_search_next_jumps(self):
        state = State()
        state.render_board()
        state.checkerboard[3][2].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[2][3].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[4][3].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        jumps = state.search_next_jumps(state.checkerboard[3][2])
        self.assertEqual(jumps, [state.checkerboard[5][4]])
        state.checkerboard[2][3].occupied.player = 1
        jumps = state.search_next_jumps(state.checkerboard[3][2])
        self.assertEqual(jumps, [state.checkerboard[1][4], state.checkerboard[5][4]])


    def test_locate_click(self):
        state = State()
        state.render_board()
        cell = state.locate_click(50, -50)
        self.assertEqual(cell.coord.x, 4)
        self.assertEqual(cell.coord.y, 3)
        cell = state.locate_click(-210, 210)
        self.assertEqual(cell, 0)


    def test_take_piece(self):
        state = State()
        state.render_board()
        state.valid_moves = {(3, 2):[state.checkerboard[1][4], state.checkerboard[5][4]]}
        cell = state.take_piece(-25, -75)
        self.assertEqual(cell, state.checkerboard[3][2])
        cell = state.take_piece(-25, -125)
        self.assertEqual(cell, 0)


    def test_take_cell(self):
        state = State()
        state.render_board()
        state.cell_focused = state.checkerboard[3][2]
        state.valid_moves = {(3, 2):[state.checkerboard[1][4], state.checkerboard[5][4]]}
        cell = state.take_cell(-125, 25)
        self.assertEqual(cell, state.checkerboard[1][4])
        self.assertEqual(state.valid_moves.get((4, 3), []), [])
        self.assertFalse(cell in state.valid_moves.get((4, 3), []))
        self.assertTrue(cell in state.valid_moves.get((3, 2), []))
        cell = state.take_cell(25, 25)
        self.assertEqual(cell, 0)


    def test_valid_piece_to_move(self):
        state = State()
        state.render_board()
        state.cell_focused = state.checkerboard[3][2]
        state.valid_moves = {(3, 2):[state.checkerboard[1][4], state.checkerboard[5][4]]}
        self.assertTrue(state.valid_piece_to_move(state.checkerboard[3][2]))
        self.assertFalse(state.valid_piece_to_move(state.checkerboard[1][2]))


    def test_update_valid_moves(self):
        state = State()
        state.render_board()
        state.checkerboard[3][2].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[2][3].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[4][3].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.update_valid_moves()
        self.assertEqual(state.valid_moves, {(3, 2):[state.checkerboard[5][4]]})

        state.checkerboard[2][3].occupied.player = 1
        state.update_valid_moves()
        self.assertEqual(state.valid_moves, {(3, 2):[state.checkerboard[1][4], state.checkerboard[5][4]]})

        state.checkerboard[2][3].occupied = 0
        state.checkerboard[4][3].occupied = 0
        state.is_capture = False
        state.update_valid_moves()
        self.assertEqual(state.valid_moves, {(3, 2):[state.checkerboard[2][3], state.checkerboard[4][3]]})

        state.checkerboard[3][2].occupied.is_king = True
        state.update_valid_moves()
        self.assertEqual(state.valid_moves, {(3, 2):[state.checkerboard[2][1], state.checkerboard[2][3], state.checkerboard[4][1], state.checkerboard[4][3]]})

        state.checkerboard[2][3].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.update_valid_moves()
        self.assertEqual(state.valid_moves, {(3, 2):[state.checkerboard[1][4]]})

    
    def test_auto_play(self):
        state = State()
        state.render_board()
        state.turn = 1
        state.cell_focused = state.checkerboard[4][5]

        state.checkerboard[4][5].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[5][4].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.update_valid_moves()
        cell = state.sample_cell()      
        state.auto_play(cell)
        self.assertEqual(state.checkerboard[4][5].occupied, 0)
        self.assertEqual(state.checkerboard[3][4].occupied.player, 1)

        state.checkerboard[4][5].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[3][4].occupied = 0
        state.checkerboard[5][4].occupied.player = 0
        state.update_valid_moves()
        cell = state.sample_cell() 
        state.auto_play(cell)
        self.assertEqual(state.checkerboard[4][5].occupied, 0)
        self.assertEqual(state.checkerboard[6][3].occupied.player, 1)

        state.checkerboard[4][5].occupied = 0
        state.checkerboard[3][4].occupied = 0
        state.checkerboard[5][4].occupied = 0
        state.checkerboard[6][3].occupied = 0
        state.checkerboard[4][5].occupied = Piece(player = 1, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[5][4].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[3][4].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[5][2].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.checkerboard[3][2].occupied = Piece(player = 0, colors = ['black', 'dark red'], radius = 24, is_king = False)
        state.cell_focused = state.checkerboard[4][5]
        state.update_valid_moves()
        cell = state.sample_cell() 
        state.auto_play(cell)
        self.assertEqual(state.checkerboard[4][5].occupied, 0)
        self.assertEqual(state.checkerboard[4][1].occupied.player, 1)


def main():
    unittest.main()


main()