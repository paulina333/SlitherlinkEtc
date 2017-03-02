import piramidy
import generpiram


def is_solve_correct(input_file, output_file):
    B = piramidy.Board()
    B.read(input_file)
    
    piramidy.solve(B, None)
    
    solution = [[] for _ in range(B.SIZE)]
    with open(output_file, 'r') as fh:
        for i in range(B.SIZE):
            solution[i] = list(map(int, fh.readline().split()))
    if piramidy.is_identical(B.nums, solution):
        return True

def is_generate_correct(size):
    G = generpiram.Board(size)
    generpiram.generate(G)
    print(generpiram.is_okay(G))

if __name__ == '__main__':

    print(is_solve_correct('piramidy.txt', 'solpiramidy.txt'))
    print(is_solve_correct('piramidy2.txt', 'solpiramidy2.txt'))
    is_generate_correct(4)
    is_generate_correct(5)
