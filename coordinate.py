'''
Created by: Shiyao Wang
Time: Nov 12, 2020
Purpose: To represent a two-dimensional coordinate
'''


class Coordinate:
    '''
    Class -- Coordinate
    Attributes: 
        x -- an integer or a float, the X coordinate
        y -- an integer or a float, the Y coordinate
    Methods:
        increment_x, increment_y, add_x, add_y, add
    '''


    def __init__(self, x = 0, y = 0):
        '''
        Constructor -- creates a new instance of Coordinate.
        Parameters:
            self -- the current Coordinate object
            x -- an integer or a float, the X coordinate
            y -- an integer or a float, the Y coordinate
        '''
        self.x = x
        self.y = y


    def __str__(self):
        '''
        Method -- __str__
            Creates a string representation of the Coordinate.
        Parameter:
            self -- The current Coordinate object
        Returns:
            A string representation of the Coordinate.
        '''
        out = 'x: ' + str(self.x) + ' ' + 'y: ' + str(self.y)
        return out


    def __eq__(self, coord):
        '''
        Method -- __eq__
            Checks if two objects are equal.
        Parameters:
            self -- The current Coordinate object
            coord -- An object to compare self to.
        Returns:
            True if the two objects are equal, False otherwise.
        '''
        return self.x == coord.x and self.y == coord.y


    def increment_x(self):
        '''
        Method -- increment_x
            Increments x by 1.
        Parameters:
            N/A
        Returns:
            N/A. Increments x by 1.
        '''
        self.x += 1


    def increment_y(self):
        '''
        Method -- increment_y
            Increments y by 1.
        Parameters:
            N/A
        Returns:
            N/A. Increments y by 1.
        '''
        self.y += 1


    def add_x(self, adder):
        '''
        Method -- add_x
            Adds a value to x.
        Parameters:
            adder -- an integer or a float, to add to x
        Returns:
            N/A. Adds a value to x.
        '''
        self.x += adder


    def add_y(self, adder):
        '''
        Method -- add_y
            Adds a value to y.
        Parameters:
            adder -- an integer or a float, to add to y
        Returns:
            N/A. Adds a value to y.
        '''
        self.y += adder


    def add(self, coord):
        '''
        Method -- add
            Adds a coordinate to this coordinate.
        Parameters:
            coord -- an instance of Coordinate
        Returns:
            N/A. Adds a coordinate to this coordinate.
        '''
        self.x += coord.x
        self.y += coord.y

