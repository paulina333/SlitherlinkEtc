import unittest
import random
import piramidy
import string
import numpy.random as nprnd


class Board:

    def __init__(self, SIZE):
        self.nums = [[0] * SIZE for _ in range(SIZE)]
        self.SIZE = SIZE
        self.upper = []
        self.down = []
        self.left = []
        self.right = []


class Test_check_location_safe(unittest.TestCase):

    def test_zeroes(self):
        B = Board(4)
        row = nprnd.randint(4)
        col = nprnd.randint(4)
        num = nprnd.randint(1, 5)
        self.assertTrue(piramidy.check_location_is_safe(B, row, col, num))

    def test_size4(self):
        B = Board(4)
        B.nums = [[1, 2, 3, 4],  [2, 0, 4, 3],  [3, 4, 1, 2],  [4, 3, 2, 1]]
        num = 1
        col = 1
        row = 1
        self.assertTrue(piramidy.check_location_is_safe(B,  row,  col, num))

    def test_size5(self):
        B = Board(5)
        B.nums = [[1, 2, 3, 4, 5],  [2, 1, 4, 5, 3],  [3, 4, 5, 1, 2],
                  [4, 5, 2, 3, 1],  [5, 3, 1, 2, 4]]
        num = 1
        col = 3
        row = 2
        self.assertFalse(piramidy.check_location_is_safe(B,  row, col, num))


class TestHowManySeen(unittest.TestCase):

    def test_empty(self):
        B = Board(5)
        RR = piramidy.how_many_seen_row_right(B, 1)
        RL = piramidy.how_many_seen_row_left(B, 2)
        CU = piramidy.how_many_seen_col_up(B, 3)
        CD = piramidy.how_many_seen_col_down(B, 4)
        check = [RR, RL, CU, CD]
        self.assertEqual(check, [1, 1, 1, 1])

    def test_size4(self):
        B = Board(4)
        B.nums = [[1, 2, 3, 4],  [2, 1, 4, 3],  [3, 4, 1, 2],  [4, 3, 2, 1]]
        RR = piramidy.how_many_seen_row_right(B, 0)  # 1
        RL = piramidy.how_many_seen_row_left(B, 1)  # 2
        CU = piramidy.how_many_seen_col_up(B, 2)  # 2
        CD = piramidy.how_many_seen_col_down(B, 3)  # 4
        check = [RR, RL, CU, CD]
        self.assertEqual(check, [1, 2, 2, 4])


class TestIsOrderedRow(unittest.TestCase):

    def test_emptyNoClues(self):
        B = Board(5)

        B.left = [-1, -1, -1, -1, -1]
        B.right = [-1, -1, -1, -1, -1]
        row = nprnd.randint(5)
        self.assertTrue(piramidy.is_ordered_row(B, row))

    def test_empty(self):
        B = Board(4)

        B.left = list(nprnd.randint(2, 5, size=4))
        B.right = list(nprnd.randint(2, 5, size=4))
        row = nprnd.randint(4)
        self.assertFalse(piramidy.is_ordered_row(B, row))

    def test_size4(self):
        B = Board(4)
        B.nums = [[2, 1, 4, 3], [3, 4, 2, 1], [1, 2, 3, 4],  [4, 3, 1, 2]]

        B.left = [-1, -1, 4, -1]
        B.right = [-1, 3, -1, -1]
        row = nprnd.randint(4)
        self.assertTrue(piramidy.is_ordered_row(B, row))

    def test_size4(self):
        B = Board(4)
        B.nums = [[4, 1, 2, 3], [3, 2, 4, 1], [1, 4, 3, 2],  [2, 3, 1, 4]]

        B.left = [-1, -1, 4, -1]   # 2
        B.right = [-1, 3, -1, -1]   # 2
        row = nprnd.choice([1, 2])
        self.assertFalse(piramidy.is_ordered_row(B, row))


