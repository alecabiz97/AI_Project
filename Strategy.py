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
        return tree.solution


class BreadthFirst(Strategy):

    def resolve(self, tree):
        while (tree._sol == False):
            n = tree.new_nodes.pop(0) # I select the node from the top of the fringe
            if n not in tree.expanded_nodes: # Check if I have already expand that node
                if n == tree.target:
                    return self.solution_found(n,tree) # return the solution
                else:
                    n.expand() # n.expand() fills the list n.child
                    tree.number_of_nodes += 1 # the number of the tree's nodes is the number of expanded nodes
                    tree.new_nodes.extend(n.child) # the new nodes are put at the end of the fringe
                    tree.expanded_nodes.append(n)

# Da rivedere
class AStarStrategy(Strategy):

    def __init__(self) -> None:
        self.heuristic_function = self._distance_rubik

    def set_heuristic_function(self,heur_f):
        self.heuristic_function=heur_f

    def resolve(self, tree):
        while (tree._sol == False):
            if not tree.new_nodes: # if tree.new_nodes is empty
                print('Nessuna soluzione')
                return -1
            else:
                n = tree.new_nodes.pop(0)
                if n not in tree.expanded_nodes:
                    if n == tree.target:
                        return self.solution_found(n,tree)
                    else:
                        n.expand()
                        for nc in n.child:
                            nc._heuristic_dist= self.heuristic_function(nc,tree.target)
                            nc._heuristic_value= nc._path_cost + nc._heuristic_dist
                        tree.new_nodes.extend(n.child)
                        tree.new_nodes=self.sort_nodes(tree.new_nodes)

                        tree.new_nodes=[n for n in tree.new_nodes if n._depth < 25]

                        tree.expanded_nodes.append(n)
                        tree.number_of_nodes += 1
                        print((len(tree.expanded_nodes),n._depth,n._heuristic_dist))

    def _distance_manhattan(self,node,node_target):
        X=node.puzzle.matrix
        X_target=node_target.puzzle.matrix
        d=0
        for el in X_target.flatten():
            ix,iy=np.argwhere(X==el)[0]
            ixt, iyt = np.argwhere(X_target == el)[0]
            d += np.abs(ix-ixt) + np.abs(iy-iyt)
        return d

    def _distance_rubik(self,node,node_target):
        cub=node.puzzle
        cub_target=node_target.puzzle
        d=0
        faces=cub.get_faces()
        faces_target=cub_target.get_faces()
        for f,f_target in zip(faces,faces_target):
            d += (f != f_target).sum()
        return d

    def path_cost_function(self,node):
        return node._path_cost

    def sort_nodes(self,nodes):
        dists=[n._heuristic_value for n in nodes]
        sorted_index=np.argsort(dists)
        sorted_nodes=[nodes[i] for i in sorted_index]
        return sorted_nodes


# Non funziona
class DepthFirst(Strategy):

    def resolve(self, tree):
        while (tree._sol == False):
            n = tree.new_nodes.pop(0)
            if n not in tree.expanded_nodes:
                if n == tree.target:
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

# Non funziona
class AStarBiderectionalStrategy(Strategy):

    def __init__(self) -> None:
        self.heuristic_function = self._distance_rubik

    def set_heuristic_function(self,heur_f):
        self.heuristic_function=heur_f


    def solution_found2(self,n_sol1,n_sol2,tree):
        tree._sol = True
        sol=n_sol1.calculate_path()
        sol.extend(n_sol2.calculate_path())
        tree.solution = sol
        #tree.depth_solution = n_sol._depth
        return tree.solution


    def resolve(self, tree):
        new_nodes2,expanded_nodes2=[deepcopy(tree.target)],[]
        target2=deepcopy(tree.root)
        cnt = 0
        while (tree._sol == False):
            if not tree.new_nodes: # if tree.new_nodes is empty
                print('Nessuna soluzione')
                return -1
            else:
                n = tree.new_nodes.pop(0)
                if n not in tree.expanded_nodes:
                    #if n == tree.target:
                    #    return self.solution_found(n,tree)
                    if n in expanded_nodes2:
                        #idx=expanded_nodes2[expanded_nodes2==n]
                        #n2=expanded_nodes2[idx]
                        n2 = [x for x in expanded_nodes2 if x == n][0]
                        print('Soluzione trovata1')
                        return self.solution_found2(n,n2, tree)
                    else:
                        n.expand()
                        for nc in n.child:
                            # Normal search
                            nc._heuristic_dist= self.heuristic_function(nc,tree.target)
                            nc._heuristic_value= nc._path_cost + nc._heuristic_dist
                        tree.new_nodes.extend(n.child)
                        tree.new_nodes = [n for n in tree.new_nodes if n._depth < 25]
                        tree.new_nodes=self.sort_nodes(tree.new_nodes)
                        tree.expanded_nodes.append(n)
                        tree.number_of_nodes += 1

                n2 = new_nodes2.pop(0)
                if n2 not in expanded_nodes2:
                    if n2 == target2:
                        print('Soluzione trovata')
                        return 1
                    elif n2 in tree.expanded_nodes:
                        #idx = tree.expanded_nodes[tree.expanded_nodes == n2]
                        #n = tree.expanded_nodes[idx]
                        n=[x for x in tree.expanded_nodes if x==n2][0]
                        print('Soluzione trovata2')
                        return self.solution_found2(n, n2, tree)
                    else:
                        n2.expand()
                        #for nc2 in n2.child:
                            # Reverse search
                            #nc2._heuristic_dist = self.heuristic_function(nc2, target2)
                            #nc2._heuristic_value = nc2._path_cost + nc2._heuristic_dist
                        # Reverse
                        new_nodes2.extend(n2.child)
                        #new_nodes2 = self.sort_nodes(new_nodes2)
                        expanded_nodes2.append(n2)

                print(((len(tree.expanded_nodes), n._depth), (len(expanded_nodes2), n2._depth)))
                cnt+=1
                if cnt==2000:
                    for el1 in tree.expanded_nodes:
                        for el2 in expanded_nodes2:
                            if el1==el2:
                                print('Soluzione')
                                return 1
                    cnt=0

    def _distance_manhattan(self,node,node_target):
        X=node.puzzle.matrix
        X_target=node_target.puzzle.matrix
        d=0
        for el in X_target.flatten():
            ix,iy=np.argwhere(X==el)[0]
            ixt, iyt = np.argwhere(X_target == el)[0]
            d += np.abs(ix-ixt) + np.abs(iy-iyt)
        return d

    def _distance_rubik(self,node,node_target):
        cub=node.puzzle
        cub_target=node_target.puzzle
        d=0
        faces=cub.get_faces()
        faces_target=cub_target.get_faces()
        for f,f_target in zip(faces,faces_target):
            d += (f != f_target).sum()
        return d


    def _distance_rubik2(self,node,node_target):
        cub=node.puzzle
        cub_target=node_target.puzzle
        d=0
        faces=cub.get_faces()
        faces_target=cub_target.get_faces()
        n_faces=len(faces)
        for f,f_target in zip(faces,faces_target):
            d += (f != f_target).sum()
        return d

    def path_cost_function(self,node):
        return node._path_cost

    def sort_nodes(self,nodes):
        dists=[n._heuristic_value for n in nodes]
        sorted_index=np.argsort(dists)
        sorted_nodes=[nodes[i] for i in sorted_index]
        return sorted_nodes