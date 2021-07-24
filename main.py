import numpy as np
from Node import *
from Puzzle import *
from Strategy import *
from Tree import *

if __name__ == '__main__':
    state = np.array([[1, 5, 4],
                      [7, 2, 8],
                      [0, 3, 6]])
    p = Puzzle(state,heuristic='manhattan')
    n=Node(p)
    for strategy in [AStarStrategy(),BreadthFirst()]:
        print(strategy.__class__.__name__)
        tree=Tree(n,strategy=strategy)
        sol=tree.resolve()
        print(sol)
        print(tree.number_of_nodes)


