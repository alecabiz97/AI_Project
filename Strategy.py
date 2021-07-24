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
            n = tree.new_nodes.pop(0) # I select the node from the top of the fringe
            if n not in tree.expanded_nodes: # Check if I have already expand that node
                if n.puzzle.goal_test():
                    return self.solution_found(n,tree) # return the solution
                else:
                    n.expand() # n.expand() fills the list n.child
                    tree.number_of_nodes += 1 # the number of the tree's nodes is the number of expanded nodes
                    tree.new_nodes.extend(n.child) # the new nodes are put at the end of the fringe
                    tree.expanded_nodes.append(n)

# Da rivedere
class AStarStrategy(Strategy):


    def resolve(self, tree):
        while (tree._sol == False):
            if not tree.new_nodes: # if tree.new_nodes is empty
                print('Nessuna soluzione')
                return -1
            else:
                n = tree.new_nodes.pop(0)
                if n not in tree.expanded_nodes:
                    if n.puzzle.goal_test():
                        return self.solution_found(n,tree)
                    else:
                        n.expand()
                        for nc in n.child:
                            nc.total_cost= nc._path_cost + nc.puzzle.heuristic_function()
                        tree.new_nodes.extend(n.child)
                        tree.new_nodes=self.sort_nodes(tree.new_nodes)

                        #tree.new_nodes=[n for n in tree.new_nodes if n._depth < 25]

                        tree.expanded_nodes.append(n)
                        tree.number_of_nodes += 1
                        #print((len(tree.expanded_nodes),n._depth))

  
    def path_cost_function(self,node):
        return node._path_cost

    def sort_nodes(self,nodes):
        dists=[n.total_cost for n in nodes]
        sorted_index=np.argsort(dists)
        sorted_nodes=[nodes[i] for i in sorted_index]
        return sorted_nodes


# Non funziona
class DepthFirst(Strategy):

    def resolve(self, tree):
        while (tree._sol == False):
            n = tree.new_nodes.pop(0)
            if n not in tree.expanded_nodes:
                if n == tree.goal:
                    return self.solution_found(n,tree)
                else:
                    n.expand()
                    #tmp=n.child
                    #tmp.extend(tree.new_nodes)
                    #tree.new_nodes=tmp
                    for el in n.child:
                        tree.new_nodes.insert(0,el)
                    tree.expanded_nodes.append(n)
                    tree.number_of_nodes += 1

