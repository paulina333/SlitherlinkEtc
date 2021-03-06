import numpy as np

EMPTY = 0
TANK = 1
HOUSE = 2
DIRS = {'down': (-1, 0), 'up': (1, 0), 'left': (0, -1), 'right': (0, 1)}
OUT_OF_BOARD = '.'


class Board:

    def __init__(self):
        self.nums = []
        self.upper = []
        self.left = []
        self.height = 0
        self.width = 0
        self.houses = []
        self.solutions = 0

    def read(self, file_name):
        with open(file_name, 'r') as fh:
            self.width, self.height = map(int, fh.readline().split())
            self.upper = [0] + list(map(int, fh.readline().split())) + [0]
            self.left = [0] + list(map(int, fh.readline().split())) + [0]
            NUMS = [[OUT_OF_BOARD] * (self.width + 2)]
            for i in range(self.height):
                NUMS += [[OUT_OF_BOARD] + [int(x) for x in
                         fh.readline().split()] + [OUT_OF_BOARD]]
        NUMS += [[OUT_OF_BOARD] * (self.width + 2)]

        self.nums = NUMS

    def print_grid(self):
        for row in self.nums:
            print(' '.join(map(str, row)))

    def find_houses(self):
        hh = []
        for i in range(self.height + 2):
            for j in range(self.width + 2):
                if self.nums[i][j] == HOUSE:
                    hh.append([i, j])
        return hh


def check_location_is_safe(board, row, col):
    Dr = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    for direct in Dr:
        i = direct[0]
        j = direct[1]
        if board.nums[row + i][col + j] == TANK:
            return False
    return True


def how_many_tanks_row(board, row):  # row = 1,...
    now = 0
    for el in range(1, board.width + 1):
        if board.nums[row][el] == TANK:
            now += 1
    return now


def how_many_tanks_col(board, col):  # col = 1,...
    now = 0
    for el in range(1, board.height + 1):
        if board.nums[el][col] == TANK:
            now += 1
    return now


def is_row_ok(board, row):

    return board.left[row] >= how_many_tanks_row(board, row)


def is_col_ok(board, col):

    return board.upper[col] >= how_many_tanks_col(board, col)


def is_ok(board):
    return all([is_row_ok(board, row) for row in range(1, board.height + 1)] +
               [is_col_ok(board, col) for col in range(1, board.width + 1)])


def is_identical(board1, board2):
    if len(board1) != len(board2):
        return False
    if len(board1) == 0:
        if len(board2) == 0:
            return True
        if len(board2) > 0:
            return False
    else:
        for row in range(len(board1)):
            for col in range(len(board1)):
                if board1[row][col] != board2[row][col]:
                    return False
    return True


def solve(board, solvedBoard, i=0):

    if i == len(board.houses):
        if solvedBoard is None:
            return True
        if is_identical(board.nums, solvedBoard):
            return False
        else:
            return True

    choice = board.houses[i]

    for direction in DIRS.values():
        row, col = choice[0] + direction[0], choice[1] + direction[1]
        if board.nums[row][col] == EMPTY:
            if check_location_is_safe(board, row, col) and is_ok(board):
                board.nums[row][col] = TANK
                if is_ok(board):
                    if solve(board, solvedBoard, i + 1):
                        return True
            board.nums[row][col] = EMPTY
    return False

if __name__ == '__main__':

    print("solve")

    T = Board()
    T.read('architekt2.txt')

    T.houses = T.find_houses()

    solve(T, None, i=0)
    T.print_grid()
    print('ARE THERE MORE?')
    B = Board()
    B.read('architekt2.txt')
    B.houses = B.find_houses()

    if solve(B, T.nums, i=0) is False:
        print('no, just this one')
    else:
        for i in range(B.height + 2):
            print(' '.join(map(str, B.nums[i])))

