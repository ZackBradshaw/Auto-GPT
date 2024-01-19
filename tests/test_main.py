# tests/test_main.py

# Import necessary modules and functions
import unittest

from my_module import my_function


# Define the test class
class TestMain(unittest.TestCase):
    def test_my_function(self):
        # Test case for my_function
        result = my_function(5)
        self.assertEqual(result, 10, "Incorrect result")

if __name__ == "__main__":
    unittest.main()
