import node


HEURISTIC_COST_DIAGONAL = 14
HEURISTIC_COST_VERTICAL_HORIZONTAL = 10

# Heuristic for 4 direction movement (Mahnattan)
def get_h_cost(node_a, node_b):
    """ Return the heuristic_cost that it takes to get from node_a to node_b.
        Heuristic: Diagonal movement cost = 14 , vertical/horizontal movement cost = 10
    """
    global HEURISTIC_COST_DIAGONAL
    global HEURISTIC_COST_VERTICAL_HORIZONTAL

    dis_x = abs(node_a.position[0] - node_b.position[0])
    dis_y = abs(node_a.position[1] - node_b.position[1])
    D = 1
    return D * (dis_x + dis_y)

def get_h_cost_dijkstra(node_a, node_b):
    """ Return the heuristic_cost that it takes to get from node_a to node_b.
        Heuristic: Diagonal movement cost = 14 , vertical/horizontal movement cost = 10
    """
    global HEURISTIC_COST_DIAGONAL
    global HEURISTIC_COST_VERTICAL_HORIZONTAL

    dis_x = abs(node_a.position[0] - node_b.position[0])
    dis_y = abs(node_a.position[1] - node_b.position[1])
    D = 0
    return D * (dis_x + dis_y)


def retrace_path(start_node, end_node):
    """ Returns the path from start_node to end_node by accessing each nodes parent node
    """
    path = []
    current_node = end_node


    while ( current_node.position != start_node.position ):
        path.append(current_node)
        current_node = current_node.parent

        print(current_node.position)

    path.append(start_node)
    return path


