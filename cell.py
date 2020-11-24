'''
Created by: Shiyao Wang
Time: Nov 11, 2020
Purpose: To represent a cell on the checkerboard
'''
import turtle
from coordinate import Coordinate


NUM_EDGE_SQUARE = 4
RIGHT_ANGLE = 90
DEFAULT_COLOR = 'white'


class Cell:
    '''
    Class -- Cell
    Attributes: 
        coord -- a integer coordinate, the coordinate of this cell on the checkerboard
        bottom_left -- a float coordinate, the world coordinate of the bottom_left corner of the cell
        occupied -- a piece, 0 when unoccupied
        edge -- an integer, the length of the edge of this cell
        color -- a string, the color of this cell
    Methods:
        is_click_in, is_adjacent, all_adjacent, render_cell, generate_cell_key, get_coords_to_search
    '''


    def __init__(self, coord = Coordinate(), bottom_left = Coordinate(), edge = -1, color = DEFAULT_COLOR):
        '''
        Constructor -- creates a new instance of Cell.
        Parameters:
            self -- the current Cell object
            coord -- an instance of integer Coordinate
            bottom_left -- an instance of float Coordinate, the position of the bottom left corner of the cell on the checkerboard
            edge -- an integer, the edge length of the cell
            color -- a string, the color of the cell
        '''
        self.coord = Coordinate(coord.x, coord.y)
        self.bottom_left = Coordinate(bottom_left.x, bottom_left.y)
        self.occupied = 0
        self.edge = edge
        self.color = color


    def __str__(self):
        '''
        Method -- __str__
            Creates a string representation of the Cell.
        Parameter:
            self -- The current Cell object
        Returns:
            A string representation of the Cell.
        '''
        res = self.coord.__str__() + ' contains piece: ' + str(self.occupied)
        return res


    def __eq__(self, cell):
        '''
        Method -- __eq__
            Checks if two objects are equal.
        Parameters:
            self -- The current Cell object
            cell -- An object to compare self to.
        Returns:
            A boolean, True if the two objects are equal, False otherwise.
        '''
        return self.coord == cell.coord


    def is_click_in(self, x, y):
        '''
        Method -- is_click_in
            Tell if a float coordinate is in this cell.
        Parameters:
            x -- X coordinate of the input coordinate
            y -- Y coordinate of the input coordinate
        Returns:
            A boolean, True if the coordinate is in this cell.
        '''
        return x >= self.bottom_left.x and \
               x <= self.bottom_left.x + self.edge and \
               y >= self.bottom_left.y and \
               y <= self.bottom_left.y + self.edge


    def is_adjacent(self, cell):
        '''
        Method -- is_adjacent
            Tell if a input cell is among the 8 cells arount this cell.
        Parameters:
            cell -- an instance of Cell
        Returns:
            A boolean, True if the input cell is adjacent to the cell.
        '''
        return abs(cell.coord.x - self.coord.x) <= 1 and \
               abs(cell.coord.y - self.coord.y) <= 1


    def all_adjacent(self, cell_list):
        '''
        Method -- is_adjacent
            Tell if every cell in a input cell list is adjacent to this cell.
        Parameters:
            cell_list -- a list of cells
        Returns:
            A boolean, True if every cell in a input cell list is adjacent to this cell.
        '''
        res = True
        for cell in cell_list:
            res *= self.is_adjacent(cell)
        return res


    def render_cell(self, pen):
        '''
        Method -- render_cell
            Draw the cell using a given turtle.
        Parameters:
            pen -- an instance of Turtle
        Returns:
            N/A. Draws a cell.
        '''
        pen.color('black', self.color)
        pen.begin_fill()
        pen.down()
        for i in range(NUM_EDGE_SQUARE):
            pen.forward(self.edge)
            pen.left(RIGHT_ANGLE)
        pen.end_fill()
        pen.up()


    def generate_cell_key(self):
        '''
        Method -- generate_cell_key
            Convert the coordinate of this cell to a tuple.
        Parameters:
            N/A
        Returns:
            N/A. Converts the coordinate of this cell to a tuple.
        '''
        return tuple([self.coord.x, self.coord.y])

    
    def get_coords_to_search(self):
        '''
        Method -- generate_cell_key
            Gets the x and y coordinates to look for valid moves from this cell.
        Parameters:
            N/A
        Returns:
            A two-element list of lists of integers. Coordinates to search from this cell.
        '''
        res = []
        try:
            x_to_search = [self.coord.x - 1, self.coord.x + 1]
            if self.occupied.is_king:
                y_to_search = [self.coord.y - 1, self.coord.y + 1]
            else:
                y_to_search = [self.coord.y + ( -1 ) ** self.occupied.player]
            res.append(x_to_search)
            res.append(y_to_search)
        except AttributeError:
            NotImplemented
        return res


