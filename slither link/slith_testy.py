import unittest
import itertools as it
import copy
import slith
import genslither


class Board:

    def __init__(self):
        self.nums = []
        self.nums += [[-1] * 6] 
        self.nums += [[-1, 1, -1, 1, -1, -1]]
        self.nums += [[-1, -1, 2, -1, -1, -1]]
        self.nums += [[-1, 3, 1, -1, 2, -1]]
        self.nums += [[-1, 3, -1, -1, 2, -1]]
        self.nums += [[-1] * 6]
        self.nums_height = 6
        self.nums_width = 6
        self.dots = [['.'] * 7] 
        self.dots += [['.', -1, -1, -1, 3, 2, '.']]
        self.dots += [['.', 3, 3, 2, 1, 2, '.']]
        self.dots += [['.', 1, 4, 3, 1, 2, '.']]
        self.dots += [['.', 3, 1, -1, 2, 4, '.']]
        self.dots += [['.', 1, 4, 4, 4, -1, '.']]
        self.dots += [['.'] * 7]


class Board2:

    def __init__(self):
        self.nums = []
        self.nums += [[-1] * 7] 
        self.nums += [[-1, 3, -1, 2, 3, -1, -1]]
        self.nums += [[-1, 2, -1, -1, 2, 1, -1]]
        self.nums += [[-1, 2, -1, -1, -1, 1, -1]]
        self.nums += [[-1, -1, -1, -1, 1, 3, -1]]
        self.nums += [[-1, -1, 1, 1, 3, -1, -1]]
        self.nums += [[-1] * 7]
        self.nums_height = 6
        self.nums_width = 6
        self.dots = [['.'] * 7] 
        self.dots += [['.', 3, 3, 2, 3, 2, -1, '.']]
        self.dots += [['.', 1, 4, 2, 1, 2, -1, '.']]
        self.dots += [['.', -1, 1, 3, 1, 2, -1, '.']]
        self.dots += [['.', 3, 1, 2, 4, 3, 2, '.']]
        self.dots += [['.', 1, 4, 4, 1, 2, 4, '.']]
        self.dots += [['.', -1, -1, -1, 1, 4, -1, '.']]
        self.dots += [['.'] * 7]



class Test_global_check(unittest.TestCase):

    def test_size4x4bad(self):
        B = Board()
        
        edges_taken = set()
        edges_taken.add(((1, 1), (2, 1)))
        edges_taken.add(((1, 1), (1, 2)))
        self.assertFalse(slith.global_check(B, edges_taken))

    def test_size4x4empty(self):
        B = Board()
        
        edges_taken = set()
        self.assertTrue(slith.global_check(B, edges_taken))


class Test_fast_check(unittest.TestCase):

    def test_size4x4bad(self):
        B = Board()
        
        edges_taken = set()
        edges_taken.add(((1, 3), (1, 4)))
        edges_taken.add(((1, 4), (2, 4)))
        self.assertFalse(slith.fast_check(B, edges_taken, (1, 3)))

    def test_size4x4empty(self):
        B = Board()
        
        edges_taken = set()
        self.assertTrue(slith.fast_check(B, edges_taken, (1, 2)))


class Test_find_biggest_tile(unittest.TestCase):

    def test_size4(self):
        B = Board()

        self.assertTrue(slith.find_biggest_tile(B) == ((3, 1), 3))

    def test_size4again(self):
        B = Board()

        B.nums[1] = [-1, 2, 1, -1, 1, -1]
        B.nums[2] = [-1, -1, -1, -1, 2, -1]
        B.nums[3] = [-1, 2, 0, -1, -1, -1]
        B.nums[4] = [-1, -1, -1, -1, 1, -1]
        self.assertTrue(slith.find_biggest_tile(B) == ((1, 1), 2))

class Test_is_drawn(unittest.TestCase):

    def test_negative(self):
        B = Board()
               
        dot1 = (1, 2)
        dot2 = (1, 3)
        self.assertFalse(genslither.is_drawn(B, dot1, dot2))

    def test_negative(self):
        B = Board()
            
        dot1 = (2, 1)
        dot2 = (2, 2)
        self.assertTrue(genslither.is_drawn(B, dot1, dot2))

    def test_out_of_board(self):
        B = Board()
               
        dot1 = (0, 2)
        dot2 = (1, 2)
        self.assertFalse(genslither.is_drawn(B, dot1, dot2))

    def test_out_of_board_nonempty(self):
        B = Board()
               
        dot1 = (0, 4)
        dot2 = (1, 4)
        self.assertFalse(genslither.is_drawn(B, dot1, dot2))

    def test_out_of_board_bottom(self):
        B = Board()
               
        dot1 = (5, 5)
        dot2 = (6, 5)
        self.assertFalse(genslither.is_drawn(B, dot1, dot2))

    def test_out_of_board_bottom_nonempty(self):
        B = Board()
               
        dot1 = (5, 1)
        dot2 = (6, 1)
        self.assertFalse(genslither.is_drawn(B, dot1, dot2))


class Test_count_edges(unittest.TestCase):

    def test_positive(self):
        B = Board()
        original = copy.deepcopy(B.nums)       
        genslither.count_edges(B)
        check = True
        if len(original) != len(B.nums):
            check = False
        for row in range(len(original)):
            for col in range(len(original)):
                if original[row][col] != B.nums[row][col]:
                    if original[row][col] != -1 and B.nums[row][col] != -1:
                        check = False
            
        self.assertTrue(check)

    def test_positive_bigger(self):
        B = Board2()
        original = copy.deepcopy(B.nums)       
        genslither.count_edges(B)
        check = True
        if len(original) != len(B.nums):
            check = False
        for row in range(len(original)):
            for col in range(len(original)):
                if original[row][col] != B.nums[row][col]:
                    if original[row][col] != -1 and B.nums[row][col] != -1:
                        check = False
            
        self.assertTrue(check)

   
if __name__ == '__main__':
    unittest.main()

