"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)  
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human

        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        self._visited = poc_grid.Grid(grid_height, grid_width)
        self._visited.clear()
        self._distance_field = [[grid_height*grid_width for dummy_col in range(grid_width)] for dummy_row in range(grid_height)]
        
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            list_to_queue = list(self._zombie_list)
        elif entity_type == HUMAN:
            list_to_queue = list(self._human_list)
        else:
            return self._distance_field
        for element in list_to_queue:
            boundary.enqueue(element)
        for cell in boundary:
            self._visited.set_full(cell[0], cell[1])
            self._distance_field[cell[0]][cell[1]] = EMPTY
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbor_cells = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbor_cells:
                if self._visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    self._visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    self._distance_field[neighbor[0]][neighbor[1]] = self._distance_field[current_cell[0]][current_cell[1]] + 1
        return self._distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        print zombie_distance_field
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        obstacle_distance = grid_height*grid_width
        for idx, human in enumerate(self._human_list):
            best_distance = zombie_distance_field[human[0]][human[1]]
            neighbors = self.eight_neighbors(human[0], human[1])
            neighbors.append(human)
            neighbor_distances = []
            for neighbor in neighbors:
                neighbor_distances.append(zombie_distance_field[neighbor[0]][neighbor[1]])
            best_move = []
            best_distance = 0
            for neighbor in neighbors:
                distance = neighbor_distances[neighbors.index(neighbor)]
                if distance > best_distance and distance != obstacle_distance:
                    best_distance = distance
                    best_move = neighbor
            if neighbor_distances[-1] == obstacle_distance:
                best_move = human
            self._human_list[idx] = best_move
                
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for idx, zombie in enumerate(self._zombie_list):
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            neighbors.append(zombie)
            neighbor_distances = []
            for neighbor in neighbors:
                neighbor_distances.append(human_distance_field[neighbor[0]][neighbor[1]])
            
            best = neighbors[neighbor_distances.index(min(neighbor_distances))]
            if neighbor_distances[-1] == (self.get_grid_height() * self.get_grid_width()):
                best = zombie
            self._zombie_list[idx] = best

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Apocalypse(30, 40))
