import random
import copy

EMPTY = 0
SIZE = 4
pointer = 0
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
        self.puzzle[SIZE + 1] = [EMPTY] + self.down + [EMPTY]
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
    #delete_col_up(upper_s, count)
    delete_col_down(lower_s, count)
    #delete_row_left(left_s, count)
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
    
    print("solve")
    
    SIZE = 5
    G = Board()
    generate(G)
    
    G.print_grid()
    
    G.upper = [how_many_seen_col_up(G, el) for el in range(SIZE)]
    G.down = [how_many_seen_col_down(G, el) for el in range(SIZE)]
    G.left = [how_many_seen_row_left(G, el) for el in range(SIZE)]
    G.right = [how_many_seen_row_right(G, el) for el in range(SIZE)]
    
    original = [copy.deepcopy(G.upper), copy.deepcopy(G.down), copy.deepcopy(G.left), copy.deepcopy(G.right)]
    

    G.create_puzzle()


    G.print_puzzle()
    
    print("koniec")
    print(is_okay(G))
    print("solve")
    original_to_txt(G.upper, G.down, G.left, G.right)
    clues = copy.deepcopy(original)

    deleted_move_txt(clues[0], clues[1], clues[2], clues[3], 1)

    with open('puzzle.txt', 'r') as fh:
        SIZE = int(fh.readline())
        upper = list(map(int, fh.readline().split()))
        down = list(map(int, fh.readline().split()))
        left = list(map(int, fh.readline().split()))
        right = list(map(int, fh.readline().split()))
    B = Board()
    B.upper = upper
    B.down = down
    B.left = left
    B.right = right
    B.create_puzzle()
    B.print_puzzle()
    pointer = 0
    if solve(B, G.nums) == False:
        print("done")
    else:
        print("kilka")
        B.print_grid()
    
    print("done, ok")

    print("NEXT")
    clues = []
    clues = copy.deepcopy(original)
    
    deleted_move_txt(clues[0], clues[1], clues[2], clues[3], 1)
    
    with open('puzzle.txt', 'r') as fh:
        SIZE = int(fh.readline())
        upper = list(map(int, fh.readline().split()))
        down = list(map(int, fh.readline().split()))
        left = list(map(int, fh.readline().split()))
        right = list(map(int, fh.readline().split()))
    B2 = Board()
    B2.upper = upper
    B2.down = down
    B2.left = left
    B2.right = right
    B2.create_puzzle()
    B2.print_puzzle()
    pointer = 0
    if solve(B2, G.nums) == False:
        print("done")
    else:
        print("kilka")
        B2.print_grid()
   
