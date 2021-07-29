import pandas as pd
from tabulate import tabulate

from Node import *
from Puzzle import *
from Strategy import *
from Tree import *

if __name__ == '__main__':

    # state = np.array([[1, 5, 2, 3],
    #                   [4, 6, 10, 7],
    #                   [8, 0, 11, 15],
    #                   [12, 9, 13, 14]])
    states = [np.array([[1, 2, 5],
                        [3, 4, 0],
                        [6, 7, 8]])]

    # creating a DataFrame
    dict = {'Heuristic': [],
            'Branching\n Factor': [],
            'Depth': [],
            'Expanded\n Nodes': [],
            'Nodes in\n Memory': [],
            'Moves': []}

    index = []
    for state in states:
        print('Initial Configuration:\n', state)
        for strategy in [BreadthFirst(),
                         DepthFirst(max_depth=5), AStarSearch('manhattan'), AStarSearch('mis_tiles')]:
            p = Puzzle(state)
            n = Node(p)
            tree = Tree(n, strategy=strategy)
            sol = tree.resolve()
            moves, depth = sol
            # print('  Moves to do:', moves)
            # print('  Depth of the solution:', depth)
            # print('  Number of nodes in memory:', len(tree.expanded_nodes) + len(tree.leaves))
            # print('  Total number of nodes expanded:', tree.number_of_nodes)
            # print('  Average branching factor', tree.calculate_branching_factor())
            index.append(strategy.__class__.__name__)
            dict['Heuristic'].append(strategy.heuristic_choice)
            dict['Branching\n Factor'].append(tree.calculate_branching_factor())
            dict['Depth'].append(depth)
            dict['Expanded\n Nodes'].append(tree.number_of_nodes)
            dict['Nodes in\n Memory'].append(len(tree.expanded_nodes) + len(tree.leaves))
            dict['Moves'].append(moves)

    df = pd.DataFrame(dict, index=index)
    print(tabulate(df, headers='keys', tablefmt='psql'))
