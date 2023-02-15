import unittest
from main import *


class TestIsSimilarName(unittest.TestCase):
    """
    Test class for the isSimilarName function.

    Methods:
    test_isSimilarName(self) -- tests the isSimilarName function with several input cases
    """

    def test_isSimilarName(self):
        """
        Test the isSimilarName function.

        Tests:
        - When two strings have similar names
        - When two strings do not have similar names
        """
        self.assertEqual(isSimilarName("kitten", "sitting"), True)
        self.assertEqual(isSimilarName("flaw", "lawn"), True)
        self.assertEqual(isSimilarName("spelling", "peeling"), True)
        self.assertEqual(isSimilarName("mississippi", "misp"), False)


class TestIsCloseProximity(unittest.TestCase):
    """
    Test class for the isCloseProximity function.

    Methods:
    test_isCloseProximity(self) -- tests the isCloseProximity function with several input cases
    """

    def test_isCloseProximity(self):
        """
        Test the isCloseProximity function.

        Tests:
        - When two coordinates are not in close proximity
        - When two coordinates are in close proximity
        """
        self.assertEqual(isCloseProximity((41.49008, -71.312796), (41.49008, -71.312796)), True)
        self.assertEqual(isCloseProximity((41.49008, -71.312796), (41.49008, -74.312796)), False)
        self.assertEqual(isCloseProximity((51.5074, 0.1278), (52.5200, 13.4050)), False)
        self.assertEqual(isCloseProximity((51.5074, 0.1278), (51.5033, -0.1195)), False)


if __name__ == '__main__':
    unittest.main()

"""
This file contains unit tests for the main module.

Classes:
TestIsSimilarName -- tests the isSimilarName function
TestIsCloseProximity -- tests the isCloseProximity function
"""
