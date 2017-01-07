import random

EMPTY = 0
pointer = 0
SIZE = 0
upper = None
down = None
left = None
right = None


class Board:

    def __init__(self):
        self.nums = [[EMPTY] * SIZE for _ in range(SIZE)]
       
        
    def print_grid(self):
        for i in range(SIZE):
            print (self.nums[i])


def used_in_row(board, row, num):
    for i in range(SIZE):
        if(board.nums[row][i] == num):
            return True
    return False


def used_in_col(board, col, num):
    for i in range(SIZE):
        if(board.nums[i][col] == num):
            return True
    return False


def check_location_is_safe(board, row, col, num):
    return not used_in_row(board, row, num) and \
           not used_in_col(board, col, num)


def how_many_seen_row_right(board, row):  # row = 0,1,...
    now = 1
    high = board.nums[row][SIZE - 1]
    for el in range(2, SIZE + 1):
        if board.nums[row][SIZE - el] > high:
            now += 1
            high = board.nums[row][SIZE - el]
    return now


def how_many_seen_row_left(board, row):  # row = 0,1,...
    now = 1
    high = board.nums[row][0]
    for el in range(1, SIZE):
        if board.nums[row][el] > high:
            now += 1
            high = board.nums[row][el]
    return now


def how_many_seen_col_up(board, col):  # col = 0,1,...
    now = 1
    high = board.nums[0][col]
    for el in range(1, SIZE):
        if board.nums[el][col] > high:
            now += 1
            high = board.nums[el][col]
    return now


def how_many_seen_col_down(board, col):  # col = 0,1,...
    now = 1
    high = board.nums[SIZE - 1][col]
    for el in range(2, SIZE + 1):
        if board.nums[SIZE - el][col] > high:
            now += 1
            high = board.nums[SIZE - el][col]
    return now


def is_ordered_row(board, row):

    if left[row] == -1 and right[row] == -1:
        return True
    else:
        if left[row] > 0:
            if how_many_seen_row_left(board, row) != left[row]:
                return False

        if right[row] > 0:
            if how_many_seen_row_right(board, row) != right[row]:
                return False

    return True


def is_ordered_col(board, col):

    if upper[col] == -1 and down[col] == -1:
        return True
    else:
        if upper[col] > 0:
            if how_many_seen_col_up(board, col) != upper[col]:
                return False
        if down[col] > 0:
            if how_many_seen_col_down(board, col) != down[col]:
                return False
    return True


def is_ordered(board):
    for row in range(SIZE):
        if 0 in board.nums[row]:
            return False
        if not is_ordered_row(board, row):
            return False
        if not is_ordered_col(board, row):
            return False
    return True

def is_identical(board1, board2):
    for row in range(len(board1)):
        for col in range(len(board1)):
            if board1[row][col] != board2[row][col]:
                return False
    return True

def solve(board, solvedBoard):
    global pointer

    # keeps the record of the first empty place in the board
    if pointer == SIZE * SIZE:
        if is_ordered(board):
            if solvedBoard == None:
                return True
            if is_identical(board.nums, solvedBoard):
                return False
            else:
                return True
        else:
            return False

    # Assigning list values to row and col that we got from the above
    row = int(pointer / SIZE)
    col = int(pointer % SIZE)
    for num in range(1, SIZE + 1):

        if(check_location_is_safe(board, row, col, num)):

            board.nums[row][col] = num
            pointer += 1
            if(solve(board, solvedBoard)):
                if solvedBoard == None:
                    return True
                if is_identical(board.nums, solvedBoard):
                    return False
                else:
                    return True
            pointer -= 1
            board.nums[row][col] = EMPTY
    return False
 
if __name__ == '__main__':
    file_name = 'puzzle.txt'
    with open(file_name, 'r') as fh:
        SIZE = int(fh.readline())
        upper = list(map(int, fh.readline().split()))
        down = list(map(int, fh.readline().split()))
        left = list(map(int, fh.readline().split()))
        right = list(map(int, fh.readline().split()))
    print("solve")

    T = Board()
    solve(T, None)

    T.print_grid()

    print("koniec")
    print(is_ordered(T))
    print('ile?')

    C = Board()
    pointer = 0
    if solve(C, T.nums) == False:
        print("jedna")
    else:
        print("kilka")
        C.print_grid()
