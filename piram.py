import itertools as it

EMPTY = 0
SIZE = None
upper = None
down = None
left = None
right = None
                
class Board:
        
    def __init__(self):
        self.nums = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.List = [0, 0]

    def print_grid(self):
        for i in range(SIZE):
            print (self.nums[i])

def find_empty_location(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if(board.nums[row][col] == EMPTY):   
                board.List[0] = row
                board.List[1] = col
                return board.List
    return False    

def used_in_row(board, row, num):
    for i in range(SIZE):
        if(board.nums[row][i] == num):
            return True
    return False

def used_in_col(board, col, num):
    for i in range( SIZE):
        if(board.nums[i][col] == num):
            return True
    return False
    
def check_location_is_safe(board, row, col, num):
    return not used_in_row(board, row, num) and not used_in_col(board, col, num)

def how_many_seen_row_right(board, row):  # row = 0,1,...
    now = 1
    high = board.nums[row][SIZE - 1]
    for el in range(1, SIZE):
        if board.nums[row][SIZE - el] < board.nums[row][SIZE - el - 1]:
            now +=1
            high = board.nums[row][SIZE - el - 1]
    return now       

def how_many_seen_row_left(board, row):  # row = 0,1,...
    now = 1
    high = board.nums[row][0]
    for el in range(SIZE-1):
        if board.nums[row][el] < board.nums[row][el + 1]:
            now +=1
            high = board.nums[row][el + 1]
    return now 

def how_many_seen_col_up(board, col):  # col = 0,1,...
    now = 1
    high = board.nums[0][col]
    for el in range(SIZE - 1):
        if board.nums[el][col] < board.nums[el + 1][col]:
            now +=1
            high = board.nums[el + 1][col]
    return now 

def how_many_seen_col_down(board, col):  # col = 0,1,...
    now = 1
    high = board.nums[0][col]
    for el in range(1, SIZE):
        if board.nums[SIZE - el][col] < board.nums[SIZE - el - 1][col]:
            now +=1
            high = board.nums[SIZE - el - 1][col]
    return now 

def is_ordered_row(board, row):
    ok = False
    if left[row] == -1 and right[row] == -1:
        return True
    else:
        if left[row] > 0:
            if how_many_seen_row_left(board, row) == left[row]:
                ok = True
        if right[row] > 0:
            if how_many_seen_row_right(board, row) == right[row]:
                ok = True
    return ok

def is_ordered_col(board, col):
    ok = True
    if upper[col] == -1 and down[col] == -1:
        return True
    else:
        if upper[col] > 0:
            if how_many_seen_col_up(board, col) != upper[col]:
                ok = False
        if down[col] > 0:
            if how_many_seen_col_down(board, col) != down[col]:
                ok = False
    return ok

def is_ordered(board):
    for row in range(SIZE):
        if 0 in board.nums[row]:
            return False
        if is_ordered_row(board, row):
            for col in range(SIZE):
                if not is_ordered_col(board, col):
                    return False
    return True

def solve(board):
     
    # keeps the record of row and col in find_empty_location Function
        
    if is_ordered(board):
        return True
    find_empty_location(board)

    # Assigning list values to row and col that we got from the above Function 
    row = board.List[0]
    col = board.List[1]

    for num in range(1, SIZE + 1):

        if(check_location_is_safe(board, row, col, num)):

            board.nums[row][col]=num
 
            if(solve(board)):
                return True
 
            board.nums[row][col] = EMPTY
                    
    return False

if __name__ == '__main__':
    file_name = 'piramidy.txt'
    with open(file_name, 'r') as fh:
        SIZE = int(fh.readline())
        upper = list(map(int, fh.readline().split()))
        down = list(map(int, fh.readline().split()))
        left =  list(map(int, fh.readline().split()))
        right = list(map(int, fh.readline().split()))

    print("solve")

    T = Board()
    solve(T)

    T.print_grid()

    print("koniec")
    print(is_ordered(T))
    #B = Board()
    #B.nums[2] = [1,2,3,4]
    #B.nums[0] = [2,1,4,3]
    #B.nums[1] = [3,4,2,1]
#    B.nums[3] = [4,3,1,2]
 #   B.print_grid()
  #  print()
   # print(upper)

    #print(how_many_seen_row_right(B, 2))
#    print(how_many_seen_row_left(B, 2))
 #   print(how_many_seen_col_up(B, 0))
  #  print(how_many_seen_col_down(B, 0))
   # print(is_ordered_row(B, 2))
 #   print(is_ordered_col(B, 0))
  #  print(is_ordered(B))

#    Bb = Board()
 #   Bb.nums[2] = [1,4,3,2]
  #  Bb.nums[0] = [4,1,2,3]
   # Bb.nums[1] = [3,2,4,1]
    #Bb.nums[3] = [2,3,1,4]
#    Bb.print_grid()
 #   print(left)
  #  print(right)
   # print(is_ordered(Bb))
    #print(how_many_seen_row_right(Bb, 1))
#    print(is_ordered_col(Bb, 0))
 #   print(is_ordered_col(Bb, 1))
  #  print(is_ordered_col(Bb, 2))
   # print(is_ordered_col(Bb, 3))

