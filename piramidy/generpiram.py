import random
import copy
import piramidy
from piramidy import solve

EMPTY = 0
SIZE = 5


class Board:

    def __init__(self, SIZE, upper, down, left, right):
        self.nums = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.upper = upper
        self.down = down
        self.left = left
        self.right = right
        self.SIZE = SIZE
        self.pointer = 0

    def print_grid(self):
        for i in range(SIZE):
            print (self.nums[i])

    def create_puzzle(self):
        self.puzzle = [[EMPTY] * (SIZE + 2) for _ in range(SIZE + 2)]
        self.puzzle[0] = [EMPTY] + self.upper + [EMPTY]
        self.puzzle[SIZE + 1] = [EMPTY] + self.down + [EMPTY]
        for i in range(1, SIZE + 1):
            self.puzzle[i][0] = self.left[i - 1]
            self.puzzle[i][SIZE + 1] = self.right[i - 1]

    def print_puzzle(self):
        for i in range(SIZE + 2):
            print(self.puzzle[i])


def is_okay(board):
    # rows
    for i in range(len(board.nums)):
        if 0 in board.nums[i]:
            return False
        if len(set(board.nums[i])) != len(board.nums[i]):
            return False
    # columns
    for j in range(len(board.nums)):
        col_j = [board.nums[i][j] for i in range(len(board.nums))]
        if len(set(col_j)) != len(col_j):
            return False

    return True


def generate(board):

    SIZE = len(board.nums)

    if board.pointer == SIZE * SIZE:
        if is_okay(board):
            return True
        else:
            return False

    row = int(board.pointer / SIZE)
    col = int(board.pointer % SIZE)

    nums = random.sample(range(1, SIZE + 1), SIZE)

    for num in nums:

        if(piramidy.check_location_is_safe(board, row, col, num)):

            board.nums[row][col] = num
            board.pointer += 1
            if(generate(board)):
                return True
            board.pointer -= 1
            board.nums[row][col] = EMPTY
    return False


def original_to_txt(upper_s, lower_s, left_s, right_s):
    with open('original.txt', 'w') as puzzle:
        Upper = ' '.join(str(n) for n in upper_s)
        Lower = ' '.join(str(n) for n in lower_s)
        Left = ' '.join(str(n) for n in left_s)
        Right = ' '.join(str(n) for n in right_s)

        puzzle.write(str(SIZE) + '\n')
        puzzle.write(Upper + '\n')
        puzzle.write(Lower + '\n')
        puzzle.write(Left + '\n')
        puzzle.write(Right + '\n')


def delete_col_up(upper_s, count):
    which = random.sample(range(SIZE), count)
    for el in which:
        if upper_s[el] != SIZE:
            upper_s[el] = -1


def delete_col_down(lower_s, count):
    which = random.sample(range(SIZE), count)
    for el in which:
        if lower_s[el] != SIZE:
            lower_s[el] = -1


def delete_row_left(left_s, count):
    which = random.sample(range(SIZE), count)
    for el in which:
        if left_s[el] != SIZE:
            left_s[el] = -1


def delete_row_right(right_s, count):
    which = random.sample(range(SIZE), count)
    for el in which:
        if right_s[el] != SIZE:
            right_s[el] = -1


def deleted_move_txt(upper_s, lower_s, left_s, right_s, count):
    delete_col_up(upper_s, count - 1)
    delete_col_down(lower_s, count)
    delete_row_left(left_s, count)
    delete_row_right(right_s, count)
    with open('puzzle.txt', 'w') as puzzle:
        Upper = ' '.join(str(n) for n in upper_s)
        Lower = ' '.join(str(n) for n in lower_s)
        Left = ' '.join(str(n) for n in left_s)
        Right = ' '.join(str(n) for n in right_s)

        puzzle.write(str(SIZE) + '\n')
        puzzle.write(Upper + '\n')
        puzzle.write(Lower + '\n')
        puzzle.write(Left + '\n')
        puzzle.write(Right + '\n')


def is_identical(board1, board2):
    for row in range(len(board1)):
        for col in range(len(board1)):
            if board1[row][col] != board2[row][col]:
                return False
    return True

if __name__ == '__main__':

    print("solve")

    SIZE = 5
    G = Board(SIZE, [], [], [], [])
    generate(G)

    G.print_grid()

    G.upper = [piramidy.how_many_seen_col_up(G, el) for el in range(SIZE)]
    G.down = [piramidy.how_many_seen_col_down(G, el) for el in range(SIZE)]
    G.left = [piramidy.how_many_seen_row_left(G, el) for el in range(SIZE)]
    G.right = [piramidy.how_many_seen_row_right(G, el) for el in range(SIZE)]

    while SIZE not in G.upper or SIZE - 1 not in G.left:
        # to ensure that it is solvable we need two big numbers
        print("generate again")
        G = Board(SIZE, [], [], [], [])
        G.pointer = 0
        generate(G)

        G.print_grid()

        G.upper = [piramidy.how_many_seen_col_up(G, el) for el in range(SIZE)]
        G.down = [piramidy.how_many_seen_col_down(G, el) for el in range(SIZE)]
        G.left = [piramidy.how_many_seen_row_left(G, el) for el in range(SIZE)]
        G.right = [piramidy.how_many_seen_row_right(G, el) for el in
                   range(SIZE)]

    original = [copy.deepcopy(G.upper), copy.deepcopy(G.down),
                copy.deepcopy(G.left), copy.deepcopy(G.right)]

    G.create_puzzle()

    G.print_puzzle()

    print("puzzle ready")
    print(is_okay(G))
    print("delete")
    original_to_txt(G.upper, G.down, G.left, G.right)

    clues = []
    clues = copy.deepcopy(original)
    deleted_move_txt(clues[0], clues[1], clues[2], clues[3], 2)

    with open('puzzle.txt', 'r') as fh:
        SIZE = int(fh.readline())
        upper = list(map(int, fh.readline().split()))
        down = list(map(int, fh.readline().split()))
        left = list(map(int, fh.readline().split()))
        right = list(map(int, fh.readline().split()))

    B = Board(SIZE, upper, down, left, right)

    B.create_puzzle()
    B.print_puzzle()
    B.pointer = 0
    print("how many?")

    if solve(B, G.nums) is False:
        print("unique")
        B.print_puzzle()
    else:
        print("many")
        B.print_grid()
        B.pointer = 0
        while True:
            clues = []
            clues = copy.deepcopy(original)

            deleted_move_txt(clues[0], clues[1], clues[2], clues[3], 2)

            with open('puzzle.txt', 'r') as fh:
                SIZE = int(fh.readline())
                upper = list(map(int, fh.readline().split()))
                down = list(map(int, fh.readline().split()))
                left = list(map(int, fh.readline().split()))
                right = list(map(int, fh.readline().split()))
            B = Board(SIZE, upper, down, left, right)

            B.create_puzzle()

            B.pointer = 0
            if solve(B, G.nums) is False:
                print("unique")
                B.print_puzzle()
                break
    print("done, ok")
