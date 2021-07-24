import numpy as np
from copy import deepcopy

class Puzzle:

    goal=np.array([[0,1, 2], [3, 4, 5], [6, 7, 8]])

    def __init__(self,matrix,heuristic='manhattan') -> None:
        self.matrix=matrix # the configuration of the puzzle
        self.heuristic=heuristic
        # r and c are cordinates of the empty cell, that is the 0
        self.r,self.c=np.argwhere(self.matrix == 0)[0]

    def calculate_next_configurations(self):
        '''Return the new possible states reachable from the actual state'''
        new_puzzle=[]
        idx_last_row=self.matrix.shape[0]-1
        idx_last_col=self.matrix.shape[1]-1
        # Si può migliorare
        if not self.r==0: #Check if I can mov the empty cell up
            p=Puzzle(deepcopy(self.matrix))
            p.mov_up()
            new_puzzle.append(('U',p))
        if not self.r == idx_last_row : #Check if I can mov the empty cell down
            p=Puzzle(deepcopy(self.matrix))
            p.mov_down()
            new_puzzle.append(('D',p))
        if not self.c==0: #Check if I can mov the empty cell on the left
            p=Puzzle(deepcopy(self.matrix))
            p.mov_left()
            new_puzzle.append(('L',p))
        if not self.c == idx_last_col: #Check if I can mov the empty cell on the right
            p=Puzzle(deepcopy(self.matrix))
            p.mov_right()
            new_puzzle.append(('R',p))
        return new_puzzle

    def mov_up(self):
        tmp=self.matrix[self.r,self.c]
        # Swap the cells
        self.matrix[self.r,self.c]=self.matrix[self.r-1,self.c]
        self.matrix[self.r-1,self.c]=tmp
        self.r -= 1 # update the coordinate

    def mov_down(self):
        tmp=self.matrix[self.r,self.c]
        # Swap the cells
        self.matrix[self.r,self.c]=self.matrix[self.r+1,self.c]
        self.matrix[self.r+1,self.c]=tmp
        self.r += 1 # update the coordinate

    def mov_left(self):
        tmp = self.matrix[self.r, self.c]
        # Swap the cells
        self.matrix[self.r, self.c] = self.matrix[self.r, self.c-1]
        self.matrix[self.r, self.c-1] = tmp
        self.c -= 1 # update the coordinate

    def mov_right(self):
        tmp = self.matrix[self.r, self.c]
        # Swap the cells
        self.matrix[self.r, self.c] = self.matrix[self.r, self.c + 1]
        self.matrix[self.r, self.c + 1] = tmp
        self.c += 1 # update the coordinate


    def __str__(self):
        return str(self.matrix)

    def __eq__(self,p2):
        '''Return True if the 2 puzzle are equal'''
        return np.all(self.matrix==p2.matrix)

    def goal_test(self):
        '''Return True if the current state is equal to the goal state '''
        return np.all(self.matrix==Puzzle.goal)

    def heuristic_function(self):
        state = self.matrix
        goal = Puzzle.goal
        heuristic_value = 0
        numbers = np.unique(goal)
        for el in numbers[1::]:  # we consider only the tiles from 1 to 8, we don't consider the blank space
            ix, iy = np.argwhere(state == el)[0]
            ix_goal, iy_goal = np.argwhere(goal == el)[0]
            if self.heuristic == 'manhattan':
                heuristic_value += np.abs(ix - ix_goal) + np.abs(iy - iy_goal)
            elif self.heuristic == 'mis_tiles':
                if (ix != ix_goal) or (iy != iy_goal):
                    heuristic_value += 1
            else:
                raise ValueError("It's not defined any heuristic choice in heuristic function()")
        return heuristic_value

if __name__=='__main__':
    state=np.array([[7,2,4], [5,0,6], [8,3,1]])
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    p = Puzzle(state)
    print(p.goal_test())
    d=p.heuristic_function(choice='mis_tiles')
    d2 = p.heuristic_function(choice='manhattan')
    print(d,d2)


    # from time import time
    #
    # s = time()
    # m = np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])
    # p = Puzzle(m)
    # #p2 = Puzzle(np.array([[1, 2, 3], [4, 5, 8], [6, 7, 0]]))
    # # print(p == p2)
    # X = p.calculate_next_configurations()
    # print('Initial state')
    # print(p.matrix)
    # for x in X:
    #     mov, pp = x
    #     print(mov)
    #     print(pp.matrix)
    #
    # e = time()
    # print(e - s)





