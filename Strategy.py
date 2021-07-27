from abc import ABC, abstractmethod
import numpy as np
from Tree import *

class Strategy(ABC):
    @abstractmethod
    def resolve(self,tree):
        pass

    def solution_found(self,n_sol,tree):
        '''Return the solution and fills the tree with the solution and the
            depth where was found the solution'''
        #print('Soluzione trovata')
        tree._sol = True
        tree.solution = n_sol.calculate_path()
        tree.depth_solution = n_sol._depth
        return tree.solution, tree.depth_solution


class BreadthFirst(Strategy):

    def resolve(self, tree):
        while (tree._sol == False):
            if not tree.new_nodes:  # if tree.new_nodes is empty
                print('No solution')
                return (None,None)
            else:
                n = tree.new_nodes.pop(0) # I select the node from the top of the fringe
                if n not in tree.expanded_nodes: # Check if I have already expand that node
                    if n.puzzle.goal_test():
                        return self.solution_found(n,tree) # return the solution
                    else:
                        n.expand() # n.expand() fills the list n.child
                        tree.number_of_nodes += 1 # the number of the tree's nodes is the number of expanded nodes
                        tree.new_nodes.extend(n.child) # the new nodes are put at the end of the fringe
                        tree.expanded_nodes.append(n)


class AStarStrategy(Strategy):

    def resolve(self, tree):
        while (tree._sol == False):
            if not tree.new_nodes: # if tree.new_nodes is empty
                print('No solution')
                return (None,None)
            else:
                n = tree.new_nodes.pop(0)
                if n not in tree.expanded_nodes:
                    if n.puzzle.goal_test():
                        return self.solution_found(n,tree)
                    else:
                        n.expand()
                        for nc in n.child:
                            nc.total_cost= nc._path_cost + nc.puzzle.heuristic_function() # Problema con path cost
                        tree.new_nodes.extend(n.child)
                        tree.new_nodes=self.sort_nodes(tree.new_nodes)

                        tree.expanded_nodes.append(n)
                        tree.number_of_nodes += 1

    def sort_nodes(self,nodes):
        dists=[n.total_cost for n in nodes]
        sorted_index=np.argsort(dists)
        sorted_nodes=[nodes[i] for i in sorted_index]
        return sorted_nodes


class DepthFirst(Strategy):

    def __init__(self,max_depth=0):
        self.max_depth=max_depth

    def resolve(self, tree):
        # n = tree.new_nodes.pop(0)
        # node_solution=DepthFirst.dfs(tree,n)
        # return self.solution_found(node_solution, tree)

        while (tree._sol == False):
            if not tree.new_nodes:  # if tree.new_nodes is empty
                print('No solution')
                return (None,None)
            else:
                n = tree.new_nodes.pop(0)
                if n not in tree.expanded_nodes and (n._depth<self.max_depth or self.max_depth==0):
                    if n.puzzle.goal_test():
                        return self.solution_found(n,tree)
                    else:
                        n.expand()
                        for el in n.child:
                            tree.new_nodes.insert(0,el)
                        tree.expanded_nodes.append(n)
                        tree.number_of_nodes += 1
                else:
                    DepthFirst.memory_management(n,tree)
                    # eliminare n dalla lista dei figli del nodo padre
                    # se il padre è senza figli rimuovo il padre e controllo il nonno
                    # provare metodo ricorsivo
                    # dfs(n,tree):
                        # se n non ha padre
                            # return
                        # eliminare n dalla lista dei figli del nodo padre
                        # controllare che il padre non abbia figli
                            # eliminare il padre da tree.expanded_nodes
                            # dfs(parentOfn,tree)
                        # return

    @staticmethod
    def memory_management(n,tree):
        # se n non ha padre
        # return
        parent=n.parent
        if parent is None: # Check if n is the root
            return True
        else:
            parent.child.remove(n) # eliminare n dalla lista dei figli del nodo padre
            if not parent.child:
                tree.expanded_nodes.remove(parent)
                DepthFirst.memory_management(parent,tree)

            # controllare che il padre non abbia figli
                 # eliminare il padre da tree.expanded_nodes
                 # dfs(parentOfn,tree)
            # return





