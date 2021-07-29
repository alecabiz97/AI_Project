class Tree:

    def __init__(self, root, strategy=None) -> None:
        self.root = root  # Root node
        self.strategy = strategy  # Search algorithm strategy
        self.leaves = [root]  # list of leaves that will be expanded
        self.number_of_nodes = 0
        self.expanded_nodes = []  # list of expanded nodes
        self.sol = False  # if it's True I found a solution
        self.solution = None  # list of action to do to reach the goal
        self.depth_solution = None  # depth of the goal node

    def resolve(self):
        return self.strategy.resolve(self)

    def calculate_branching_factor(self):
        """Return the branching factor"""
        if self.expanded_nodes:
            b = 0
            for n in self.expanded_nodes:
                b += len(n.children)
            return round(b / len(self.expanded_nodes), 3)
        else:
            raise ZeroDivisionError('tree.expanded node is empty')
