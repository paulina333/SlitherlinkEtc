from slith import *


def is_solve_correct(input_file):

    B = Board()
    B.read(input_file)

    biggest_tile, biggest_tile_val = find_biggest_tile(B)

    found_solution = False
    for begining_offsets in ALL_DIRS:

        begin_i = biggest_tile[0] + begining_offsets[0]
        begin_j = biggest_tile[1] + begining_offsets[1]
        if backtrack(B, edges_taken=None, i=begin_i, j=begin_j,
                     begin_i=begin_i, begin_j=begin_j):
            found_solution = True
            break
    if found_solution:
        C = Board()
        C.read(input_file)

        biggest_tile, biggest_tile_val = find_biggest_tile(C)

        found_solution = False
        for begining_offsets in ALL_DIRS:
            begin_i = biggest_tile[0] + begining_offsets[0]
            begin_j = biggest_tile[1] + begining_offsets[1]
            backtrack(C, edges_taken=None, i=begin_i, j=begin_j,
                      begin_i=begin_i, begin_j=begin_j, end_if_found=False)
            if C.solutions != 0:
                break

        if C.solutions > 2:
            return False
        else:
            return True
    else:
        return False


if __name__ == '__main__':

    print(is_solve_correct('slith3_5x5.txt') is True)
    print(is_solve_correct('testowa4x4.txt') is True)
    print(is_solve_correct('slith2_4x6.txt') is True)
    print(is_solve_correct('nosolution.txt') is False)