class Pathfinder:
    """ The pathfinder finds the shortest path from a starting node to a target node
        using the well known A*-Algorithm

        Attributes:
            open_set
            closed_set              The nodes (x,y) position in a 2D grid.
            grid                    The cost that it takes to reach the node from the starting node.
            start_node_position     The cost that it takes to teach the target node from the current node (Heuristic).
            target_node_position    The parent node from which the current node has originated from, which is needed to
    """
    #world_grid, self.map_wall_list, self.start_node, self.target_node)
    def __init__(self, grid, map_element_status_dict, start_node_position, target_node_position):
        self.open_set = []
        self.closed_set = []
        self.grid = grid
        self.start_node_position = start_node_position
        self.target_node_position = target_node_position
        self.map_element_status_dict = map_element_status_dict

    ######################################################
    # A-Star Algorithm
    ######################################################
    def find_path_astar(self):
        start_node = node.Node(False, eval(self.start_node_position))
        target_node = node.Node(False, eval(self.target_node_position))
        start_node.h_cost = get_h_cost(start_node, target_node)

        # Step 1:
        # Add start node to the open set
        self.open_set.append(start_node)

        # Step 2:
        # Enter Loop
        # While current_node != target node
        while len(self.open_set) > 0:
            # Step 3:
            # Set current node to first node from the open set
            current_node = self.open_set[0]

            # Step 4.
            # Find node in the open_set which has the lowest f_cost:
            # If the the current_node and a node from the open_set have the same f_cost:
            #   take the node with the lowest h_cost
            for i in self.open_set:

                # Hint. Loopin like that is obviously terribly unoptimized
                # Since we have to iterate through all nodes
                # Using a Hashtable datastructure would speed the algorithm up dramatically
                # However, the purpose of this example is readability and to teach the basic idea of AStar
                if i.get_f_cost() < current_node.get_f_cost() or (
                        i.get_f_cost() == current_node.get_f_cost() and i.h_cost < current_node.h_cost):
                    current_node = i

            # Step 5
            # Remove current node from the open set and append it to the closed set
            self.open_set.remove(current_node)
            self.closed_set.append(current_node)

            # Step 6.
            # Check if:     current_node == target_node -> return path
            #       else:   we need to update costs to neighbours if they were aleady cosidered:
            #                   check if neighbour of current node is walkable and or in the closed set
            #                   determine new costs to neighbour
            #                   if new costs are lower than old costs -> set new costs and set current node as parent of neighbour
            if current_node.position[0] == target_node.position[0] and current_node.position[1] == target_node.position[
                1]:
                path = retrace_path(start_node, current_node)
                path.pop(0)
                path.pop(-1)
                return path, self.closed_set

            # neighbours = self.grid.get_neighbours(current_node)
            neighbours = self.grid.get_neighbours_four_way(current_node)

            # If node is unwalkable or neighbour is in closed_set
            for i in neighbours:
                if i.walkable == False or i in self.closed_set:
                    continue

                new_cost_to_neighbour = current_node.g_cost + get_h_cost(current_node, i)

                if new_cost_to_neighbour < i.g_cost or i not in self.open_set:
                    i.g_cost = new_cost_to_neighbour
                    i.h_cost = get_h_cost(i, target_node)
                    i.parent = current_node

                    if i not in self.open_set:
                        self.open_set.append(i)

    ######################################################
    # Dijkstra Algorithm
    ######################################################
    def find_path_dijkstra(self):
        start_node = node.Node(False, eval(self.start_node_position))
        target_node = node.Node(False, eval(self.target_node_position))
        start_node.h_cost = get_h_cost(start_node, target_node)

        #Init
        for i in range(self.grid.grid_world_size[0]):
            for j in range(self.grid.grid_world_size[1]):
                if i == start_node.position[0] and j == start_node.position[1]:
                    pass
                else:
                    self.grid.grid[i][j].g_cost = 1000000000000 # high cost

        # Step 1:
        # Add start node to the open set
        self.open_set.append(start_node)

        # Step 2:
        # Enter Loop
        # While current_node != target node
        while len(self.open_set) > 0:
            # Step 3:
            # Set current node to first node from the open set
            current_node = self.open_set[0]

            # Step 4.
            # Find node in the open_set which has the lowest f_cost:
            # If the the current_node and a node from the open_set have the same f_cost:
            #   take the node with the lowest h_cost
            for i in self.open_set:

                # Hint. Loopin like that is obviously terribly unoptimized
                # Since we have to iterate through all nodes
                # Using a Hashtable datastructure would speed the algorithm up dramatically
                # However, the purpose of this example is readability and to teach the basic idea of AStar
                if i.get_g_cost() < current_node.get_g_cost():
                    current_node = i

            # Step 5
            # Remove current node from the open set and append it to the closed set
            self.open_set.remove(current_node)
            self.closed_set.append(current_node)

            neighbours = self.grid.get_neighbours_four_way(current_node)


            # Step 6.
            # Check if:     current_node == target_node -> return path
            #       else:   we need to update costs to neighbours if they were aleady cosidered:
            #                   check if neighbour of current node is walkable and or in the closed set
            #                   determine new costs to neighbour
            #                   if new costs are lower than old costs -> set new costs and set current node as parent of neighbour
            if current_node.position[0] == target_node.position[0] and current_node.position[1] == target_node.position[
                1]:
                path = retrace_path(start_node, current_node)
                path.pop(0)
                path.pop(-1)
                return path, self.closed_set


            # If node is unwalkable or neighbour is in closed_set
            for i in neighbours:
                if i.walkable == False or i in self.closed_set:
                    continue

                new_cost_to_neighbour = current_node.g_cost

                if new_cost_to_neighbour < i.g_cost:
                    i.g_cost = new_cost_to_neighbour
                    i.parent = current_node

                    if i not in self.open_set:
                        self.open_set.append(i)

    ######################################################
    # Depth-First-Search Algorithm
    ######################################################
    def find_path_dfs(self):
        path_stack = []
        visualization_stack = []

        start_node = node.Node(False, eval(self.start_node_position))
        target_node = node.Node(False, eval(self.target_node_position))
        current_node = start_node
        path_stack.append(current_node)
        current_direction = "up" # init direction is up ->

        while(path_stack):
            # Mark current node as visited in the grid
            self.grid.grid[current_node.position[0]][current_node.position[1]].visited = True
            current_node = self.grid.grid[current_node.position[0]][current_node.position[1]]
            if current_node not in visualization_stack:
                visualization_stack.append(current_node)

            # Check if target node found
            if current_node.position == target_node.position:
                path_stack.pop(0)
                path_stack.pop(0)
                path_stack.reverse()
                return path_stack, visualization_stack

            if self.up_node_valid(current_node):
                path_stack.append(current_node)
                current_direction = "up"
                current_node = self.get_specific_neighbour(current_node,current_direction)
            elif self.right_node_valid(current_node):
                path_stack.append(current_node)
                current_direction = "right"
                current_node = self.get_specific_neighbour(current_node, current_direction)
            elif self.down_node_valid(current_node):
                path_stack.append(current_node)
                current_direction = "down"
                current_node = self.get_specific_neighbour(current_node, current_direction)
            elif self.left_node_valid(current_node):
                path_stack.append(current_node)
                current_direction = "left"
                current_node = self.get_specific_neighbour(current_node, current_direction)
            else:
                current_node = path_stack.pop()

        return path_stack, visualization_stack

    def up_node_valid(self, current_node):
        current_node_x = current_node.position[0]
        current_node_y = current_node.position[1]
        if current_node_x - 1 >= 0 \
                and self.grid.grid[current_node_x-1][current_node_y].walkable == True\
                and self.grid.grid[current_node_x-1][current_node_y].visited == False:
            return True
        else:
            return False

    def right_node_valid(self, current_node):
        current_node_x = current_node.position[0]
        current_node_y = current_node.position[1]
        grid_width = self.grid.grid_world_size[0]
        if current_node_y + 1 <= grid_width - 1 \
                and self.grid.grid[current_node_x][current_node_y+1].walkable == True\
                and self.grid.grid[current_node_x][current_node_y+1].visited == False:
            return True
        else:
            return False

    def down_node_valid(self, current_node):
        current_node_x = current_node.position[0]
        current_node_y = current_node.position[1]
        grid_height = self.grid.grid_world_size[1]

        if current_node_x + 1 <= grid_height - 1 \
             and self.grid.grid[current_node_x + 1][current_node_y].walkable == True \
             and self.grid.grid[current_node_x + 1][current_node_y].visited == False:
            return True
        else:
            return False

    def left_node_valid(self, current_node):
        current_node_x = current_node.position[0]
        current_node_y = current_node.position[1]

        if current_node_y - 1 >= 0 \
                and self.grid.grid[current_node_x][current_node_y - 1].walkable == True \
                and self.grid.grid[current_node_x][current_node_y - 1].visited == False:
            return True
        else:
            return False

    # Return the Neighbour node which is the adjecent node in current searching/expending direction
    def get_specific_neighbour(self, current_node, current_direction):
        current_node_x = current_node.position[0]
        current_node_y = current_node.position[1]

        if current_direction == "right":
            return self.grid.grid[current_node_x][current_node_y + 1]

        if current_direction == "left":
            return self.grid.grid[current_node_x][current_node_y - 1]

        if current_direction == "up":
            return self.grid.grid[current_node_x - 1][current_node_y]

        if current_direction == "down":
            return self.grid.grid[current_node_x + 1][current_node_y]


    # Check if in the current direction there is enough depth meaning a node that is walkable and that exists
    def has_valid_neighbours(self, current_node):
        current_node_y = current_node.position[1]
        current_node_x = current_node.position[0]
        grid_width = self.grid.grid_world_size[0]
        grid_height = self.grid.grid_world_size[1]

        # Check if neighbour to the right is valid
        if current_node_y + 1 <= grid_width - 1 \
                and self.grid.grid[current_node_x][current_node_y+1].walkable == True\
                and self.grid.grid[current_node_x][current_node_y+1].visited == False:
            return True
        # Check if neighbour to the left is valid
        elif current_node_y - 1 >= 0 \
                and self.grid.grid[current_node_x][current_node_y-1].walkable == True\
                and self.grid.grid[current_node_x][current_node_y-1].visited == False:
            return True
        # Check if neighbour above is valid
        elif current_node_x - 1 >= 0 \
                and self.grid.grid[current_node_x-1][current_node_y].walkable == True\
                and self.grid.grid[current_node_x-1][current_node_y].visited == False:
            return True
        # Check if neighbour below is valid
        elif current_node_x + 1 <= grid_height - 1 \
                and self.grid.grid[current_node_x+1][current_node_y].walkable == True\
                and self.grid.grid[current_node_x+1][current_node_y].visited == False:
            return True

        else:
            return False


    ######################################################
    # Breadth-First-Search Algorithm
    ######################################################
    def find_path_bfs(self):
        path_que = []
        visualization_stack = []

        start_node = node.Node(False, eval(self.start_node_position))
        target_node = node.Node(False, eval(self.target_node_position))
        current_node = start_node
        path_que.append(current_node)
        visualization_stack.append(current_node)

        while(path_que):
            # Mark current node as visited in the grid
            current_node = path_que.pop()

            # Check if target node found
            if current_node.position == target_node.position:
                visualization_stack.append(current_node)
                visualization_stack.reverse()
                current_node = visualization_stack[0]
                path_que = []
                while current_node.parent is not None:
                    path_que.append(current_node)
                    current_node = current_node.parent

                path_que.pop(0)
                visualization_stack.reverse()
                visualization_stack.pop(-1)

                return path_que, visualization_stack

            if current_node not in visualization_stack:
                visualization_stack.append(current_node)

            #Add up node
            if self.up_node_valid(current_node):
                current_direction = "up"
                observed_node = self.get_specific_neighbour(current_node, current_direction)
                observed_node.parent = current_node
                path_que.insert(0,observed_node)

                self.grid.grid[observed_node.position[0]][observed_node.position[1]].visited = True
                if current_node not in visualization_stack:
                    visualization_stack.append(observed_node)

            #Add right node
            if self.right_node_valid(current_node):
                current_direction = "right"
                observed_node = self.get_specific_neighbour(current_node, current_direction)
                observed_node.parent = current_node
                path_que.insert(0,observed_node)
                self.grid.grid[observed_node.position[0]][observed_node.position[1]].visited = True
                if current_node not in visualization_stack:
                    visualization_stack.append(observed_node)

            #Add down node
            if self.down_node_valid(current_node):
                current_direction = "down"
                observed_node = self.get_specific_neighbour(current_node, current_direction)
                observed_node.parent = current_node
                path_que.insert(0, observed_node)
                self.grid.grid[observed_node.position[0]][observed_node.position[1]].visited = True
                if current_node not in visualization_stack:
                    visualization_stack.append(observed_node)

            #Add left node
            if self.left_node_valid(current_node):
                current_direction = "left"
                observed_node = self.get_specific_neighbour(current_node, current_direction)
                observed_node.parent = current_node
                path_que.insert(0, observed_node)
                self.grid.grid[observed_node.position[0]][observed_node.position[1]].visited = True
                if current_node not in visualization_stack:
                    visualization_stack.append(observed_node)

        return path_que, visualization_stack

    ######################################################
    # Bridirectional Dijkstra Algorithm
    ######################################################
    # todo: To be implemented
    def find_path_bidirect_dijkstra(self):
        start_node = node.Node(False, eval(self.start_node_position))
        target_node = node.Node(False, eval(self.target_node_position))
        start_node.h_cost = get_h_cost(start_node, target_node)
