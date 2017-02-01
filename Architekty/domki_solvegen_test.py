import domki
import generdomki


def is_solve_correct(input_file, output_file):
    T = domki.Board()
    T.read(input_file)

    T.houses = T.find_houses()

    domki.solve(T, None, i=0)

    solution = [[] for _ in range(T.width + 2)]
    solution[0] = ['.'] * (T.width + 2)
    with open(output_file, 'r') as fh:
        for i in range(1, T.height + 1):
            solution[i] = ['.'] + list(map(int, fh.readline().split())) + ['.']
    solution[T.width + 1] = ['.'] * (T.width + 2)
    if domki.is_identical(T.nums, solution):
        return True


def is_generate_correct(height, width):
    ok = False

    while True:
        T = generdomki.Board(height, width)
        T.generate_board()

        T.houses = sorted(T.get_houses(5))

        generdomki.generate(T, i=0)
        generdomki.print_puzzle(T)
        generdomki.puzzle_to_txt(T)

        B = domki.Board()
        B.read('architekt_puzz.txt')
        hh = []
        for i in range(B.height + 2):
            for j in range(B.width + 2):
                if B.nums[i][j] == 2:
                    hh.append([i, j])
        B.houses = hh

        if domki.solve(B, T.nums, i=0) is False:  # is there a unique solution
            ok = True
            break
        else:
            ok = False
    return ok


if __name__ == '__main__':

    print(is_solve_correct('architekt.txt', 'solarchitekt.txt'))
    print(is_solve_correct('architekt2.txt', 'solarchitekt2.txt'))
    print(is_solve_correct('architekt3.txt', 'solarchitekt3.txt'))
    print(is_solve_correct('architekt4.txt', 'solarchitekt4.txt'))

    for _ in range(5):
        print(is_generate_correct(6, 6))
    for _ in range(5):
        print(is_generate_correct(5, 5))
