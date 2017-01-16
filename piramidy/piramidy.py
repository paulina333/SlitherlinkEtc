EMPTY = 0


class Board:

    def __init__(self):
        self.nums = []
        self.upper = []
        self.down = []
        self.left = []
        self.right = []
        self.SIZE = 1
        self.pointer = 0

    def print_grid(self):
        for i in range(self.SIZE):
            print (self.nums[i])

    def read(self, file_name):
        with open(file_name, 'r') as fh:
            self.SIZE = int(fh.readline())
            self.upper = list(map(int, fh.readline().split()))
            self.down = list(map(int, fh.readline().split()))
            self.left = list(map(int, fh.readline().split()))
            self.right = list(map(int, fh.readline().split()))
        self.nums = [[EMPTY] * self.SIZE for _ in range(self.SIZE)]


def used_in_row(board, row, num):
    for i in range(board.SIZE):
        if(board.nums[row][i] == num):
            return True
    return False


def used_in_col(board, col, num):
    for i in range(board.SIZE):
        if(board.nums[i][col] == num):
            return True
    return False


def check_location_is_safe(board, row, col, num):
    return not used_in_row(board, row, num) and \
           not used_in_col(board, col, num)


def how_many_seen_row_right(board, row):  # row = 0,1,...
    now = 1
    high = board.nums[row][board.SIZE - 1]
    for el in range(2, board.SIZE + 1):
        if board.nums[row][board.SIZE - el] > high:
            now += 1
            high = board.nums[row][board.SIZE - el]
    return now


def how_many_seen_row_left(board, row):  # row = 0,1,...
    now = 1
    high = board.nums[row][0]
    for el in range(1, board.SIZE):
        if board.nums[row][el] > high:
            now += 1
            high = board.nums[row][el]
    return now


def how_many_seen_col_up(board, col):  # col = 0,1,...
    now = 1
    high = board.nums[0][col]
    for el in range(1, board.SIZE):
        if board.nums[el][col] > high:
            now += 1
            high = board.nums[el][col]
    return now


def how_many_seen_col_down(board, col):  # col = 0,1,...
    now = 1
    high = board.nums[board.SIZE - 1][col]
    for el in range(2, board.SIZE + 1):
        if board.nums[board.SIZE - el][col] > high:
            now += 1
            high = board.nums[board.SIZE - el][col]
    return now


def is_ordered_row(board, row):

    if board.left[row] == -1 and board.right[row] == -1:
        return True
    else:
        if board.left[row] > 0:
            if how_many_seen_row_left(board, row) != board.left[row]:
                return False

        if board.right[row] > 0:
            if how_many_seen_row_right(board, row) != board.right[row]:
                return False

    return True


def is_ordered_col(board, col):

    if board.upper[col] == -1 and board.down[col] == -1:
        return True
    else:
        if board.upper[col] > 0:
            if how_many_seen_col_up(board, col) != board.upper[col]:
                return False
        if board.down[col] > 0:
            if how_many_seen_col_down(board, col) != board.down[col]:
                return False
    return True


def is_ordered(board):
    for row in range(board.SIZE):
        if 0 in board.nums[row]:
            return False
        if not is_ordered_row(board, row):
            return False
        if not is_ordered_col(board, row):
            return False
    return True


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


def solve(board, solvedBoard):

    # keeps the record of the first empty place in the board
    if board.pointer == board.SIZE * board.SIZE:
        if is_ordered(board):
            if solvedBoard is None:
                return True
            if is_identical(board.nums, solvedBoard):
                return False
            else:
                return True
        else:
            return False

    # Assigning list values to row and col that we got from the above
    row = int(board.pointer / board.SIZE)
    col = int(board.pointer % board.SIZE)
    for num in range(1, board.SIZE + 1):

        if(check_location_is_safe(board, row, col, num)):

            board.nums[row][col] = num
            board.pointer += 1
            if(solve(board, solvedBoard)):
                if solvedBoard is None:
                    return True
                if is_identical(board.nums, solvedBoard):
                    return False
                else:
                    return True
            board.pointer -= 1
            board.nums[row][col] = EMPTY
    return False


if __name__ == '__main__':

    print("solve")

    T = Board()
    T.read('puzzle.txt')
    solve(T, None)
    T.print_grid()

    print("solved")
    print(is_ordered(T))
    print('how many solutions?')

    C = Board()
    C.read('puzzle.txt')
    C.pointer = 0
    if solve(C, T.nums) is False:
        print("unique")
    else:
        print("many")
        C.print_grid()
