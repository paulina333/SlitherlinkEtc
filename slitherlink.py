class slither:
    def __init__(self, file):
        self.board = []                               # empty <--> -1
        with open(file) as f:
            for line in f:
                line = line.split()
                self.board.append(line)
        self.height = len(self.board)                       # M dots widthwise
        self.width = len(self.board[0])                    # N dots heightwise
        # j = row, i = column
        # 0 <-> the edge isn't included in the cycle, 1 <-> it is included,
       
        self.vert = [[j for i in range(self.width +1)] for j in range(self.height)]  
        # there are (M+1) vertical edges widthwise, N heightwise
        # j=1,2,...,N;   i = 1,2,...,M+1;
        self.horiz = [[0 for i in range(self.width)] for j in range(self.height + 1)]
        # M horizontal edges widthwise, N+1 heightwise
        # j=1,2,...,N;   i = 1,2,...,M+1;
        self.edges = []           #all edges: horizontal in even lines, vertical below horizontal
        for m in range(2*self.height +1):
            if m%2 == 0:
                self.edges.append(self.horiz[m//2])
            else:
                self.edges.append(self.vert[(m-1)//2])

    def rules(self):
        pass
    
    def is_valid(self):
        
        ok = True
        
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] != -1:
                    if self.board[j][i] != self.horiz[j][i] + self.vert[j][i] + self.horiz[j+1][i] + self.vert[j][i+1]:
                        ok = False
        # number of edges around a nonempty cell ( != -1) must equal the number inside the cell
        
        for i in range(self.width + 1):
            for j in range(self.height + 1):
                if self.board[j][i] != -1:
                    if i == 0 or j == 0:
                        # Nodes at the borders of the board have less than four incident edges
                        if self.horiz[j][i] + self.vert[j][i] not in [0,2]:  
                            ok = False
                    else:
                        if self.horiz[j][i-1] + self.vert[j-1][i] + self.horiz[j][i] + self.vert[j][i] not in [0,2]:
                            ok = False       
        # every solution forms a cycle without crossings in the grid graph
        # if a node lies on the cycle, both its incident egdes must be == 1
        # for every dot in the gris there can be at most two incident egdes
        # the path is closed so either two or zero edges
        return ok

game = slither("input.txt")

