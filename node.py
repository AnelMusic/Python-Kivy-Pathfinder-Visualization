
class Node:
    """ A set of nodes is used to define a nxm 2D world, where n is the number of rows
        and m is the number of columns

        Attributes:
            walkable    The boolean value defines weather a node can be conquered or must be avoided.
            position    The nodes (x,y) position in a 2D grid.
            g_cost      The cost that it takes to reach the node from the starting node.
            h_cost      The cost that it takes to teach the target node from the current node (Heuristic).
            parent      The parent node from which the current node has originated from, which is needed to
                        retrace the found path.
    """

    def __init__(self, walkable = False, position = None):
        self.walkable = walkable
        self.position = position # [x,y]
        self.visited = False
        self.g_cost = 0.0
        self.h_cost = 0.0
        self.parent = None

    def get_f_cost(self):
        return self.h_cost+self.g_cost

    def get_g_cost(self):
        return self.g_cost


    # Check equality of all attributes with dunder method (convenient way for caparing nodes)
    def __eq__(self, other) :
        return self.__dict__ == other.__dict__