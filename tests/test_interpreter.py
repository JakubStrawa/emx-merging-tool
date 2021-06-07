import unittest
from interpreter import Interpreter


class TestInterpreter(unittest.TestCase):
    def test_interpreter1(self):
        interpreter1 = Interpreter("test_files/2 - only one empty class.emx", "test_files/2 - only one empty class.emx", 1, 0, None, "interpreter1_output.emx")
        file1 = open("interpreter1_output.emx", 'r')
        file1_expected = open("interpreter1_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter2(self):
        interpreter2 = Interpreter("test_files/2 - only one empty class.emx", "test_files/2,5 - only one empty class with conflicts.emx", 1, 0, None, "interpreter2_output.emx")
        file1 = open("interpreter2_output.emx", 'r')
        file1_expected = open("interpreter2_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter3(self):
        interpreter3 = Interpreter("test_files/3 - one class with one attribute.emx", "test_files/3,5 - one class with one attribute with conflicts.emx", 1, 0, None, "interpreter3_output.emx")
        file1 = open("interpreter3_output.emx", 'r')
        file1_expected = open("interpreter3_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter4(self):
        interpreter4 = Interpreter("test_files/4 - one class, one attribute with all options.emx", "test_files/4,5 - one class, one attribute with all options with conflicts.emx", 1, 0, None, "interpreter4_output.emx")
        file1 = open("interpreter4_output.emx", 'r')
        file1_expected = open("interpreter4_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter5(self):
        interpreter5 = Interpreter("test_files/5 - one class with one attribute and method, all opotions.emx", "test_files/5,5 - one class with one attribute and method, all opotions with conflicts.emx", 1, 0, None, "interpreter5_output.emx")
        file1 = open("interpreter5_output.emx", 'r')
        file1_expected = open("interpreter5_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter6(self):
        interpreter6 = Interpreter("test_files/6 - one class with attribute, metod with return value, all options.emx", "test_files/6,5 - one class with attribute, metod with return value, all options with conflicts.emx", 1, 0, None, "interpreter6_output.emx")
        file1 = open("interpreter6_output.emx", 'r')
        file1_expected = open("interpreter6_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter7(self):
        interpreter7 = Interpreter("test_files/7 - one class, one atribute and method with all possible parameters.emx", "test_files/7,5 - one class, one atribute and method with all possible parameters with conflicts.emx", 1, 0, None, "interpreter7_output.emx")
        file1 = open("interpreter7_output.emx", 'r')
        file1_expected = open("interpreter7_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter8(self):
        interpreter8 = Interpreter("test_files/8 - one class, multiple parameters, method, all options.emx", "test_files/8,5 - one class, multiple parameters, method, all options with conflicts.emx", 1, 0, None, "interpreter8_output.emx")
        file1 = open("interpreter8_output.emx", 'r')
        file1_expected = open("interpreter8_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter9(self):
        interpreter6 = Interpreter("test_files/9 - two classes, one complex, one simplest.emx", "test_files/9,5 - two classes, one complex, one simplest with conflicts.emx", 1, 0, None, "interpreter9_output.emx")
        file1 = open("interpreter9_output.emx", 'r')
        file1_expected = open("interpreter9_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()

    def test_interpreter10(self):
        interpreter10 = Interpreter("test_files/10 - 3 classes, complex with generalizations and association.emx", "test_files/10,5 - 3 classes, complex with generalizations and association with conflicts.emx", 1, 0, None, "interpreter10_output.emx")
        file1 = open("interpreter10_output.emx", 'r')
        file1_expected = open("interpreter10_expected_output.emx", 'r')
        line1 = file1.readline()
        line1_expected = file1_expected.readline()
        self.assertEqual(line1, line1_expected)
        while line1:
            line1 = file1.readline()
            line1_expected = file1_expected.readline()
            self.assertEqual(line1, line1_expected)
        file1.close()
        file1_expected.close()
