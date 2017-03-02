import unittest
import random
import domki
import generdomki
import string
import numpy.random as nprnd


class TBoard:

    def __init__(self):
        self.nums = [['.', '.', '.', '.', '.', '.', '.', '.']]
        self.nums += [['.', 0, 2, 0, 0, 0, 0, '.']]
        self.nums += [['.', 0, 0, 0, 0, 0, 0, '.']]
        self.nums += [['.', 0, 0, 0, 0, 0, 0, '.']]
        self.nums += [['.', 0, 0, 2, 0, 2, 0, '.']]
        self.nums += [['.', 2, 0, 0, 0, 2, 0, '.']]
        self.nums += [['.', 0, 0, 2, 0, 0, 2, '.']]
        self.nums += [['.', '.', '.', '.', '.', '.', '.', '.']]

        self.upper = [0, 1, 1, 2, 1, 1, 1, 0]
        self.left = [0, 1, 0, 2, 1, 2, 1, 0]
        self.height = 6
        self.width = 6
        self.houses = []


class Board:

    def __init__(self):
        self.nums = [['.', '.', '.', '.', '.', '.', '.', '.']]
        self.nums += [['.', 0, 2, 1, 0, 0, 0, '.']]
        self.nums += [['.', 0, 0, 0, 0, 0, 0, '.']]
        self.nums += [['.', 0, 0, 1, 0, 1, 0, '.']]
        self.nums += [['.', 1, 0, 2, 0, 2, 0, '.']]
        self.nums += [['.', 2, 0, 0, 1, 2, 1, '.']]
        self.nums += [['.', 0, 1, 2, 0, 0, 2, '.']]
        self.nums += [['.', '.', '.', '.', '.', '.', '.', '.']]
        self.upper = [0, 1, 1, 2, 1, 1, 1, 0]
        self.left = [0, 1, 0, 2, 1, 2, 1, 0]
        self.height = 6
        self.width = 6


class Test_check_location_is_safe(unittest.TestCase):

    def test_empty(self):
        B = TBoard()
        row = 1
        col = 1
        self.assertTrue(domki.check_location_is_safe(B, row, col))

    def test_empty2(self):
        B = TBoard()
        row = 1
        col = 2
        self.assertFalse(domki.check_location_is_safe(B, row, col))

    def test_out_of_board2(self):
        B = TBoard()
        row = 0
        col = 2
        self.assertFalse(domki.check_location_is_safe(B, row, col))


class Test_how_many_tanks_row(unittest.TestCase):

    def test_empty(self):
        B = TBoard()
        row = nprnd.randint(1, 7)
        self.assertEqual(domki.how_many_tanks_row(B, row), 0)

    def test_size4(self):
        B = Board()

        check = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 7):
            check[i] += domki.how_many_tanks_row(B, i)
        self.assertEqual(check, B.left)


class Test_how_many_tanks_col(unittest.TestCase):

    def test_empty(self):
        B = TBoard()
        col = nprnd.randint(1, 7)
        self.assertEqual(domki.how_many_tanks_col(B, col), 0)

    def test_size4(self):
        B = Board()
        check = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 7):
            check[i] += domki.how_many_tanks_col(B, i)
        self.assertEqual(check, B.upper)


class Test_is_row_ok(unittest.TestCase):

    def test_empty(self):
        B = TBoard()
        row = nprnd.randint(1, 7)
        self.assertTrue(domki.is_row_ok(B, row))

    def test_solution(self):
        B = Board()
        row = nprnd.randint(1, 7)
        self.assertTrue(domki.is_row_ok(B, row))

    def test_spoil(self):
        B = Board()
        B.nums[2] = ['.', 1, 2, 1, 1, 1, 0, '.']
        row = 2
        self.assertFalse(domki.is_row_ok(B, row))


class Test_is_col_ok(unittest.TestCase):

    def test_empty(self):
        B = TBoard()
        col = nprnd.randint(1, 7)
        self.assertTrue(domki.is_col_ok(B, col))

    def test_solution(self):
        B = Board()
        col = nprnd.randint(1, 7)
        self.assertTrue(domki.is_col_ok(B, col))

    def test_spoil(self):
        B = Board()
        B.nums[1] = ['.', 1, 2, 1, 0, 0, 0, '.']
        col = 1
        self.assertFalse(domki.is_col_ok(B, col))


class Test_Is_Identical(unittest.TestCase):

    def test_tooLong(self):
        list1 = list(nprnd.randint(10, size=(4, 4)))
        list2 = list(nprnd.randint(10, size=(5, 5)))
        self.assertFalse(domki.is_identical(list1, list2))

    def test_size5(self):
        board1 = list(nprnd.randint(5, size=(5, 5)))
        board2 = list(nprnd.randint(5, size=(5, 5)))
        result = True
        for i in range(len(board1)):
            for j in range(len(board1)):
                if board1[i][j] == board2[i][j]:
                    result = False
        self.assertTrue(domki.is_identical(board1, board2) == result)


class Test_is_ok(unittest.TestCase):

    def test_empty(self):
        B = TBoard()
        self.assertTrue(domki.is_ok(B))

    def test_solution(self):
        B = Board()
        self.assertTrue(domki.is_ok(B))

    def test_spoil(self):
        B = Board()
        B.nums[4] = ['.', 1, 0, 2, 1, 2, 0, '.']
        self.assertFalse(domki.is_ok(B))


if __name__ == '__main__':
    unittest.main()
