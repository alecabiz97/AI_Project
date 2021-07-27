import numpy as np
from Node import *
from Puzzle import *
from Strategy import *
from Tree import *

if __name__ == '__main__':
    state = np.array([[1, 2, 0],
                      [3, 4, 5],
                      [6, 7, 8]])
    p = Puzzle(state,heuristic='manhattan')
    n=Node(p)
    for strategy in [AStarStrategy(),BreadthFirst(),DepthFirst()]:
        print(strategy.__class__.__name__)
        tree=Tree(n,strategy=strategy)
        sol=tree.resolve()
        moves, depth=sol
        print('  Moves to do:',moves)
        print('  Depth of the solution:',depth)
        print('  Number of nodes:',len(tree.expanded_nodes))


