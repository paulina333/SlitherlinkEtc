import random
from piram2 import *

EMPTY = 0
SIZE = 4
pointer = 0
spointer = 0
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
    
    def create_puzzle(self):
        self.puzzle = [[EMPTY] * (SIZE + 2) for _ in range(SIZE + 2)]
        self.puzzle[0] = [EMPTY] + self.upper + [EMPTY]
        self.puzzle[SIZE + 1] = [EMPTY] + self.lower + [EMPTY]
        for i in range(1, SIZE + 1):
           self.puzzle[i][0] = self.left[i - 1]
           self.puzzle[i][SIZE + 1] = self.right[i - 1]
  
    
    def print_puzzle(self):
        for i in range(SIZE + 2):
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

def generate(board):
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
            if(generate(board)):
                return True
            pointer -= 1
            board.nums[row][col] = EMPTY
    return False


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


def original_to_txt(board, upper_s, lower_s, left_s, right_s):
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


def delete_col_up(board, upper_s, count):
    which = random.sample(range(SIZE), count)
    for el in which:
        upper_s[el] = EMPTY


def delete_col_down(board, lower_s, count):
    which = random.sample(range(SIZE), count)
    for el in which:
        lower_s[el] = EMPTY


def delete_row_left(board, left_s, count):
    which = random.sample(range(SIZE), count)
    for el in which:
        left_s[el] = EMPTY


def delete_row_right(board, right_s, count):
    which = random.sample(range(SIZE), count)
    for el in which:
        right_s[el] = EMPTY

def deleted_move_txt(board, upper_s, lower_s, left_s, right_s, count):
    delete_col_up(board, upper_s, count)
    delete_col_down(board, lower_s, count)
    delete_row_left(board, left_s, count)
    delete_row_right(board, right_s, count)
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
 
def solve_test_clues(file_name):
    with open(file_name, 'r') as fh:
        SIZE = int(fh.readline())
        upper = list(map(int, fh.readline().split()))
        down = list(map(int, fh.readline().split()))
        left = list(map(int, fh.readline().split()))
        right = list(map(int, fh.readline().split()))
    T = piram2.Board()
    pointer = 0
    piram2.solve(T)
    T.print_grid()



if __name__ == '__main__':
    
    print("solve")
    
    SIZE = 5
    G = Board()
    generate(G)
    
    G.print_grid()
    
    G.upper = [how_many_seen_col_up(G, el) for el in range(SIZE)]
    G.lower = [how_many_seen_col_down(G, el) for el in range(SIZE)]
    G.left = [how_many_seen_row_left(G, el) for el in range(SIZE)]
    G.right = [how_many_seen_row_right(G, el) for el in range(SIZE)]
    
    original = [G.upper, G.lower, G.left, G.right]
    

    G.create_puzzle()


    G.print_puzzle()
    
    print("koniec")
    print(is_okay(G))
    print("solve")
    original_to_txt(G, G.upper, G.lower, G.left, G.right)
    deleted_move_txt(G, G.upper, G.lower, G.left, G.right, 2)
    with open('puzzle.txt', 'r') as fh:
        SIZE = int(fh.readline())
        upper = list(map(int, fh.readline().split()))
        down = list(map(int, fh.readline().split()))
        left = list(map(int, fh.readline().split()))
        right = list(map(int, fh.readline().split()))
    T = Board()
    pointer = 0
    solve(T)
    rozw = T.nums
    print(rozw)
    #while solve_test_clues('puzzle.txt') == False:
     #   deleted_move_txt(G, G.upper, G.lower, G.left, G.right, 2)
      #  solve_test_clues('puzzle.txt')

    print("done, ok")
    
