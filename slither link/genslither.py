import itertools as it
import random
import numpy as np
import slith
import copy

EMPTY = -1
OUT_OF_BOARD = -2
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4


ALL_DIRS = [
    [-1, 0],
    [1,  0],
    [0, -1],
    [0,  1]
]

OFFSET_TO_DIR = {
    (-1, 0): UP,
    (1,  0): DOWN,
    (0,  1): RIGHT,
    (0, -1): LEFT
}


class Board:
    def __init__(self, n, m):
        self.nums_height = n + 2
        self.nums_width = m + 2
        self.nums = [[EMPTY] * self.nums_width]
        for i in range(n):
            self.nums += [[EMPTY] + [EMPTY for x in range(m)] +
                          [EMPTY]]
        self.nums += [[EMPTY] * self.nums_width]

        self.dots_height = self.nums_height + 1
        self.dots_width = self.nums_width + 1
        self.dots = [[OUT_OF_BOARD] * self.dots_width]
        for i in range(1, self.dots_height - 1):
            self.dots += [[OUT_OF_BOARD] + [EMPTY] * (self.dots_width - 2) +
                          [OUT_OF_BOARD]]
        self.dots += [[OUT_OF_BOARD] * self.dots_width]

        self.edges_taken = 0
        self.solutions = 0


def global_check(board, edges_taken, final=False):
    for i, j in it.product(range(board.nums_height), range(board.nums_width)):
        amount_taken = 0
        for edge in slith.face_to_edges(i, j):
            if edge in edges_taken:
                amount_taken += 1
    x = board.dots[board.dots_height - 1]
    if amount_taken > 3 or x.count(-1) == len(x):
        return False
    if len(edges_taken) < 2 * board.nums_height + board.nums_width:
        return False

    board.edges_taken = len(edges_taken)
    return True


def is_drawn(board, dot1, dot2):
    i, j = dot1
    x, y = dot2

    if x == i and y == j + 1:   # top / bottom of the cell
        if board.dots[i][j] == 3 or board.dots[x][y] == 4:
            return True
    if x == i + 1 and y == j:   # left / right hand side of the cell
        if board.dots[i][j] == 2 or board.dots[x][y] == 1:
            return True
    return False


def count_edges(board):
    for i, j in it.product(range(1, board.nums_height - 1),
                           range(1, board.nums_width - 1)):
        amount_taken = 0
        edges = slith.face_to_edges(i, j)
        for edge in edges:
            if is_drawn(board, edge[0], edge[1]):
                amount_taken += 1
        board.nums[i][j] = amount_taken


def fast_check(board, edges_taken, face):
    i, j = face
    amount_taken = 0
    for edge in slith.face_to_edges(i, j):
        if edge in edges_taken:
            amount_taken += 1
    if amount_taken > 3:
        return False
    return True


def delete_clues(board, nums, how_many):
    clues = set()

    while len(clues) < how_many:
        x = np.random.randint(1, board.nums_height)
        y = np.random.randint(1, board.nums_width)
        if board.nums[x][y] != 0 and board.nums[x][y] != EMPTY:
            clues.add((x, y))
    for clue in clues:
        nums[clue[0]][clue[1]] = EMPTY
    return nums


def create_puzzle(board, nums):
    with open("slither.txt", 'w') as puzzle:
        puzzle.write(str(board.nums_height - 2) + ' ' +
                     str(board.nums_height - 2) + '\n')
        for row in nums[1:-1]:
            puzzle.write(' '.join(map(str, row[1:-1])) + '\n')


def generate(board, edges_taken=None, i=1, j=1, begin_i=1, begin_j=1):
    if not edges_taken:  # edges are represented by an ORDERED pair of pairs
        edges_taken = set()
    if abs(begin_i - i) + abs(begin_j - j) == 1 and len(edges_taken) > 1:
        last_edge = tuple(sorted([(begin_i, begin_j), (i, j)]))
        board.dots[i][j] = OFFSET_TO_DIR[(begin_i - i, begin_j - j)]
        edges_taken.add(last_edge)
        if global_check(board, edges_taken, final=True):
            return True
        board.dots[i][j] = EMPTY
        edges_taken.remove(last_edge)

    for _ in range(4):
        offset = random.choice(list(OFFSET_TO_DIR.keys()))
        dir_to_next = OFFSET_TO_DIR[offset]
        next_i, next_j = i + offset[0], j + offset[1]
        if board.dots[next_i][next_j] == EMPTY:
            board.dots[i][j] = dir_to_next
            edge_being_added = tuple(sorted([(i, j), (next_i, next_j)]))
            edges_taken.add(edge_being_added)
            face_A, face_B = slith.edge_to_faces(edge_being_added)
            if fast_check(board, edges_taken, face_A) and \
            fast_check(board, edges_taken, face_B):
                ret_val = generate(board, edges_taken, next_i,
                                   next_j, begin_i, begin_j)
                if ret_val:
                    return True
            board.dots[i][j] = EMPTY
            edges_taken.remove(edge_being_added)
    return False

