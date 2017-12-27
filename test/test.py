import unittest

# Add path in order to be able to do imports
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src')
import filecmp  # For file comparison

# Import the price updater
import price_updater


class TestPriceUpdater(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._price_updater = price_updater.PriceUpdater()

    def test_1_three_valid_files_valid_input(self):
        inputs = ['input1.txt', 'input2.txt', 'input3.txt']
        self._price_updater.update_receipts(inputs)

        for input in inputs:
            self.assertEqual(True, filecmp.cmp(
                'expected-output-' + input, 'output-' + input))

    def test_2_single_valid_file_valid_input(self):
        inputs = ['input1.txt']
        self._price_updater.update_receipts(inputs)
        self.assertEqual(True, filecmp.cmp(
            'expected-output-' + inputs[0], 'output-' + inputs[0]))

    def test_2_single_invalid_file_valid_input(self):
        inputs = ['input1.txt']
        self._price_updater.update_receipts(inputs)
        self.assertEqual(True, filecmp.cmp(
            'expected-output-' + inputs[0], 'output-' + inputs[0]))

    # These tests will benefit from a good exception handling policy
    # test_#_single_invalid_file
    # test_#_single_valid_file_invalid_input
    # test_#_1st_valid_2nd_invalid_files_valid_input -> return

    # Tests should be added to test single functions with valid/invalid parameters
    # These test will benefit from moving the functions to a outside price_updater.py
    # For instance:
    # test_#_round_down_0.2
    # test_#_round_up_0.7
    # test_#_round_middle_0.5
    # test_#_round_3.7

    # These tests will be placed in a separate TestCase
    def test_3_is_basic_exempt_valid(self):
        exempt = self._price_updater._is_basic_exempt('book')
        self.assertEqual(True, exempt)

    def test_4_is_basic_exempt_invalid(self):
        exempt = self._price_updater._is_basic_exempt('not exempt')
        self.assertEqual(False, exempt)

    # _update_price() should be tested as well


if __name__ == '__main__':
    unittest.main()
