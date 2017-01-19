import numpy as np
import domki

EMPTY = 0
TANK = 1
HOUSE = 2
DIRS = {'down': (-1, 0), 'up': (1, 0), 'left': (0, -1), 'right': (0, 1)}
OUT_OF_BOARD = '.'


class Board:

    def __init__(self, width, height):
        self.upper = []
        self.left = []
        self.height = height
        self.width = width
        self.houses = []
        self.nums = []
        self.puzzle = []

    def generate_board(self):
        NUMS = [[EMPTY] * (self.width + 2) for _ in range(self.height + 2)]
        NUMS[0] = [OUT_OF_BOARD] * (self.width + 2)
        NUMS[self.height + 1] = [OUT_OF_BOARD] * (self.width + 2)
        for i in range(1, self.height + 1):
            NUMS[i][0] = OUT_OF_BOARD
            NUMS[i][self.width + 1] = OUT_OF_BOARD
        self.nums = NUMS

    def print_puzzle(self):
        for row in self.puzzle:
            print(' '.join(map(str, row)))

    def get_houses(self, how_many):

        hh = set()

        while len(hh) < how_many:
            x = np.random.randint(1, self.height + 1)
            y = np.random.randint(1, self.width + 1)
            hh.add((x, y))

        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                if (i, j) in hh:
                    self.nums[i][j] = HOUSE
        hh = list(hh)
        return hh


def generate(board, i=0):

    if i == len(board.houses):
        return True

    choice = board.houses[i]

    for direction in DIRS.values():
        row, col = choice[0] + direction[0], choice[1] + direction[1]

        if board.nums[row][col] == EMPTY:
            if domki.check_location_is_safe(board, row, col):
                board.nums[row][col] = TANK
                if generate(board, i + 1):
                    return True
            board.nums[row][col] = EMPTY
    return False


def print_puzzle(board):
    board.upper = [domki.how_many_tanks_col(board, col) for col in
                   range(1, board.width + 1)]
    board.left = [domki.how_many_tanks_row(board, row) for row in
                  range(1, board.height + 1)]
    board.puzzle = [[EMPTY] * (board.width + 1) for _ in
                    range(board.height + 1)]
    board.puzzle[0] = [OUT_OF_BOARD] + board.upper
    for i in range(1, board.height + 1):
        board.puzzle[i][0] = board.left[i - 1]
    hh = board.houses
    for i in range(1, board.height + 1):
        for j in range(1, board.width + 1):
            if (i, j) in hh:
                board.puzzle[i][j] = HOUSE
    for row in board.puzzle:
        print(' '.join(map(str, row)))


def puzzle_to_txt(board):
    with open('architekt_puzz.txt', 'w') as puzzle:
        Upper = ' '.join(str(n) for n in board.upper)
        Left = ' '.join(str(n) for n in board.left)

        puzzle.write(str(board.width) + ' ' + str(board.height) + '\n')
        puzzle.write(Upper + '\n')
        puzzle.write(Left + '\n')
        for row in range(1, board.height + 1):
            puzzle.write(' '.join(map(str, board.puzzle[row][1:])) + '\n')

if __name__ == '__main__':

    while True:
        print("create")

        T = Board(6, 6)
        T.generate_board()

        T.houses = sorted(T.get_houses(5))

        generate(T, i=0)
        for i in range(T.height + 2):
            print(' '.join(map(str, T.nums[i])))

        print_puzzle(T)

        puzzle_to_txt(T)

        print('ARE THERE MORE?')
        B = domki.Board()
        B.read('architekt_puzz.txt')
        hh = []
        for i in range(B.height + 2):
            for j in range(B.width + 2):
                if B.nums[i][j] == HOUSE:
                    hh.append([i, j])
        B.houses = hh

        if domki.solve(B, T.nums, i=0) is False:
            print('no, just this one')
            break
        else:
            print('yes, for example')
            for i in range(B.height + 2):
                print(' '.join(map(str, B.nums[i])))

    print("done, ok")

