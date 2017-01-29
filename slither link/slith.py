import itertools as it

EMPTY = -1
OUT_OF_BOARD = "."
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
    def __init__(self):
        self.nums_height = 0
        self.nums_width = 0
        self.nums = []
        self.dots_height = 0
        self.dots_width = 0
        self.dots = []
        self.solutions = 0

    def read(self, filename):
        with open(filename, 'r') as fh:
            n, m = map(int, fh.readline().split())
            NUMS = [[EMPTY] * (m + 2)]
            for _ in range(n):
                NUMS += [[EMPTY] + [int(x) for x in fh.readline().split()] +
                         [EMPTY]]
            NUMS += [[EMPTY] * (m + 2)]
        self.nums = NUMS
        self.nums_height = n + 2
        self.nums_width = m + 2

        self.dots_height = self.nums_height + 1
        self.dots_width = self.nums_width + 1
        self.dots = [[OUT_OF_BOARD] * self.dots_width]
        for i in range(1, self.dots_height - 1):
            self.dots += [[OUT_OF_BOARD] + [EMPTY] * (self.dots_width - 2) +
                          [OUT_OF_BOARD]]
        self.dots += [[OUT_OF_BOARD] * self.dots_width]


def edge_to_faces(edge):
    begin, end = edge
    if begin[0] == end[0]:
        return [(begin[0], begin[1] - 1), (begin[0], begin[1])]
        # upper and lower cell
    else:
        return [(begin[0] - 1, begin[1]), (begin[0], begin[1])]
        # left and right cell


def face_to_edges(i, j):
    # the points surrounding the face
    A = (i, j)
    B = (i, j + 1)
    C = (i + 1, j)
    D = (i + 1, j + 1)
    return [(A, B), (A, C), (B, D), (C, D)]


def global_check(board, edges_taken, final=False):
    # check if all the edges are consistent with the numbers in all the cells
    for i, j in it.product(range(board.nums_height), range(board.nums_width)):
        if board.nums[i][j] != EMPTY:
            amount_taken = 0
            for edge in face_to_edges(i, j):
                if edge in edges_taken:
                    amount_taken += 1
            if amount_taken > board.nums[i][j] or \
                    (final and amount_taken != board.nums[i][j]):
                return False
    return True


def fast_check(board, edges_taken, face):
    # check if there arent too many edges around the face
    i, j = face
    if board.nums[i][j] != EMPTY:
        amount_taken = 0
        for edge in face_to_edges(i, j):
            if edge in edges_taken:
                amount_taken += 1
        if amount_taken > board.nums[i][j]:
            return False
    return True


def find_biggest_tile(board):
    biggest_tile, biggest_tile_val = (1, 1), board.nums[1][1]
    for i in range(1, board.nums_height - 1):
        for j in range(1, board.nums_width - 1):
            if board.nums[i][j] > biggest_tile_val:
                biggest_tile_val = board.nums[i][j]
                biggest_tile = (i, j)
    return (biggest_tile, biggest_tile_val)


def backtrack(board, edges_taken=None, i=1, j=1, begin_i=1, begin_j=1,
              end_if_found=True):
    # print(str(i) + " " + str(j))
    if not edges_taken:
        # edge is an ORDERED pair of pairs, so the same two edges dont coincide
        edges_taken = set()
    if abs(begin_i - i) + abs(begin_j - j) == 1 and len(edges_taken) > 1:
        # i.e. path is one edge away from being finished
        last_edge = tuple(sorted([(begin_i, begin_j), (i, j)]))
        # if last_edge not in edges_taken:
        board.dots[i][j] = OFFSET_TO_DIR[(begin_i - i, begin_j - j)]
        edges_taken.add(last_edge)
        if global_check(board, edges_taken, final=True):
            print("Found\n")
            if end_if_found:
                return True
            else:
                board.solutions += 1
                print("sols " + str(board.solutions))
                for dots_row in board.dots:
                    print(' '.join(map(str, dots_row)))
                print()
        board.dots[i][j] = EMPTY
        edges_taken.remove(last_edge)
        return False

    for (offset, dir_to_next) in OFFSET_TO_DIR.items():
        next_i, next_j = i + offset[0], j + offset[1]
        if board.dots[next_i][next_j] == EMPTY:
            board.dots[i][j] = dir_to_next
            edge_being_added = tuple(sorted([(i, j), (next_i, next_j)]))
            edges_taken.add(edge_being_added)
            face_A, face_B = edge_to_faces(edge_being_added)
            if fast_check(board, edges_taken, face_A) and \
                    fast_check(board, edges_taken, face_B):

                if backtrack(board, edges_taken,
                             next_i, next_j, begin_i, begin_j, end_if_found):
                    return True
            board.dots[i][j] = EMPTY
            edges_taken.remove(edge_being_added)

    return False

if __name__ == "__main__":

    B = Board()
    B.read('no_sol.txt')
    # for debuging purposes
    # for row in B.nums:
    #    print(' '.join(map(str, row)))
    # print()

    # ugly part

    biggest_tile, biggest_tile_val = find_biggest_tile(B)

    # dangerous assumption that there is a tile with val >= 1
    # ... and all the tiles are <= 3

    found_solution = False
    for begining_offsets in ALL_DIRS:

        begin_i = biggest_tile[0] + begining_offsets[0]
        begin_j = biggest_tile[1] + begining_offsets[1]
        if backtrack(B, edges_taken=None, i=begin_i, j=begin_j,
                     begin_i=begin_i, begin_j=begin_j):
            found_solution = True
            break

    if found_solution:
        for dots_row in B.dots:
            print(' | '.join(map(str, dots_row)))
        print()
    else:
        print("No solution")

    C = Board()
    C.read('no_sol.txt')
    print(C.nums)

    biggest_tile, biggest_tile_val = find_biggest_tile(C)

    found_solution = False
    for begining_offsets in ALL_DIRS:
        begin_i = biggest_tile[0] + begining_offsets[0]
        begin_j = biggest_tile[1] + begining_offsets[1]
        backtrack(C, edges_taken=None, i=begin_i, j=begin_j,
                  begin_i=begin_i, begin_j=begin_j, end_if_found=False)
        if C.solutions != 0:
            break
    print(C.solutions)

    if C.solutions > 2:
        print("The solution is not unique")
    else:
        print("unique")
