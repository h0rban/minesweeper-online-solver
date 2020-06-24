from Posn import Posn
from unittest import TestCase


# examples and tests
class Test(TestCase):

    # test for Posn
    def test_posn(self):

        # in_range
        self.assertFalse(Posn(1, 10).in_range(5, 5))
        self.assertFalse(Posn(10, 1).in_range(5, 5))
        self.assertFalse(Posn(10, 10).in_range(5, 5))
        self.assertFalse(Posn(-3, 10).in_range(5, 5))
        self.assertFalse(Posn(-10, 10).in_range(5, 5))
        self.assertFalse(Posn(2, -10).in_range(5, 5))
        self.assertFalse(Posn(-5, -5).in_range(5, 5))
        self.assertFalse(Posn(5, 5).in_range(5, 5))

        self.assertTrue(Posn(1, 1).in_range(5, 5))
        self.assertTrue(Posn(1, 3).in_range(5, 5))
        self.assertTrue(Posn(3, 1).in_range(5, 5))
        self.assertTrue(Posn(0, 0).in_range(5, 5))
        self.assertTrue(Posn(0, 4).in_range(5, 5))
        self.assertTrue(Posn(4, 0).in_range(5, 5))
        self.assertTrue(Posn(4, 4).in_range(5, 5))

        # surrounding
        self.assertEqual(Posn(0, 0).surrounding(),
                         [Posn(-1, -1), Posn(-1, 0), Posn(-1, 1),
                          Posn(0, -1), Posn(0, 1),
                          Posn(1, -1), Posn(1, 0), Posn(1, 1)])
        self.assertEqual(Posn(10, 10).surrounding(),
                         [Posn(9, 9), Posn(9, 10), Posn(9, 11),
                          Posn(10, 9), Posn(10, 11),
                          Posn(11, 9), Posn(11, 10), Posn(11, 11)])

        # surrounding_in_range
        self.assertEqual(Posn(0, 0).surrounding_in_range(0, 0), [])
        self.assertEqual(Posn(0, 0).surrounding_in_range(1, 1), [])
        self.assertEqual(Posn(0, 0).surrounding_in_range(2, 2),
                         [Posn(0, 1), Posn(1, 0), Posn(1, 1)])
        self.assertEqual(Posn(10, 10).surrounding_in_range(100, 100),
                         Posn(10, 10).surrounding())
        self.assertEqual(Posn(10, 10).surrounding_in_range(11, 11),
                         [Posn(9, 9), Posn(9, 10),
                          Posn(10, 9)])

        # equal
        self.assertTrue(Posn(10, 10).__eq__(Posn(10, 10)))
        self.assertTrue(Posn(3, 3).__eq__(Posn(3, 3)))
        self.assertFalse(Posn(0, 0).__eq__(Posn(1, 0)))
        self.assertFalse(Posn(0, 0).__eq__(Posn(0, 1)))
        self.assertFalse(Posn(0, 0).__eq__(Posn(1, 1)))
        self.assertFalse(Posn(0, 0).__eq__(Posn(-1, -1)))
        self.assertFalse(Posn(0, 0).__eq__(5))
        self.assertFalse(Posn(0, 0).__eq__('hi'))

        # str
        self.assertEqual(Posn(0, 0).coordinates(), '(0, 0)')
        self.assertEqual(Posn(3, 4).coordinates(), '(4, 3)')
        self.assertEqual(str(Posn(0, 0)), 'Posn(row = 0, col = 0)')
        self.assertEqual(str(Posn(3, 4)), 'Posn(row = 3, col = 4)')
