
import node
import numpy as np
import config

class Grid:
    """ Implementation of the grid class which serves as playground for pathfinding Algos

        Attributes:
            grid_world_size
            grid_image
            unwalkable_mask
            grid
            grid_image

    """
    def __init__(self, grid_world_size, unwalkable_mask):
        self.grid_world_size = grid_world_size
        self.grid_image = None
        self.unwalkable_mask = unwalkable_mask
        self.grid = []
        self.grid_image = np.zeros((grid_world_size[0], grid_world_size[1]))
        self.init_grid()


    def init_grid(self):
        # Create 2D grid of nodes and set node properties
        # according to unwalkable_mask
        for i in range(self.grid_world_size[0]):
            self.grid.append([])
            for j in range(self.grid_world_size[1]):
                self.grid[i].append(node.Node())
                self.grid[i][j].position = (i,j)
                if str((i, j)) not in self.unwalkable_mask:
                    #print((i,j), " Not in unwalkable")
                    self.grid[i][j].walkable = True


    def print_grid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                print("Inhalt",self.grid[i][j].position, self.grid[i][j].walkable)




    def get_neighbours(self, current_node):

        neighbours = []

        for i in range(-1, 2):
            for j in range(-1, 2):

                eval_x = current_node.position[0] + i
                eval_y = current_node.position[1] + j

                if current_node.position[0] == eval_x and current_node.position[1] == eval_y:  # ( [ besser loesen
                    continue
                else:
                    if eval_x >= 0 and eval_x < self.grid_world_size[0] and eval_y >= 0 and eval_y < \
                            self.grid_world_size[1]:  # ich denke kleiner und nich gleich
                        neighbours.append(self.grid[eval_x][eval_y])
                        print("self.grid[eval_x][eval_y]   ", self.grid[eval_x][eval_y])

        return neighbours

    def get_neighbours_four_way(self, current_node):

        """
        Definitely not te most elegant solution
        as Im setting the neighbour indices by hand
        Next iteration will improve this

        :param current_node:
        :return:
        """
        neighbours = []


        top_x = current_node.position[0]
        top_y = current_node.position[1]-1
        bottom_x = current_node.position[0]
        bottom_y = current_node.position[1]+1
        left_x = current_node.position[0]-1
        left_y = current_node.position[1]
        right_x = current_node.position[0]+1
        right_y = current_node.position[1]

        if top_x >= 0 and top_x < self.grid_world_size[0] and top_y >= 0 and top_y < self.grid_world_size[1]:
            neighbours.append(self.grid[top_x][top_y])

        if bottom_x >= 0 and bottom_x < self.grid_world_size[0] and bottom_y >= 0 and bottom_y < self.grid_world_size[1]:
            neighbours.append(self.grid[bottom_x][bottom_y])

        if left_x >= 0 and left_x < self.grid_world_size[0] and left_y >= 0 and left_y < self.grid_world_size[1]:
            neighbours.append(self.grid[left_x][left_y])

        if right_x >= 0 and right_x < self.grid_world_size[0] and right_y >= 0 and right_y < self.grid_world_size[1]:
            neighbours.append(self.grid[right_x][right_y])

        return neighbours

