'''
Created by: Shiyao Wang
Time: Nov 11, 2020
Purpose: To maintain the states of the game
'''


import turtle
import random
from piece import Piece
from cell import Cell
from coordinate import Coordinate


NUM_SQUARES = 8
NUM_PIECES = 12
SQUARE = 50
PIECE_RADIUS = 24
RIGHT_ANGLE = 90
NUM_EDGE_SQUARE = 4
OUT_TIME = 30
PIECE_COLORS = ('black', 'dark red')
CELL_COLORS = ('light gray', 'white')
LINE_COLOR = 'black'
BOARD_COLOR = 'white'
BRUSH_COLOR = 'dark blue'
OUT_COLORS = ['red', 'green', 'blue', 'magenta', 'yellow', 'cyan']

FONT = 'Arial'
FONT_SIZE = 18
FONT_SIZE_BRUSH = 40
FONT_TYPE_HEADER = 'bold'
FONT_TYPE_TEXT = 'normal'

HUMAN = 0
COMPUTER = 1
PLAYERS = ['human', 'computer']
PLAYER_PROMPT = ['your', 'my']
GAME_OVER = ['lose', 'win']

TAKING_PIECE = 0
TAKING_CELL = 1

X_TO_SEARCH = 0
Y_TO_SEARCH = 1

AUTO_DELAY = 500


