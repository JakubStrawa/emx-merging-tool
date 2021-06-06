import unittest
from interpreter import Interpreter


class TestInterpreter(unittest.TestCase):
    def test_interpreter1(self):
        interpreter1 = Interpreter("test_files/2 - only one empty class.emx", "test_files/2 - only one empty class.emx", 1, 0, None, "interpreter1_output.txt")
        file1 = open("interpreter1_output.txt", 'r')
        file1_expected = open("interpreter1_expected_output.txt", 'r')
        for i in range(6):
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        # skip graphics
        for i in range(18):
            line1 = file1.readline()
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter2(self):
        interpreter2 = Interpreter("test_files/2 - only one empty class.emx", "test_files/2,5 - only one empty class with conflicts.emx", 1, 0, None, "interpreter2_output.txt")
        file1 = open("interpreter2_output.txt", 'r')
        file1_expected = open("interpreter2_expected_output.txt", 'r')
        for i in range(6):
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        # skip graphics
        for i in range(18):
            line1 = file1.readline()
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()
