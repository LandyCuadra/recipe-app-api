"""
Sample tests
"""

from django.test import SimpleTestCase

from app.calc import add, subtract


class CalcTest(SimpleTestCase):
    """ Test calculator module """

    def test_add_number(self):
        """ Test add function """
        self.assertEqual(add(5, 6), 11)

    def test_subtract_number(self):
        """ Test subtract function """
        self.assertEqual(subtract(15, 10), 5)