class State:
    '''
    Class -- State

    Attributes: 
        num_cells -- an integer, the number of cells per row / column
        cell_size -- an integer, the edge length of each cell
        piece_radius -- an integer, the radius of the piece
        piece_colors -- a list of strings, a pair of colors representing different players
        cell_colors -- a list of strings, colors representing cells on the checkerboard
        board_color -- a string, the color of the checkerboard
        board_size -- an integer, the edge length of the checkerboard
        window_size -- an integer, the width of the turtle window
        checkerboard -- a 2D list of cells, representing the actual checkerboard
        cell_focused -- a cell to move a piece from
        valid_moves --  a dict, store valid moves(cells) from each of the 12 cells, tuple(cell.coord.x, cell.coord.y) as the key
        turn -- turn marker for the current move, a boolean, 0 for human, 1 for computer
        piece_or_cell -- whether a click handler is handling a piece to move or a cell to move to
        is_capture -- capture marker for the current move, a boolean, 0 for non-capture move, 1 for capture move
        move_count -- an integer, counting steps taken in the game
        screen -- a turtle screen to draw the UI
        pen -- a turtle pen to render the checkeerboard
        pen_circle -- a turtle pen to draw circles as pieces
        pen_out -- a turtle pen for visual effects of capture moves
        pen_header -- a turtle pen for game information updates
        pen_click -- a turtle pen for click error prompts
        pen_brush -- a turtle pen for welcome page and winner prompts
        pen_brush_steps -- a turtle pen for steps updating

    Methods:
        click_handler
        run_checkers
        switch_player_to_computer
        update_state
        auto_play
        update_valid_moves
        update_valid_moves_to_jump
        sample_piece
        sample_cell
        add_jumps_only
        search_jump
        search_next_moves
        search_next_jumps
        locate_click
        take_piece
        take_cell
        valid_piece_to_move
        move_piece
        capture_and_continue
        burst_cell_in_between
        print_valid_moves
        print_welcome
        print_win
        print_cell_coord
        print_click
        print_invalid_piece
        print_invalid_move
        print_turn
        print_capture
        render_board
        init_pieces
        render_pieces
        tint_out
        tint_red
        tint_green
        tint_blue
        tint_magenta
        tint_yellow
        tint_cyan
        tint
    '''

    def __init__(self):
        '''
        Constructor -- creates a new instance of State.
        Parameters:
            self -- the current State object
        '''
        self.num_cells = NUM_SQUARES
        self.cell_size = SQUARE
        self.piece_radius = PIECE_RADIUS
        self.piece_colors = PIECE_COLORS
        self.cell_colors = CELL_COLORS
        self.board_color = BOARD_COLOR
        self.board_size = self.num_cells * self.cell_size
        self.window_size = self.board_size + self.cell_size
        self.checkerboard = [[0 for i in range(self.num_cells)] for j in range(self.num_cells)]
        self.cell_focused = Cell()
        self.valid_moves = {}
        self.turn = HUMAN
        self.piece_or_cell = TAKING_PIECE
        self.is_capture = False
        self.move_count = 1

        turtle.setup(self.window_size, self.window_size + self.cell_size)
        turtle.screensize(self.board_size, self.board_size)
        turtle.bgcolor(BOARD_COLOR)
        turtle.tracer(0, 0)

        self.screen = turtle.Screen()
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen_circle = turtle.Turtle()
        self.pen_circle.hideturtle()
        self.pen_out = turtle.Turtle()
        self.pen_out.hideturtle()
        self.pen_header = turtle.Turtle()
        self.pen_header.hideturtle()
        self.pen_guide = turtle.Turtle()
        self.pen_guide.hideturtle()
        self.pen_click = turtle.Turtle()
        self.pen_click.hideturtle()
        self.pen_brush = turtle.Turtle()
        self.pen_brush.hideturtle()
        self.pen_brush_steps = turtle.Turtle()
        self.pen_brush_steps.hideturtle()


    def click_handler(self, x, y):
        '''
        Method -- click_handler
            Called when a click occurs.
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle
            y -- Y coordinate of the click. Automatically provided by Turtle
        Returns:
            N/A. Click handlers are a special type of Method automatically called by Turtle. 
            You will not have access to anything returned by this Method.
        '''
        if self.piece_or_cell == TAKING_PIECE:
            self.cell_focused = self.take_piece(x, y)
            if self.cell_focused:
                self.piece_or_cell = TAKING_CELL
        else:
            cell = self.take_cell(x, y)
            if cell:
                self.move_piece(self.cell_focused, cell)
                if self.is_capture:
                    self.capture_and_continue(cell)
                    valid_jumps = self.search_next_jumps(cell)
                    if valid_jumps:
                        self.update_valid_moves_to_jumps(cell, valid_jumps)
                        self.print_capture()
                    else:
                        self.switch_player_to_computer()
                else:
                    self.switch_player_to_computer()


    def run_checkers(self): 
        '''
        Method -- run_checkers
            Called when a game should start.
        Parameters:
            N/A
        Returns:
            N/A, but keeps the game running.
        '''
        self.render_board()
        self.init_pieces()
        self.update_valid_moves()
        self.print_turn()
        self.screen.onclick(self.click_handler) 
        turtle.done()


    def switch_player_to_computer(self):
        '''
        Method -- switch_player_to_computer
            Called when the human player has finished the move.
        Parameters:
            N/A
        Returns:
            N/A, but updates the game state and calls the auto-player.
        '''
        self.update_state()
        self.cell_focused = self.sample_piece()
        to_cell = self.sample_cell()
        self.auto_play(to_cell)
        self.update_state()


    def update_state(self):
        '''
        Method -- update_state
            Called every time when switching player and updates the game state.
        Parameters:
            N/A
        Returns:
            N/A, but refreshes the game state.
        '''
        self.turn = not self.turn
        self.piece_or_cell = TAKING_PIECE
        self.is_capture = False
        self.update_valid_moves()
        if self.valid_moves:
            self.move_count += 1
            self.print_turn()
        else:
            self.print_win()


    def auto_play(self, cell):
        '''
        Method -- auto_play
            Implements the activities of a computer player within one step.
        Parameters:
            N/A
        Returns:
            N/A, but keeps the game running.
        '''
        self.move_piece(self.cell_focused, cell)
        if self.is_capture:
            self.capture_and_continue(cell)
            valid_jumps = self.search_next_jumps(cell)
            if valid_jumps:
                self.update_valid_moves_to_jumps(cell, valid_jumps)
                self.print_capture()
                to_cell = self.sample_cell()
                self.auto_play(to_cell)
        else:
            self.screen.ontimer(self.render_pieces(), AUTO_DELAY)


    def update_valid_moves(self):
        '''
        Method -- update_valid_moves
            Updates the valid_moves dictionary before any move required by the player.
        Parameters:
            N/A
        Returns:
            N/A, but updates the valid_moves dictionary.
        '''
        self.valid_moves.clear()
        for col in range(self.num_cells):
            for row in range(self.num_cells):
                if col % 2 != row % 2:
                    try:
                        if self.checkerboard[col][row].occupied.player == self.turn:
                            moves = self.search_next_moves(self.checkerboard[col][row])
                            if moves:
                                if not self.is_capture:
                                    if self.checkerboard[col][row].all_adjacent(moves):
                                        self.valid_moves[self.checkerboard[col][row].generate_cell_key()] = moves
                                    else:
                                        self.is_capture = True
                                        self.valid_moves.clear()
                                        self.add_jumps_only(self.checkerboard[col][row], moves)
                                else:
                                    self.add_jumps_only(self.checkerboard[col][row], moves)
                    except AttributeError:
                        NotImplemented
        self.print_valid_moves()
 

    def update_valid_moves_to_jumps(self, cell, valid_jumps):
        '''
        Method -- update_valid_moves_to_jumps
            Updates the valid_moves dictionary to a signle item, with a cell as the key and valid jumps from that cell.
        Parameters:
            cell -- a cell, the key cell
            valid_jumps -- a list of cells, valid jumps from the key
        Returns:
            N/A, but updates the valid_moves dictionary to a signle item.
        '''
        self.valid_moves.clear()
        self.valid_moves[cell.generate_cell_key()] = valid_jumps


    def sample_piece(self):
        '''
        Method -- sample_piece
            Samples a cell with a piece that is valid to move.
        Parameters:
            N/A
        Returns:
            A cell, with a piece for the player to move.
        '''
        sampled_key = random.choice(list(self.valid_moves.keys()))
        x = sampled_key[0]   
        y = sampled_key[1] 
        print('sampled_piece: x y: ', x, y)
        return self.checkerboard[x][y]


    def sample_cell(self):
        '''
        Method -- sample_piece
            Samples a cell for a selected piece to move to.
        Parameters:
            N/A
        Returns:
            A cell, with no piece occupied.
        '''
        key = self.cell_focused.generate_cell_key()
        res = random.choice(self.valid_moves[key])
        print('sampled_cell: ', res)
        return res


    def add_jumps_only(self, cell, moves):
        '''
        Method -- add_jumps_only
            Updates valid moves to jumps instead adjacent moves around a given cell.
        Parameters:
            cell -- a cell
            moves -- a list of cells
        Returns:
            A list of cells, containing only those non-adjacent to cell.
        '''
        res = []
        for move in moves:
            if not cell.is_adjacent(move):
                res.append(move)
        if res:
            self.valid_moves[cell.generate_cell_key()] = res


    def search_jump(self, x, y, cell, jumps):
        '''
        Method -- search_jump
            Updates a valid jump of the piece from the input cell to the direction determined by x and y.
        Parameters:
            x -- an integer, the X coordinate of an adjacent cell of the input cell
            y -- an integer, the Y coordinate of an adjacent cell of the input cell
            cell -- a cell
            jumps -- a list of cells to be updated, that maintains valid jumps from the imput cell
        Returns:
            N/A, but updates valid jumps from cell by one if possible.
        '''
        try:
            if self.checkerboard[x][y].occupied.player != cell.occupied.player:
                x_jump = x + (x - cell.coord.x)
                y_jump = y + (y - cell.coord.y)
                if x_jump >= 0 and x_jump <= self.num_cells - 1 and y_jump >= 0 and y_jump <= self.num_cells - 1:
                    if not self.checkerboard[x_jump][y_jump].occupied:
                        jumps.append(self.checkerboard[x_jump][y_jump])
        except AttributeError:
            NotImplemented
        except IndexError:
            NotImplemented


    def search_next_moves(self, cell):
        '''
        Method -- search_next_moves
            Gets all valid moves, either jump or adjacent, from the input cell.
        Parameters:
            cell -- a cell that the piece moves from
        Returns:
            A list of cells that the piece from the cell can move to, either jump or adjacent.
        '''
        res = []
        coords = cell.get_coords_to_search()
        for x in coords[X_TO_SEARCH]:
            for y in coords[Y_TO_SEARCH]:
                if x >= 0 and x <= self.num_cells - 1 and y >= 0 and y <= self.num_cells - 1:
                    if not self.checkerboard[x][y].occupied:
                        res.append(self.checkerboard[x][y])
                    else:
                        self.search_jump(x, y, cell, res)
        return res

    
    def search_next_jumps(self, cell):
        '''
        Method -- search_next_jumps
            Gets all valid jumps from the input cell.
        Parameters:
            cell -- a cell that the piece jumps from
        Returns:
            A list of cells that the piece from the cell can jump to.
        '''
        res = []
        coords = cell.get_coords_to_search()
        for x in coords[X_TO_SEARCH]:
            for y in coords[Y_TO_SEARCH]:
                self.search_jump(x, y, cell, res)
        return res


    def locate_click(self, x, y):
        '''
        Method -- locate_click
            Gets the cell given the click coordinate on the board.
        Parameters:
            x -- an integer, the X coordinate from the caller
            y -- an integer, the Y coordinate from the caller
        Returns:
            A cell that contains the clicked point, 0 if not a cell.
        '''
        for col in range(self.num_cells):
            for row in range(self.num_cells):
                if row % 2 != col % 2:
                    if self.checkerboard[col][row].is_click_in(x, y):
                        return self.checkerboard[col][row]
        return 0


    def take_cell(self, x, y):
        '''
        Method -- take_cell
            Gets a cell for the piece from the focused cell to move to.
        Parameters:
            x -- an integer, the X coordinate from the caller
            y -- an integer, the Y coordinate from the caller
        Returns:
            A cell containing the input coordinate that is a valid destination for the piece from the focused cell.
        '''
        key = self.cell_focused.generate_cell_key() 
        cell = self.locate_click(x, y)
        try:
            if cell in self.valid_moves.get(key, []):
                self.pen_click.clear()
                print('take cell: x y:', cell.coord.x, cell.coord.y)
                return cell
        except AttributeError:
            NotImplemented
        self.print_invalid_move()
        return 0
                

    def take_piece(self, x, y):
        '''
        Method -- take_piece
            Gets a piece if it is valid to move.
        Parameters:
            x -- an integer, the X coordinate from the caller
            y -- an integer, the Y coordinate from the caller
        Returns:
            A cell containing the input coordinate that contains a valid piece to move, 0 if doesn't contain a valid piece.
        '''
        cell = self.locate_click(x, y)
        try:
            if self.valid_piece_to_move(cell):
                self.pen_click.clear()
                print('take piece: x y: ', cell.coord.x, cell.coord.y)
                return cell
        except AttributeError:
            NotImplemented
        self.print_invalid_piece()
        return 0


    def valid_piece_to_move(self, cell):
        '''
        Method -- valid_piece_to_move
            Judges whether the input cell contains a valid piece to move.
        Parameters:
            cell -- a cell, the input cell to judge
        Returns:
            A boolean, True if is a cell that contains a valid piece to move, False if not.
        '''
        key = cell.generate_cell_key()
        return key in self.valid_moves.keys()


    def move_piece(self, from_cell, to_cell):
        '''
        Method -- move_piece
            Moves a piece from one place to another place on the checkerboard.
        Parameters:
            from_cell -- a cell, that the piece comes from
            to_cell -- a cell, that the piece moves to
        Returns:
            N/A, but updates the occupied state in both cells
        '''
        to_cell.occupied = from_cell.occupied
        from_cell.occupied = 0
        if to_cell.coord.y == ( self.num_cells - 1 ) * ( 1 - self.turn ):
            to_cell.occupied.crown()


    def capture_and_continue(self, cell):
        '''
        Method -- capture_and_continue
            Renders a burst effect to the cell in between of the input cell and the focused cell, then updates the focused cell.
        Parameters:
            cell -- a cell, that the piece from the focused cell moves to
        Returns:
            N/A, but render a visual effect and updates the focused cell.
        '''
        self.burst_cell_in_between(self.cell_focused, cell)
        self.screen.ontimer(self.render_pieces(), AUTO_DELAY)
        self.cell_focused = cell


    def burst_cell_in_between(self, first_cell, second_cell):
        '''
        Method -- capture_and_continue
            Renders a burst effect to the cell in between of two cells.
        Parameters:
            first_cell -- a cell
            second_cell -- a cell
        Returns:
            N/A, but renders a visual effect to the cell in between of the two input cells.
        '''
        x = int(( first_cell.coord.x + second_cell.coord.x ) / 2)
        y = int(( first_cell.coord.y + second_cell.coord.y ) / 2)
        self.pen_out.setposition(- self.board_size / 2 + self.cell_size * (x + 0.5), - self.board_size / 2 + self.cell_size * y)
        self.tint_out()
        self.checkerboard[x][y].occupied = 0


    def print_valid_moves(self):
        '''
        Method -- print_valid_moves
            Prints the valid_moves dictionary to the terminal as the game runs.
        Parameters:
            N/A
        Returns:
            N/A, but prints the valid_moves dictionary to the terminal.
        '''
        out_dict = {}
        for key in self.valid_moves.keys():
            moves = self.valid_moves[key]
            for move in moves:
                if not key in out_dict:
                    out_dict[key] = [] 
                coord_str = move.coord.__str__()
                out_dict[key].append(coord_str)
        print('****************************************************************')
        print("Who's turn: ", PLAYERS[self.turn])
        print('Valid moves at this moment: ')
        for key in out_dict.keys():
            print(key, ':', out_dict[key])


    def print_welcome(self):
        '''
        Method -- print_welcome
            Prints the welcome page to the UI when the game starts.
        Parameters:
            N/A
        Returns:
            N/A, but prints the welcome page to the UI.
        '''
        self.pen_brush.write("Welcome to the game!", align = 'center', font = (FONT, FONT_SIZE_BRUSH, FONT_TYPE_TEXT))
        self.screen.ontimer(self.pen_brush.clear(), AUTO_DELAY)
        self.pen_brush.write("This is Mr.Robot playing!", align = 'center', font = (FONT, FONT_SIZE_BRUSH, FONT_TYPE_TEXT))
        self.screen.ontimer(self.pen_brush.clear(), AUTO_DELAY)


    def print_win(self):
        '''
        Method -- print_win
            Prints the winner prompts to the UI when the game is over.
        Parameters:
            N/A
        Returns:
            N/A, but prints the winner prompts to the UI.
        '''
        if self.turn == HUMAN:
            out_str = 'Ahhh!  '
        else:
            out_str = 'Congrats! '
        out_str += 'You ' + GAME_OVER[self.turn] + '!'
        self.pen_brush.write(out_str, align = 'center', font = (FONT, FONT_SIZE_BRUSH, FONT_TYPE_TEXT))
        out_steps = 'After ' + str(self.move_count) + ' steps.'
        self.pen_brush_steps.write(out_steps, align = 'center', font = (FONT, FONT_SIZE_BRUSH, FONT_TYPE_TEXT))


    def print_cell_coord(self, col, row):
        '''
        Method -- print_cell_coord
            Prints the coordinate of a cell on the checkerboard to the UI.
        Parameters:
            col -- an integer, column number of the cell
            row -- an integer, row number of the cell
        Returns:
            N/A, but prints the coordinate of a cell on the checkerboard to the UI.
        '''
        self.pen_click.clear()
        self.pen_click.write('Cell ' + str(col) +  ' ' + str(row) + ' ' + 'on the board.', font = (FONT, FONT_SIZE, FONT_TYPE_TEXT))


    def print_click(self, x, y):
        '''
        Method -- print_click
            Prints the coordinate of the clicked cell to the UI.
        Parameters:
            x -- an integer, the X coordinate from the caller
            y -- an integer, the Y coordinate from the caller
        Returns:
            N/A, but prints the coordinate of the clicked cell to the UI.
        '''
        self.pen_click.clear()
        self.pen_click.write('Clicked at ' + str(x) + str(y), font = (FONT, FONT_SIZE, FONT_TYPE_TEXT))


    def print_invalid_piece(self):
        '''
        Method -- print_invalid_piece
            Prompts a notice to the UI that the selected piece is invalid to move.
        Parameters:
            N/A
        Returns:
            N/A, but prompts a notice to the UI that the piece is invalid.
        '''
        self.pen_click.clear()
        self.pen_click.write('Not a valid ' + str(self.piece_colors[self.turn]) + ' piece. Try again.', font = (FONT, FONT_SIZE, FONT_TYPE_TEXT))


    def print_invalid_move(self):
        '''
        Method -- print_invalid_piece
            Prompts a notice to the UI that the selected cell is invalid to move to.
        Parameters:
            N/A
        Returns:
            N/A, but prompts a notice to the UI that the cell is invalid.
        '''
        self.pen_click.clear()
        self.pen_click.write('Not a valid move. Try diagnally. Capture if possible.', font = (FONT, FONT_SIZE, FONT_TYPE_TEXT))


    def print_turn(self): 
        '''
        Method -- print_invalid_piece
            Prints whose turn it is when the player is switched.
        Parameters:
            N/A
        Returns:
            N/A, but prints whose turn it is.
        '''
        self.pen_header.clear()
        self.pen_header.write('Checkers!   Move: ' + str(self.move_count) + "   It's " + PLAYER_PROMPT[self.turn] + ' turn. ', font = (FONT, FONT_SIZE, FONT_TYPE_HEADER))
        self.pen_guide.clear()
        if self.turn == HUMAN:
            self.pen_guide.write('Move a ' + self.piece_colors[self.turn] + ' piece by clicking it and a cell.', font = (FONT, FONT_SIZE, FONT_TYPE_TEXT))


    def print_capture(self):
        '''
        Method -- print_invalid_piece
            Prompts a notice to the UI that the player should keep capturing.
        Parameters:
            N/A
        Returns:
            N/A, but prompts a notice to the UI that the player should keep capturing.
        '''
        self.pen_guide.clear()
        self.pen_guide.color('dark red')
        self.pen_guide.write('Keep capturing with this piece by clicking a cell!', font = (FONT, FONT_SIZE, FONT_TYPE_TEXT))
        self.pen_guide.color('black')


    def render_board(self):
        '''
        Method -- render_board
            Draw the checkerboard with white and gray cells at the beginning of the game.
        Parameters:
            pen -- an instance of Turtle
            board_size -- the length of the edge of the checkerboard
            window_size -- the length of the edge of the window
        Returns:
            N/A. Draws checkerboard with white and gray cells.
        '''
        self.pen.penup()
        self.pen.color(LINE_COLOR, BOARD_COLOR)

        corner = - self.board_size / 2
        self.pen.setposition(corner, corner)
        self.pen_header.setposition(- self.board_size / 2, self.board_size / 2 + self.cell_size / 2)
        self.pen_guide.setposition(- self.board_size / 2, self.board_size / 2)
        self.pen_click.setposition(- self.board_size / 2, - self.board_size / 2 - self.cell_size / 2)
        
        self.pen_brush.up()
        self.pen_brush.setposition(0, 0)
        self.pen_brush.color(BRUSH_COLOR)

        self.pen_brush_steps.up()
        self.pen_brush_steps.setposition(0, - self.cell_size)
        self.pen_brush_steps.color(BRUSH_COLOR)

        self.print_welcome()

        large_cell = Cell(edge = self.board_size)
        large_cell.render_cell(self.pen)

        for col in range(self.num_cells):
            for row in range(self.num_cells):
                bottom_left = Coordinate(corner + self.cell_size * col, corner + self.cell_size * row)
                coord = Coordinate(col, row)
                if col % 2 != row % 2:
                    self.checkerboard[col][row] = Cell(coord, bottom_left, self.cell_size, self.cell_colors[0])
                    self.pen.setposition(bottom_left.x, bottom_left.y)
                    self.checkerboard[col][row].render_cell(self.pen)
                else:
                    self.checkerboard[col][row] = Cell(coord, bottom_left, self.cell_size, self.cell_colors[0])


    def init_pieces(self):
        '''
        Method -- init_pieces
            Initiate pieces for designated cells on the board and render the pieces.
        Parameters:
            N/A
        Returns:
            N/A. Draws pieces initiated in the cells.
        '''
        corner = - self.board_size / 2
        self.pen_circle.penup()
        self.pen_circle.color(LINE_COLOR)
        for col in range(self.num_cells):
            for row in range(self.num_cells):
                if col % 2 != row % 2:
                    self.pen_circle.setposition(corner + self.cell_size * (col + 1 / 2), corner + self.cell_size * row)
                    if row < self.num_cells / 2 - 1:
                        piece = Piece(player = HUMAN, colors = self.piece_colors, radius = self.piece_radius, is_king = False)
                        self.checkerboard[col][row].occupied = piece
                        piece.render_piece(self.pen_circle)
                    elif row > self.num_cells / 2:
                        piece = Piece(player = COMPUTER, colors = self.piece_colors, radius = self.piece_radius, is_king = False)
                        self.checkerboard[col][row].occupied = piece
                        piece.render_piece(self.pen_circle)


    def render_pieces(self):
        '''
        Method -- render_pieces
            Iterates through all cells on the board and render the piece if there is one.
        Parameters:
            N/A
        Returns:
            N/A. Draws pieces after a screen update.
        '''
        corner = - self.board_size / 2
        self.pen_circle.clear()
        for col in range(self.num_cells):
            for row in range(self.num_cells):
                if col % 2 != row % 2:
                    try:
                        self.pen_circle.setposition(corner + self.cell_size * (col + 0.5), corner + self.cell_size * row)
                        self.checkerboard[col][row].occupied.render_piece(self.pen_circle)
                    except AttributeError:
                        not NotImplemented


    def tint_out_recursive(self):
        '''
        Method -- tint_out_recursive
            Renders a color flashing effect to a cell on the checkerboard.
        Parameters:
            N/A
        Returns:
            N/A, but renders a visual effect.
        
        It seems turtle doesn't display the colors if the flashing color 
        method is written in a recursive form.
        Everything inside a single loop are skipped, only the ultimate result 
        is displayed when tracer(0, 0) is on. 
        Therefore, we have to create serial methods with distinct names.
        '''
        self.pen.clear()
        if len(OUT_COLORS) == 0:
            self.screen.ontimer(self.pen_out.clear(), OUT_TIME)
        else:
            self.pen.clear()
            self.pen.color(self.out_colors.pop())
            self.pen.begin_fill()
            self.pen.down()
            self.pen.circle(self.piece_radius)
            self.pen.end_fill()
            self.pen.up()
            self.screen.ontimer(self.tint_out_recursive, OUT_TIME)


    def tint_out(self):
        '''
        Method -- tint_out
            Call serial flashing color methods after some time.
        Parameters:
            N/A
        Returns:
            N/A. Calls a flashing color(red) method after some time.
        '''
        self.screen.ontimer(self.tint_red, OUT_TIME)


    def tint_red(self):
        '''
        Method -- tint_red
            Flashes red and call the next flashing color(green).
        Parameters:
            N/A
        Returns:
            N/A. Calls a flashing color(green) method after some time.
        '''
        self.tint('red')
        self.screen.ontimer(self.tint_green, OUT_TIME)


    def tint_green(self):
        '''
        Method -- tint_green
            Flashes green and call the next flashing color(blue).
        Parameters:
            N/A
        Returns:
            N/A. Calls a flashing color(blue) method after some time.
        '''
        self.tint('green')
        self.screen.ontimer(self.tint_blue, OUT_TIME)


    def tint_blue(self):
        '''
        Method -- tint_blue
            Flashes blue and call the next flashing color(magenta).
        Parameters:
            N/A
        Returns:
            N/A. Calls a flashing color(magenta) method after some time.
        '''
        self.tint('blue')
        self.screen.ontimer(self.tint_magenta, OUT_TIME)


    def tint_magenta(self):
        '''
        Method -- tint_magenta
            Flashes magenta and call the next flashing color(yellow).
        Parameters:
            N/A
        Returns:
            N/A. Calls a flashing color(yellow) method after some time.
        '''
        self.tint('magenta')
        self.screen.ontimer(self.tint_yellow, OUT_TIME)


    def tint_yellow(self):
        '''
        Method -- tint_yellow
            Flashes yellow and call the next flashing color(cyan).
        Parameters:
            N/A
        Returns:
            N/A. Calls a flashing color(cyan) method after some time.
        '''
        self.tint('yellow')
        self.screen.ontimer(self.tint_cyan, OUT_TIME)
    

    def tint_cyan(self):
        '''
        Method -- tint_cyan
            Flashes cyan and delete this piece from the board after some time.
        Parameters:
            N/A
        Returns:
            N/A. Calls the clear method to the pen after some time.
        '''
        self.tint('cyan')
        self.screen.ontimer(self.pen_out.clear(), OUT_TIME)


    def tint(self, color):
        '''
        Method -- tint
            Perform a color flashing across the board.
        Parameters:
            color -- a string, the color to flash.
        Returns:
            N/A. Performs a color flashing across the board.
        '''
        self.pen_out.clear()
        self.pen_out.color(color)
        self.pen_out.begin_fill()
        self.pen_out.down()
        self.pen_out.circle(self.piece_radius)
        self.pen_out.end_fill()
        self.pen_out.up()