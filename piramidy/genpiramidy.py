import random

EMPTY = 0
pointer = 0


class Board:

    def __init__(self, SIZE):
        self.nums = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.SIZE = SIZE
        
    def print_grid(self):
        for i in range(self.SIZE):
            print (self.nums[i])
    
    def create_puzzle(self):
        self.puzzle = [[EMPTY] * (self.SIZE + 2) for _ in range(self.SIZE + 2)]
        self.puzzle[0] = [EMPTY] + self.upper + [EMPTY]
        self.puzzle[self.SIZE + 1] = [EMPTY] + self.lower + [EMPTY]
        for i in range(1, self.SIZE + 1):
           self.puzzle[i][0] = self.left[i - 1]
           self.puzzle[i][self.SIZE + 1] = self.right[i - 1]
  
    
    def print_puzzle(self):
        for i in range(self.SIZE + 2):
            print(self.puzzle[i])


def used_in_row(board, row, num):
    for i in range(len(board.nums)):
        if(board.nums[row][i] == num):
            return True
    return False


def used_in_col(board, col, num):
    for i in range(len(board.nums)):
        if(board.nums[i][col] == num):
            return True
    return False


def check_location_is_safe(board, row, col, num):
    return not used_in_row(board, row, num) and \
           not used_in_col(board, col, num)


def is_okay(board):
    # rows
    for i in range(len(board.nums)):
        if 0 in board.nums[i]:
            return False
        if len(set(board.nums[i])) != len(board.nums[i]):
            return False
    #columns
    for j in range(len(board.nums)):
        col_j = [board.nums[i][j] for i in range(len(board.nums))]
        if len(set(col_j)) != len(col_j):
            return False
        
    return True

def solve(board):
    global pointer
    SIZE = len(board.nums)

    if pointer == SIZE * SIZE:
        if is_okay(board):
            return True
        else:
            return False
        
    row = int(pointer / SIZE)
    col = int(pointer % SIZE)
    
    nums = random.sample(range(1, SIZE + 1), SIZE)
    
    for num in nums:

        if(check_location_is_safe(board, row, col, num)):

            board.nums[row][col] = num
            pointer += 1
            if(solve(board)):
                return True
            pointer -= 1
            board.nums[row][col] = EMPTY
    return False


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



if __name__ == '__main__':
    
    print("solve")
    
    size = 5
    T = Board(size)
    solve(T)
    
    T.print_grid()
    
    T.upper = [how_many_seen_col_up(T, el) for el in range(size)]
    T.lower = [how_many_seen_col_down(T, el) for el in range(size)]
    T.left = [how_many_seen_row_left(T, el) for el in range(size)]
    T.right = [how_many_seen_row_right(T, el) for el in range(size)]
    
    T.create_puzzle()


    T.print_puzzle()
    
    print("koniec")
    print(is_okay(T))