class TestIsOrderedColumn(unittest.TestCase):

    def test_emptyNoClues(self):
        B = Board(5)
        B.nums = [[1] * 5 for _ in range(5)]   # there can be no 0s
        B.upper = [-1, -1, -1, -1, -1]
        B.down = [-1, -1, -1, -1, -1]

        col = nprnd.randint(0, 5)
        self.assertTrue(piramidy.is_ordered_col(B, col))

    def test_empty(self):
        B = Board(4)
        B.upper = list(nprnd.randint(2, 5, size=4))  # one is always seen
        B.down = list(nprnd.randint(2, 5, size=4))

        col = nprnd.randint(0, 4)
        self.assertFalse(piramidy.is_ordered_col(B, col))

    def test_size4T(self):
        B = Board(4)
        B.nums = [[2, 1, 4, 3], [3, 4, 2, 1], [1, 2, 3, 4],  [4, 3, 1, 2]]
        B.upper = [3, -1, 1, -1]
        B.down = [-1, 2, 3, -1]

        col = nprnd.randint(0, 4)
        self.assertTrue(piramidy.is_ordered_col(B, col))

    def test_size4F(self):
        B = Board(4)
        B.nums = [[4, 1, 2, 3], [3, 2, 4, 1], [1, 4, 3, 2],  [2, 3, 1, 4]]
        B.upper = [3, -1, 1, -1]
        B.down = [-1, 1, -1, -1]

        col = nprnd.choice([0, 1])
        self.assertFalse(piramidy.is_ordered_col(B, col))


class TestIsOrderedBoard(unittest.TestCase):

    def test_emptyNoClues(self):
        B = Board(5)
        B.nums = [[1] * 5 for _ in range(5)]
        B.upper = [-1, -1, -1, -1, -1]
        B.down = [-1, -1, -1, -1, -1]
        B.left = [-1, -1, -1, -1, -1]
        B.right = [-1, -1, -1, -1, -1]

        self.assertTrue(piramidy.is_ordered(B))

    def test_empty(self):
        B = Board(4)
        B.upper = list(nprnd.randint(2, 5, size=4))
        B.down = list(nprnd.randint(2, 5, size=4))
        B.left = list(nprnd.randint(2, 5, size=4))
        B.right = list(nprnd.randint(2, 5, size=4))

        self.assertFalse(piramidy.is_ordered(B))

    def test_size4(self):
        B = Board(4)
        B.nums = [[4, 3, 1, 2], [2, 1, 4, 3], [1, 2, 3, 4],  [3, 4, 2, 1]]
        B.upper = [-1, -1, -1, 3]
        B.down = [-1, 1, -1, -1]
        B.left = [-1, -1, 4, -1]
        B.right = [-1, -1, -1, 3]

        self.assertTrue(piramidy.is_ordered(B))

    def test_size4(self):
        B = Board(4)
        B.nums = [[4, 3, 1, 2], [2, 1, 4, 3], [1, 2, 3, 4],  [3, 4, 2, 1]]
        B.upper = [3, -1, 1, -1]
        B.down = [-1, 1, -1, -1]
        B.left = [-1, -1, 3, -1]
        B.right = [-1, -1, -1, 2]

        self.assertFalse(piramidy.is_ordered(B))


class TestIsIdentical(unittest.TestCase):

    def test_bothempty(self):
        self.assertTrue(piramidy.is_identical([], []))

    def test_empty(self):

        self.assertFalse(piramidy.is_identical([], [1]))

    def test_tooLong(self):
        list1 = list(nprnd.randint(10, size=(4, 4)))
        list2 = list(nprnd.randint(10, size=(5, 5)))
        self.assertFalse(piramidy.is_identical(list1, list2))

    def test_size2(self):
        board1 = list(nprnd.randint(2, size=(2, 2)))
        board2 = list(nprnd.randint(2, size=(2, 2)))
        result = True
        for i in range(len(board1)):
            for j in range(len(board1)):
                if board1[i][j] == board2[i][j]:
                    result = False
        self.assertTrue(piramidy.is_identical(board1, board2) == result)

    def test_size5(self):
        board1 = list(nprnd.randint(5, size=(5, 5)))
        board2 = list(nprnd.randint(5, size=(5, 5)))
        result = True
        for i in range(len(board1)):
            for j in range(len(board1)):
                if board1[i][j] == board2[i][j]:
                    result = False
        self.assertTrue(piramidy.is_identical(board1, board2) == result)


suite1 = unittest.TestLoader().loadTestsFromTestCase(Test_check_location_safe)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestHowManySeen)
suite3 = unittest.TestLoader().loadTestsFromTestCase(TestIsOrderedRow)
suite4 = unittest.TestLoader().loadTestsFromTestCase(TestIsOrderedColumn)
suite5 = unittest.TestLoader().loadTestsFromTestCase(TestIsOrderedBoard)
suite6 = unittest.TestLoader().loadTestsFromTestCase(TestIsIdentical)

print(unittest.TextTestRunner(verbosity=3).run(suite1))
print(unittest.TextTestRunner(verbosity=3).run(suite2))
print(unittest.TextTestRunner(verbosity=3).run(suite3))
print(unittest.TextTestRunner(verbosity=3).run(suite4))
print(unittest.TextTestRunner(verbosity=3).run(suite5))
print(unittest.TextTestRunner(verbosity=3).run(suite6))

