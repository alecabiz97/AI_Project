from abc import ABC, abstractmethod
import numpy as np
from Tree import *


class Strategy(ABC):
    @abstractmethod
    def __init__(self, heuristic_choice=None, max_depth=0):
        self.heuristic_choice = heuristic_choice  # It's a string
        self.max_depth = max_depth

    @abstractmethod
    def resolve(self, tree):
        pass

    def solution_found(self, n_sol, tree):
        """Return the solution and fills the tree with the solution and the
            depth where the solution was found
            :param
                n_sol -> solution node
                tree -> tree
            :return
                tree.solution -> list of moves from the root to the goal
                tree.depth_solution -> depth of the goal node"""
        tree.sol = True
        tree.solution = n_sol.calculate_path()
        tree.depth_solution = n_sol.depth
        return tree.solution, tree.depth_solution


class BreadthFirst(Strategy):

    def __init__(self, heuristic_choice=None, max_depth=0):
        super().__init__(heuristic_choice, max_depth)

    def resolve(self, tree):
        while tree.sol == False:
            if not tree.leaves:  # if tree.leaves is empty
                print('No solution')
                return None, None
            else:
                n = tree.leaves.pop(0)  # I select the node from the top of the fringe
                if n not in tree.expanded_nodes:  # Check if I have already expanded that node
                    if n.puzzle.goal_test():  # Check if n contains the goal state
                        return self.solution_found(n, tree)  # return the solution
                    else:
                        n.expand()  # n.expand() fills the list n.children
                        tree.number_of_nodes += 1  # the number of the tree's nodes is the number of expanded nodes
                        tree.leaves.extend(n.children)  # the new nodes are put at the end of the fringe
                        tree.expanded_nodes.append(n)


class AStarSearch(Strategy):

    def __init__(self, heuristic_choice=None, max_depth=0):
        super().__init__(heuristic_choice, max_depth)

    def resolve(self, tree):
        #print('Heuristic used ->', self.heuristic_choice)
        while tree.sol == False:
            if not tree.leaves:  # if tree.leaves is empty
                print('No solution')
                return None, None
            else:
                n = tree.leaves.pop(0)  # I select the node from the top of the fringe
                if n not in tree.expanded_nodes:
                    if n.puzzle.goal_test():
                        return self.solution_found(n, tree)
                    else:
                        n.expand()
                        # For each child node in n.children I calculate the total cost f = g + h
                        for nc in n.children:
                            nc.total_cost = nc.path_cost + nc.puzzle.heuristic_function(self.heuristic_choice)
                        tree.leaves.extend(n.children)
                        # Sorting the leaves based on the total_cost,from the smallest to the biggest
                        tree.leaves = self.sort_nodes(tree.leaves)
                        tree.expanded_nodes.append(n)
                        tree.number_of_nodes += 1

    def sort_nodes(self, nodes):
        """Return the list of nodes sorted with respect to the smallest total cost"""
        dists = [n.total_cost for n in nodes]
        sorted_index = np.argsort(dists)
        sorted_nodes = [nodes[i] for i in sorted_index]
        return sorted_nodes


class DepthFirst(Strategy):
    def __init__(self, heuristic_choice=None, max_depth=0):
        # For the DepthFirst limited, if it's 0 is DepthFirst without limitation of depth
        super().__init__(heuristic_choice, max_depth)

    def resolve(self, tree):
        while tree.sol == False:
            if not tree.leaves:  # if tree.leaves is empty
                print('No solution')
                return None, None
            else:
                n = tree.leaves.pop(0)  # I select the node from the top of the fringe
                if n not in tree.expanded_nodes and (n.depth < self.max_depth or self.max_depth == 0):
                    if n.puzzle.goal_test():  # Check if n contains the goal state
                        return self.solution_found(n, tree)
                    else:
                        n.expand()
                        for el in n.children:
                            # I insert the new leaf at the beginning of the list according to the DFS logic
                            tree.leaves.insert(0, el)
                        tree.expanded_nodes.append(n)
                        tree.number_of_nodes += 1
                else:
                    # Elimination of the nodes that didn't reach the solution
                    DepthFirst.memory_management(n, tree)

    @staticmethod
    def memory_management(n, tree):
        parent = n.parent
        if parent is None:  # Check if n is the root
            return True
        else:
            parent.children.remove(n)  # Delete n from the list of the parent's children
            if not parent.children:  # Check if parent has other children
                # If parent doesn't have children I delete the parent
                tree.expanded_nodes.remove(parent)
                # I call recursive the function on the parent
                DepthFirst.memory_management(parent, tree)
