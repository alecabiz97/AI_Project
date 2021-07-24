import numpy as np
from Node import *
from Puzzle import *
from Strategy import *
from Tree import *

if __name__ == '__main__':
    state = np.array([[1, 2, 3], [5, 6, 0], [4, 7, 8]])
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    p = Puzzle(state, goal)
    n=Node(p)
    tree=Tree(n,strategy=BreadthFirst())
    sol=tree.resolve()
    print(sol)


