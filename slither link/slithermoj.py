EMPTY = 0
OUT_OF_BOARD = -2
n = 0
m = 0
pointer = 0

class Board:
    def __init__(self):
        global n
        global m
        self.nums_height = n
        self.nums_width = m
        
        self.nums = NUMS

        self.vert = [[EMPTY for i in range(m +1)] for j in range(n)]  
        # there are (M+1) vertical edges widthwise, N heightwise
        # j=1,2,...,N;   i = 1,2,...,M+1;
        self.horiz = [[EMPTY for i in range(m)] + [OUT_OF_BOARD] for j in range(n + 1)]
        # M horizontal edges widthwise, N+1 heightwise
        # j=1,2,...,N;   i = 1,2,...,M+1;
        self.edges = []           #all edges: horizontal in even lines, vertical below horizontal
        for m in range(2*n +1):
            if m%2 == 0:
                self.edges.append(self.horiz[m//2])
            else:
                self.edges.append(self.vert[(m-1)//2])
        self.edges_width = m + 1
        self.edges_height = 2 * n + 1

def rules(self):
    pass

def is_valid(board):
    
    for i in range(m):
        for j in range(n):
            if board.nums[j][i] != -1:
                if board.nums[j][i] != board.edges[2*j][i] + board.edges[2*j+1][i] + board.edges[2*(j+1)][i] + board.vert[2*j+1][i+1]:
                    return False
    # number of edges around a nonempty cell ( != -1) must equal the number inside the cell
    
    for i in range(m + 1):
        for j in range(n + 1):
            if board.nums[j][i] != -1:
                if i == 0 or j == 0:
                    # Nodes at the borders of the board have less than four incident edges
                    if board.edges[2*j][i] + board.edges[2*j+1][i] not in [0,2]:  
                        return False
                else:
                    if board.edges[2*j][i-1] + board.edges[2*(j-1)+1][i] + board.edges[2*j][i] + board.edges[2*j+1][i] not in [0,2]:
                        return False       
    # every solution forms a cycle without crossings in the grid graph
    # if a node lies on the cycle, both its incident egdes must be == 1
    # for every dot in the grid there can be at most two incident egdes
    # the path is closed so either two or zero edges

def edge_to_cells(row, col):
    if row % 2 == 0:   # horizontal edge
        if row == 0:
            return [(row, col)] #use board.nums[row][col]
        if row == 2 * n + 1:
            return [(row -1, col)]
        else:
            return [(row - 1, col), (row, col)]
    else:
        if col == 0:
            return [(row, col)]
        if col == m + 1:
            return [(row, col -1)]
        else:
            return [(row, col - 1), (row, col)]
            
def cell_to_edges(row, col):
    # the horiz and vert edges surrounding the cell
    A = (row, col)   # upper - horiz
    B = (row + 1, col)   # left - vert
    C = (row + 1, col + 1)   # right - vert
    D = (row + 2, col)   # bottom - horiz
    return [A, B, C, D]

def check_location_is_safe(board, row, col):
    for cell in edge_to_cells(row, col):
        sum_of_edges = 0
        for edge in cell_to_edges(cell[0], cell[1]):
            sum_of_edges += board.edges[edge[0]][edge[1]]
        if board.nums[cell[0]][cell[1]] == -1:
            if sum_of_edges == 4:
                return False
        else:
            if board.nums[cell[0]][cell[1]] < sum_of_edges:
                return False
            

def solve(board):
    pointer = 0
    if pointer == (board.edges_height) * (board.edges_width):
        if is_valid(board):
            return True
        else:
            return False

    # Assigning list values to row and col that we got from the above
    row = int(pointer / (2 * n + 1))
    col = int(pointer % (m + 1))
   
    board.edges[row][col] = 1
    if(check_location_is_safe(board, row, col)):

        pointer += 1
        if(solve(board)):
            return True
        pointer -= 1
        board.nums[row][col] = EMPTY
    return False


if __name__ == "__main__":

    filename = 'input.txt'
    with open(filename, 'r') as fh:
        n, m = map(int, fh.readline().split())
        NUMS = [[int(x) for x in fh.readline().split()]]
        for i in range(1, n):
            NUMS += [[int(x) for x in fh.readline().split()]]

    B = Board()
    solve(B)
    print(B.edges)
    print('nums')
    print(B.nums)