if __name__ == "__main__":
    B = Board(5, 5)

    found = False
    if generate(B, edges_taken=None, i=1, j=1, begin_i=1, begin_j=1):
        found = True
    if found:
        print(str(B.dots_height) + " " + str(B.dots_width))
        for dots_row in B.dots:
            print(' | '.join(map(str, dots_row)))
        print()
    else:
        print("No solution")

    count_edges(B)

    for row in B.nums:
        print(' '.join(map(str, row)))  # good, no mistakes in counting edges
    print()

    original = B.nums
    nums = copy.deepcopy(original)
    print('nums')
    print(nums)

    # now we have generated the solved board
    # and we're going to create a puzzle
    # for that we need to delete some of the excessive numbers in cells

    many = B.edges_taken
    nums = delete_clues(B, nums, 5)
    print('nums')
    print(nums)
    create_puzzle(B, nums)
    for row in nums:
        print(' '.join(map(str, row[1:-1])) + '\n')

    # is it solvable? it should be, but it is worth checking anyway
    C = slith.Board()
    C.read('slither.txt')

    biggest_tile, biggest_tile_val = slith.find_biggest_tile(C)

    # dangerous assumption that there is a tile with val >= 1
    # ... and all the tiles are <= 3

    found_solution = False
    for begining_offsets in ALL_DIRS:
        begin_i = biggest_tile[0] + begining_offsets[0]
        begin_j = biggest_tile[1] + begining_offsets[1]
        if slith.backtrack(C, edges_taken=None, i=begin_i, j=begin_j,
                           begin_i=begin_i, begin_j=begin_j):
            found_solution = True
            break

    if found_solution:
        for dots_row in C.dots:
            print(' | '.join(map(str, dots_row)))
        print()
    else:
        print("No solution")

    # the main prroblem is - is the solution unique
    D = slith.Board()
    D.read('slither.txt')

    biggest_tile, biggest_tile_val = slith.find_biggest_tile(D)
    found_solution = False
    for begining_offsets in ALL_DIRS:
        begin_i = biggest_tile[0] + begining_offsets[0]
        begin_j = biggest_tile[1] + begining_offsets[1]
        slith.backtrack(D, edges_taken=None, i=begin_i, j=begin_j,
                        begin_i=begin_i, begin_j=begin_j, end_if_found=False)
        if D.solutions != 0:
            break
    print(D.solutions)
    if D.solutions > 2:
        print("The solution is not unique")
    else:
        print("unique")

    # there are two edges coming out of a vertex, so there are two
    # possible directions to follow the path

    while D.solutions > 2:
        many = B.edges_taken
        nums = delete_clues(B, nums, 5)
        print('nums')
        print(nums)
        create_puzzle(B, nums)
        for row in nums:
            print(' '.join(map(str, row[1:-1])) + '\n')

        C = slith.Board()
        C.read('slither.txt')

        biggest_tile, biggest_tile_val = slith.find_biggest_tile(C)

        # dangerous assumption that there is a tile with val >= 1
        # ... and all the tiles are <= 3

        found_solution = False
        for begining_offsets in ALL_DIRS:

            begin_i = biggest_tile[0] + begining_offsets[0]
            begin_j = biggest_tile[1] + begining_offsets[1]
            if slith.backtrack(C, edges_taken=None, i=begin_i, j=begin_j,
                               begin_i=begin_i, begin_j=begin_j):
                found_solution = True
                break

        if found_solution:
            # print(str(B.dots_height) + " " + str(B.dots_width))
            for dots_row in C.dots:
                print(' | '.join(map(str, dots_row)))
            print()
        else:
            print("No solution")

        D = slith.Board()
        D.read('slither.txt')

        biggest_tile, biggest_tile_val = slith.find_biggest_tile(D)
        found_solution = False
        for begining_offsets in ALL_DIRS:
            begin_i = biggest_tile[0] + begining_offsets[0]
            begin_j = biggest_tile[1] + begining_offsets[1]
            slith.backtrack(D, edges_taken=None, i=begin_i, j=begin_j,
                            begin_i=begin_i, begin_j=begin_j,
                            end_if_found=False)
            if D.solutions != 0:
                break
        print(D.solutions)

    if D.solutions > 2:
        print("The solution is not unique")
    else:
        print("unique")

