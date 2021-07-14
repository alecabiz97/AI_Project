from Puzzle import Puzzle
import numpy as np
from copy import deepcopy, copy

class Node:
    id=-1

    def __init__(self,puzzle=None,parent=None,child=[],depth=0) -> None:
        self.puzzle = copy(puzzle) # the state of that node
        self.parent = parent # the parent node
        self.parent_mov='' # the move has been done from the parent node
        self.child = copy(child) # list of all the child nodes
        self._path_cost=0 # cost of the path from the root to this node
        self._heuristic_dist=None # heuristic function
        self._heuristic_value=None # heuristic value
        self._depth=depth # depth of this node
        Node.id += 1
        self._id=copy(Node.id) # node id, the first node (root) has id=0

    def expand(self):
        '''Expand the node, so it fills the list self.child'''
        p_child=self.puzzle.get_next_configurations()
        for mov,p in p_child:
            n=Node(puzzle=p,parent=self,depth=self._depth+1)
            n.parent_mov = mov
            n._path_cost += self._path_cost + 0 # QUESTO DEVE ESSERE MODIFICATO
            self.child.append(n)

    # First version
    # def expand2(self):
    #     up,down,left,right=self.puzzle.check_mov()
    #     # Si può migliorare
    #     if up:
    #         p=Puzzle(deepcopy(self.puzzle.matrix))
    #         p.mov_up()
    #         n=Node(puzzle=p,parent=self,depth=self._depth+1)
    #         n.parent_mov='U'
    #         self.child.append(n)
    #     if down:
    #         p=Puzzle(deepcopy(self.puzzle.matrix))
    #         p.mov_down()
    #         n = Node(puzzle=p, parent=self, depth=self._depth + 1)
    #         n.parent_mov = 'D'
    #         self.child.append(n)
    #     if left:
    #         p=Puzzle(deepcopy(self.puzzle.matrix))
    #         p.mov_left()
    #         n = Node(puzzle=p, parent=self, depth=self._depth + 1)
    #         n.parent_mov = 'L'
    #         self.child.append(n)
    #     if right:
    #         p=Puzzle(deepcopy(self.puzzle.matrix))
    #         p.mov_right()
    #         n = Node(puzzle=p, parent=self, depth=self._depth + 1)
    #         n.parent_mov = 'R'
    #         self.child.append(n)

    def calculate_path(self):
        '''Return the moves from the root node to the target'''
        path=[]
        # if self.parent==None it means that I am the root node because
        # I don't have a parent
        while(self.parent is not None):
            path.append(self.parent_mov)
            self=self.parent
        # Reverse the order of the moves from target -> root to root -> target
        return path[::-1]

    def __eq__(self,node2):
        '''Return true if the state in the two nodes are the same'''
        return self.puzzle==node2.puzzle

if __name__=='__main__':
    m = np.array([[1, 2, 3], [4, 5, 8], [6, 7, 0]])
    target=Puzzle(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]))
    p = Puzzle(m)
    n1,n2=Node(p),Node(target)

    l1=[deepcopy(n1),n2]
    l2=[n2]

    if n1 in l1:
        print('ciao')