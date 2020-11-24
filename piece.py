'''
Created by: Shiyao Wang
Time: Nov 11, 2020
Purpose: To represent a piece in the game of Checker
'''
import turtle

DEFAULT_PIECE_COLOR = 'gray'
CROWN_COLOR = 'gold'
CROWN_ROTATE = 80
OCT_ANGLE = 135
CROWN_SHIFT = 30
NUM_EDGE_OCTAGRAM = 8
NUM_EDGE_SQUARE = 4


class Piece:
    '''
    Class -- Piece
    Attributes: 
        player -- an integer, 0 for the human player, 1 for the computer player
        color -- a string, the color of this piece
        radius -- an integer, slightly smaller than the checkerboad cell
        is_king -- a boolean, True if the piece is a king piece
        crown_size -- size of the crown, visible if the piec is a king piece
        crown_color -- a string, the color of the crown
    Methods:
        crown, render_piece, render_circle, render_crown
    '''


    def __init__(self = -1, player = -1, colors = [DEFAULT_PIECE_COLOR, DEFAULT_PIECE_COLOR], radius = -1, is_king = False):
        '''
        Constructor -- creates a new instance of Piece.
        Parameters:
            self -- the current Piece object
            player -- an integer
            colors -- a list of strings, a pair of colors for representing different players
            radius -- an integer, the radius of the piece
            is_king -- a boolean, True if this piece is a king piece, False otherwise
        '''
        self.player = player
        self.color = colors[self.player]
        self.radius = radius
        self.is_king = is_king
        self.crown_size = radius
        self.crown_color = CROWN_COLOR

    
    def __str__(self):
        '''
        Method -- __str__
            Creates a string representation of the Piece.
        Parameter:
            self -- The current Piece object
        Returns:
            A string representation of the Piece.
        '''
        res = 'player: ' + str(self.player)
        res += ', which is '
        res += 'king.' if self.is_king else 'non-king.'
        return res


    def __eq__(self, piece):
        '''
        Method -- __eq__
            Checks if two objects are equal.
        Parameters:
            self -- The current Piece object
            piece -- An object to compare self to.
        Returns:
            A boolean, True if the two objects are equal, False otherwise.
        '''
        return self.player == piece.player


    def crown(self):
        '''
        Function -- crown
            Mark the piece as a king piece.
        Parameters:
            N/A
        Returns:
            N/A. Marks the attribute is_king True.
        '''
        self.is_king = True
    

    def render_piece(self, pen):
        '''
        Function -- render_piece
            Draw the piece using a given turtle.
        Parameters:
            pen -- an instance of Turtle
        Returns:
            N/A. Draws a piece, with crown if it's a king piece.
        '''
        self.render_circle(pen)
        if self.is_king:
            pen.left(CROWN_ROTATE)
            pen.forward(CROWN_SHIFT)
            self.render_crown(pen)
            pen.backward(CROWN_SHIFT)
            pen.right(CROWN_ROTATE)

    
    def render_circle(self, pen):
        '''
        Function -- render_circle
            Draw a circle using a given turtle.
        Parameters:
            pen -- an instance of Turtle
        Returns:
            N/A. Draws a circle to represent the piece.
        '''
        pen.color(self.color)
        pen.begin_fill()
        pen.down()
        pen.circle(self.radius)
        pen.end_fill()
        pen.up()


    def render_crown(self, pen):
        '''
        Function -- render_crown
            Draw a crown on the topright of the piece.
        Parameters:
            pen -- an instance of Turtle
        Returns:
            N/A. Draws a octagram to represent the crown.
        '''
        pen.color(self.crown_color)
        pen.begin_fill()
        pen.down()
        for i in range(NUM_EDGE_OCTAGRAM):
            pen.forward(self.crown_size)
            pen.right(OCT_ANGLE)
        pen.end_fill()
        pen.up()
    