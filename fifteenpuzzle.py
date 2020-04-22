"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
    
    def position_tile(self, target_tile, desired_position, original_position, move_string):
        """
        Takes the current location of target_tile (a tuple) and 
        desired position of target tile. Will position target tile to desired_position
        and zero tile one square to left, and return a move string.
        Column must be greater than 0.
        """
        zero_position = self.current_position(0, 0)
        if zero_position[1] == target_tile[1]:
            print "in line"
            for dummy_row in range(zero_position[0] - target_tile[0]):
                self.update_puzzle("u")
                move_string += "u"
            for dummy_row in range(desired_position[0] - 
                                   self.current_position(original_position[0], original_position[1])[0]):
                self.update_puzzle("lddru")
                move_string += "lddru"
                print move_string
            self.update_puzzle("ld")
            move_string += "ld"
        if zero_position [1] > target_tile[1]:
            for dummy_row in range(zero_position[0] - target_tile[0]):
                self.update_puzzle("u")
                move_string += "u"
            for dummy_col in range(zero_position[1] - target_tile[1]):
                self.update_puzzle("l")
                move_string += "l"
            if self.current_position(original_position[0], original_position[1]) == desired_position:
                return move_string
            if self.current_position(original_position[0], original_position[1])[1] != desired_position[1]:
                
                for dummy_col in range(desired_position[1]
                                       - self.current_position(original_position[0], original_position[1])[1]):
                    self.update_puzzle("drrul")
                    move_string += "drrul"
            self.update_puzzle("dru")
            move_string += "dru"
            print move_string
            if self.current_position(original_position[0], original_position[1])[0] != desired_position[0]:
                
                for dummy_row in range(desired_position[0] - self.current_position(original_position[0],
                                                                                   original_position[1])[0]):
                    self.update_puzzle("lddru")
                    move_string += "lddru"
            self.update_puzzle("ld")
            move_string += "ld"
            print move_string
            
        if zero_position [1] < target_tile[1]:
            print "right"
            for dummy_row in range(zero_position[0] - target_tile[0]):
                self.update_puzzle("u")
                move_string += "u"
            for dummy_col in range(target_tile[1] - zero_position[1]):
                self.update_puzzle("r")
                move_string += "r"
            if self.current_position(original_position[0], original_position[1]) == desired_position:
                return move_string
            if self.current_position(original_position[0], original_position[1])[1] != desired_position[1]:
                
                for dummy_col in range(self.current_position(original_position[0], original_position[1])[1] - desired_position[1]):
                    print "push left"
                    self.update_puzzle("dllur")
                    move_string += "dllur"
            self.update_puzzle("dlu")
            move_string += "dlu"
            print move_string
            if self.current_position(original_position[0], original_position[1])[0] != desired_position[0]:
                for dummy_row in range(desired_position[0] - self.current_position(original_position[0],
                                                                                   original_position[1])[0]):
                    print "push down"
                    self.update_puzzle("lddru")
                    move_string += "lddru"
            self.update_puzzle("ld")
            move_string += "ld"
            print move_string
      
        return move_string
        
    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self.current_position(0, 0) != (target_row, target_col):
            print (0, 0)
            return False
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    print (row, col)
                    return False
        for col in range(target_col + 1, self._width):
            if self.current_position(target_row, col) != (target_row, col):
                print (target_row, col)
                return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.lower_row_invariant(target_row, target_col)
        target_tile = self.current_position(target_row, target_col)
        move_string = ""
        move_string = self.position_tile(target_tile, (target_row, target_col), (target_row, target_col), move_string)
        
        print move_string
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.lower_row_invariant(target_row, 0)
        move_string = ""
        self.update_puzzle("ur")
        move_string += "ur"
        print move_string
        if self.current_position(target_row, 0) == (target_row, 0):
            print self._width, self.current_position(0,0)[1]
            print range((self._width - 1) - self.current_position(0,0)[1])
            for dummy_col in range((self._width - 1) - self.current_position(0,0)[1]):
                #print "right!"
                self.update_puzzle("r")
                move_string += "r"
            print move_string
        else:
            target_tile = self.current_position(target_row, 0)
            print "moving tile into position"
            move_string = self.position_tile((target_tile), ((target_row - 1), 1), (target_row, 0), move_string)
            print move_string
            print "problem nine manuever"
            self.update_puzzle("ruldrdlurdluurddlur")
            move_string += "ruldrdlurdluurddlur"
            print move_string
            for dummy_col in range((self._width - 1) - self.current_position(0,0)[1]):
                self.update_puzzle("r")
                move_string += "r"
        assert self.lower_row_invariant(target_row - 1, self._width - 1)    
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.current_position(0, 0) != (0, target_col):
            return False
        for row in range(2, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    return False
        for col in range(target_col, self._width):
            if self.current_position(1, col) != (1, col):
                return False
        for col in range(target_col + 1, self._width):
            if self.current_position(0, col) != (0, col):
                return False
        return True
        

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row0_invariant(target_col)
        move_string = ""
        self.update_puzzle("ld")
        move_string += "ld"
        print move_string
        if self.current_position(0, target_col) != (0, target_col):
            target_tile = self.current_position(0, target_col)
            print "moving tile into position"
            move_string = self.position_tile((target_tile), (1, (target_col - 1)), (0, target_col), move_string)
            print move_string
            print "problem ten manuever"
            self.update_puzzle("urdlurrdluldrruld")
            move_string += "urdlurrdluldrruld"
        print move_string
        #assert self.row0_invariant(target_col - 1)  
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(target_col)
        target_tile = self.current_position(1, target_col)
        move_string = ""
        move_string = self.position_tile(target_tile, (1, target_col), (1, target_col), move_string)
        self.update_puzzle("ur")
        move_string += "ur"
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(1)
        self.update_puzzle("ul")
        move_string = "ul"
        while True:
            if self.current_position(0, 1) == (0, 1):
                break
            self.update_puzzle("rdlu")
            move_string += "rdlu"
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        if self._height > 2:
            for row in range(self._height - 1, 1, -1):
                for col in range(self._width - 1, -1, -1):
                    if col > 0:
                        move_string += self.solve_interior_tile(row, col)
                    else:
                        move_string += self.solve_col0_tile(row)
        if self._width > 2:
            for col in range(self._width - 1, 1, -1):
                move_string += self.solve_row1_tile(col)
                move_string += self.solve_row0_tile(col)
        move_string += self.solve_2x2()
        return move_string
    

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#obj.solve_row1_tile(2)
#obj = Puzzle(2, 2, [[0, 3], [1, 2]])
#obj.solve_2x2()
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]]))
