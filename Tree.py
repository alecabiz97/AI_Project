from Puzzle import Puzzle
from Node import Node
import numpy as np
from Strategy import *



class Tree:

    def __init__(self,root,strategy=None) -> None:
        self.root = root # Root node
        #self.target = target # Target node
        self.strategy = strategy # Search algorithm strategy
        self.new_nodes=[root] # list of the nodes not already expanded
        self.number_of_nodes=0
        self.expanded_nodes=[] # list of expanded node
        self._sol=False # if it's True I found a solution
        self.solution=None # list of action to do to reach the target
        self.depth_solution=None # depth of the target node

    def resolve(self):
        return self.strategy.resolve(self)


def test(X,X_goal,strategy):
    p = Puzzle(X)
    p_goal = Puzzle(X_goal)
    t = Tree(Node(p), Node(p_goal), strategy)
    sol = t.resolve()

    # d = {'U': 'up ', 'D': 'down ', 'L': 'left ', 'R': 'right '}
    # sol2 = ''
    # for s in sol:
    #     sol2 += d[s]
    print('Soluzione: {}'.format(t.solution))
    print('Number of nodes expanded: {}'.format(t.number_of_nodes))
    print('Depth of solution: {}\n'.format(t.depth_solution))


if __name__=='__main__':

    X=np.array([[1, 2, 3], [4, 5, 6], [0, 7, 8]])
    X_goal=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    #
    #
    strategy=BreadthFirst()

    test(X, X_goal, strategy)








