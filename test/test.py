import unittest

# Add path in order to be able to do imports
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src')
import filecmp  # For file comparison

# Import the price updater
import price_updater


class TestPausesExtraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._price_updater = price_updater.PriceUpdater()

    def test_1_all_input(self):
        inputs = ['input1.txt', 'input2.txt', 'input3.txt']
        self._price_updater.update_receipts(inputs)

        for input in inputs:
            self.assertEqual(True, filecmp.cmp(
                'expected-output-' + input, 'output-' + input))

if __name__ == '__main__':
    unittest.main()
