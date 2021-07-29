from Node import *
from Puzzle import *
from Strategy import *
from Tree import *
from IPython.display import display
import pandas as pd
from tabulate import tabulate


if __name__ == '__main__':

    # state = np.array([[1, 5, 2, 3],
    #                   [4, 6, 10, 7],
    #                   [8, 0, 11, 15],
    #                   [12, 9, 13, 14]])
    # states = [np.array([[1, 2, 5],
    #                     [3, 4, 0],
    #                     [6, 7, 8]]),
    #           np.array([[3, 1, 2],
    #                     [6, 0, 8],
    #                     [7, 5, 4]]),
    #           np.array([[4, 0, 1],
    #                     [3, 6, 2],
    #                     [7, 8, 5]])]
    states = [np.array([[1, 2, 5],
                        [3, 4, 0],
                        [6, 7, 8]])]
    # creating a DataFrame 'Strategy': [],
    dict = {'Depth': [],
            'Heuristic':[],
            'Branching Factor': [],
            'Moves':[]}
    index =[]
    for state in states:
        print(state)
        for strategy in [AStarStrategy('manhattan'), AStarStrategy('mis_tiles'), BreadthFirst(),
                         DepthFirst(max_depth=10)]:
            print(strategy.__class__.__name__)
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
            dict['Depth'].append(depth)
            #dict['Strategy'].append(strategy.__class__.__name__)
            index.append(strategy.__class__.__name__)
            dict['Heuristic'].append(strategy.heuristic_choice)
            dict['Branching Factor'].append(tree.calculate_branching_factor())
            dict['Moves'].append(moves)

    #index=dict['Strategy']
    #del dict['Strategy']
    df = pd.DataFrame(dict,index=index)

    # displaying the DataFrame
    #display(df)
    print(tabulate(df, headers='keys', tablefmt='psql'))