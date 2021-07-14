import numpy as np
from copy import deepcopy

class Puzzle:

    def __init__(self,matrix) -> None:
        self.matrix=matrix # the configuration of the puzzle

        # r and c are cordinates of the empty cell, that is the 0
        self.r,self.c=np.argwhere(self.matrix == 0)[0]

    def get_next_configurations(self):
        '''Return the new possible states reachable from the actual state'''
        up,down,left,right=self.check_mov() # check which are the possible moves
        new_puzzle=[]
        # Si può migliorare
        if up:
            p=Puzzle(deepcopy(self.matrix))
            p.mov_up()
            new_puzzle.append(('U',p))
        if down:
            p=Puzzle(deepcopy(self.matrix))
            p.mov_down()
            new_puzzle.append(('D',p))
        if left:
            p=Puzzle(deepcopy(self.matrix))
            p.mov_left()
            new_puzzle.append(('L',p))
        if right:
            p=Puzzle(deepcopy(self.matrix))
            p.mov_right()
            new_puzzle.append(('R',p))
        return new_puzzle

    def mov_up(self):
        if self._check_mov_up():
            tmp=self.matrix[self.r,self.c]
            # Swap the cells
            self.matrix[self.r,self.c]=self.matrix[self.r-1,self.c]
            self.matrix[self.r-1,self.c]=tmp
            self.r -= 1 # update the coordinate

    def mov_down(self):
        if self._check_mov_down():
            tmp=self.matrix[self.r,self.c]
            # Swap the cells
            self.matrix[self.r,self.c]=self.matrix[self.r+1,self.c]
            self.matrix[self.r+1,self.c]=tmp
            self.r += 1 # update the coordinate

    def mov_left(self):
        if self._check_mov_left():
            tmp = self.matrix[self.r, self.c]
            # Swap the cells
            self.matrix[self.r, self.c] = self.matrix[self.r, self.c-1]
            self.matrix[self.r, self.c-1] = tmp
            self.c -= 1 # update the coordinate

    def mov_right(self):
        if self._check_mov_right():
            tmp = self.matrix[self.r, self.c]
            # Swap the cells
            self.matrix[self.r, self.c] = self.matrix[self.r, self.c + 1]
            self.matrix[self.r, self.c + 1] = tmp
            self.c += 1 # update the coordinate

    def _check_mov_up(self):
        '''If r==0 I cannot swap the empty cell with an upper cell'''
        return not self.r==0

    def _check_mov_down(self):
        '''If r== last row I cannot swap the empty cell with an lower cell'''
        return not self.r == self.matrix.shape[0]-1

    def _check_mov_left(self):
        '''If c==0 I cannot swap the empty cell with a cell on the left'''
        return not self.c==0

    def _check_mov_right(self):
        '''If c== last column I cannot swap the empty cell with a cell on the right'''
        return not self.c == self.matrix.shape[1]-1

    def check_mov(self):
        '''Return 4 boolen values for each move, if it's true I can do that move
         :return
            up: Boolean
            down: Boolean
            left: Boolean
            right: Boolean
            '''
        up=self._check_mov_up()
        down=self._check_mov_down()
        left=self._check_mov_left()
        right=self._check_mov_right()
        return up,down,left,right

    def __str__(self):
        return str(self.matrix)

    def __eq__(self,p2):
        '''Return True if the 2 puzzle are equal'''
        return (self.matrix==p2.matrix).all()


if __name__=='__main__':

    m=np.array([[1,2,3],[4,5,8],[6,7,0]])
    p=Puzzle(m)
    p.mov_up()
    p.mov_left()
    p.mov_down()
    p.mov_right()
    print(p)

    mov=p.check_mov()
    print(mov)


