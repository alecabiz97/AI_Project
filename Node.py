from copy import copy


class Node:
    id = -1

    def __init__(self, puzzle=None, parent=None, children=[], depth=0) -> None:
        self.puzzle = copy(puzzle)  # the state of that node
        self.parent = parent  # the parent node
        self.parent_move = ''  # the move has been done from the parent node
        self.children = copy(children)  # list of all the children nodes
        self.path_cost = 0  # cost of the path from the root to this node
        self.total_cost = 0  # path cost + heuristic value
        self.depth = depth  # depth of this node
        Node.id += 1
        self.id = copy(Node.id)  # node id, the first node (root) has id=0

    def expand(self):
        """Expand the node, so it fills the list self.children"""
        p_children = self.puzzle.calculate_next_configurations()  # ex p_children -> [('U',new_puzzle),...]
        for move, p in p_children:
            n = Node(puzzle=p, parent=self, depth=self.depth + 1)
            n.parent_move = move
            n.path_cost += self.path_cost + n.puzzle.get_path_cost()  # in this case getpath_cost() is always 1
            self.children.append(n)

    def calculate_path(self):
        """Return the moves from the root node to the target"""
        path = []
        # if self.parent==None it means that I am the root node because
        # I don't have a parent
        while self.parent is not None:
            path.append(self.parent_move)
            self = self.parent
        # Reverse the order of the moves from target -> root to root -> target
        return path[::-1]

    def __str__(self):
        return str(self.puzzle)

    def __eq__(self, node2):
        """Return true if the state in the two nodes are the same"""
        return self.puzzle == node2.puzzle
