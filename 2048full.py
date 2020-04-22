"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # move zeroes to the end
    moved_list = [0 for number in line]
    index = 0
    for number in line:
        if number != 0:
            moved_list[index] = number
            index += 1
    # merge pairs of numbers
    paired_list = []
    paired = False
    for index, number in enumerate(moved_list):
        if index < (len(moved_list) - 1):
            if number == moved_list[index + 1] and number != 0 and not paired:
                paired_list.append(number * 2)
                paired_list.append(0)
                paired = True
            elif paired:
                paired = False
            else:
                paired_list.append(number)
        elif not paired:
            paired_list.append(number)
    #move zeroes to the end again
    final_list = [0 for number in line]
    index = 0
    for number in paired_list:
        if number != 0:
            final_list[index] = number
            index += 1
    return final_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        # compute indices
        self._indices = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        self._indices[UP] = [(0, dummy_num) for dummy_num in range(self._grid_width)]
        self._indices[DOWN] = [(self._grid_height - 1, dummy_num) for dummy_num in range(self._grid_width)]
        self._indices[LEFT] = [(dummy_num, 0) for dummy_num in range(self._grid_height)]
        self._indices[RIGHT] = [(dummy_num, self._grid_width - 1) for dummy_num in range(self._grid_height)]
        print self._indices

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._grid = [[0 for dummy_cols in range(self._grid_width)] for dummy_rows in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        offset = OFFSETS[direction]
        changed = False
        for tile_loc in self._indices[direction]:
            temp_list = []
            if offset[0] != 0:
                for num in range(self._grid_height):
                    temp_list.append(self.get_tile(tile_loc[0] + offset[0] * num, tile_loc[1]))
            if offset[1] != 0:
                for num in range(self._grid_width):
                    temp_list.append(self.get_tile(tile_loc[0], tile_loc[1] + offset[1] * num))
            temp_list = merge(temp_list)
            for num, tile_value in enumerate(temp_list):
                if offset[0] != 0:
                    if self.get_tile(tile_loc[0] + offset[0] * num, tile_loc[1]) != tile_value:
                        changed = True
                    self.set_tile(tile_loc[0] + offset[0] * num, tile_loc[1], tile_value)
                if offset[1] != 0:
                    if self.get_tile(tile_loc[0], tile_loc[1] + offset[1] * num) != tile_value:
                        changed = True
                    self.set_tile(tile_loc[0], tile_loc[1] + offset[1] * num, tile_value)
        if changed:
            self.new_tile()
                    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        row = random.randrange(0, self._grid_height)
        col = random.randrange(0, self._grid_width)
        while self.get_tile(row, col) != 0:
            row = random.randrange(0, self._grid_height)
            col = random.randrange(0, self._grid_width)
        if random.random() <= .9:
            self.set_tile(row, col, 2)
        else:
            self.set_tile(row, col, 4)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
