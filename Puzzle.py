import numpy as np
from copy import deepcopy


class Puzzle:
    goal = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    # goal = np.array([[0, 1, 2, 3], [4, 5, 6,7], [8, 9, 10,11],[12, 13, 14, 15]])

    def __init__(self, matrix) -> None:
        self.matrix = matrix  # the configuration of the puzzle
        # r and c are coordinates of the empty cell, that is the 0
        self.r, self.c = np.argwhere(self.matrix == 0)[0]

    def calculate_next_configurations(self):
        """Return the new possible states reachable from the actual state"""
        new_puzzle = []
        idx_last_row = self.matrix.shape[0] - 1
        idx_last_col = self.matrix.shape[1] - 1
        if not self.r == 0:  # Check if I can move the empty cell up
            p = Puzzle(deepcopy(self.matrix))
            p.move_up()
            new_puzzle.append(('U', p))
        if not self.r == idx_last_row:  # Check if I can move the empty cell down
            p = Puzzle(deepcopy(self.matrix))
            p.move_down()
            new_puzzle.append(('D', p))
        if not self.c == 0:  # Check if I can move the empty cell on the left
            p = Puzzle(deepcopy(self.matrix))
            p.move_left()
            new_puzzle.append(('L', p))
        if not self.c == idx_last_col:  # Check if I can move the empty cell on the right
            p = Puzzle(deepcopy(self.matrix))
            p.move_right()
            new_puzzle.append(('R', p))
        return new_puzzle

    def move_up(self):
        tmp = self.matrix[self.r, self.c]
        # Swap the cells
        self.matrix[self.r, self.c] = self.matrix[self.r - 1, self.c]
        self.matrix[self.r - 1, self.c] = tmp
        self.r -= 1  # update the coordinate

    def move_down(self):
        tmp = self.matrix[self.r, self.c]
        # Swap the cells
        self.matrix[self.r, self.c] = self.matrix[self.r + 1, self.c]
        self.matrix[self.r + 1, self.c] = tmp
        self.r += 1  # update the coordinate

    def move_left(self):
        tmp = self.matrix[self.r, self.c]
        # Swap the cells
        self.matrix[self.r, self.c] = self.matrix[self.r, self.c - 1]
        self.matrix[self.r, self.c - 1] = tmp
        self.c -= 1  # update the coordinate

    def move_right(self):
        tmp = self.matrix[self.r, self.c]
        # Swap the cells
        self.matrix[self.r, self.c] = self.matrix[self.r, self.c + 1]
        self.matrix[self.r, self.c + 1] = tmp
        self.c += 1  # update the coordinate

    def __str__(self):
        return str(self.matrix)

    def __eq__(self, p2):
        """Return True if the 2 puzzle are equal"""
        return np.all(self.matrix == p2.matrix)

    def goal_test(self):
        """Return True if the current state is equal to the goal state """
        return np.all(self.matrix == Puzzle.goal)

    def heuristic_function(self, heuristic_choice):
        """Return the heuristic value used during the A* search.
            heuristic_choice:
             'manhattan' -> manhattan distance
             'mis_tiles' -> number of misplaced tiles"""
        state = self.matrix
        goal = Puzzle.goal
        heuristic_value = 0
        numbers = np.unique(goal)
        for el in numbers[1::]:  # we consider only the tiles from 1 to 8, we don't consider the blank space
            ix, iy = np.argwhere(state == el)[0]
            ix_goal, iy_goal = np.argwhere(goal == el)[0]
            if heuristic_choice == 'manhattan':
                heuristic_value += np.abs(ix - ix_goal) + np.abs(iy - iy_goal)
            elif heuristic_choice == 'mis_tiles':
                if (ix != ix_goal) or (iy != iy_goal):
                    heuristic_value += 1
            else:
                raise ValueError("It's not defined any heuristic choice in heuristic function()")
        return heuristic_value

    # For this problem this method return always 1 because the move has unitary cost
    # if we change the problem this method will be overridden
    def get_path_cost(self):
        return 1




