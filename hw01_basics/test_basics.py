import unittest
from unittest import TestCase, mock

import io

from hw01_basics.basics import *


class TestBasics(TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, f, n, m, expected_output, mock_stdout):
        if m is not None:
            f(n, m)
        elif n is not None:
            f(n)
        else:
            f()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def setUp(self):
        self.listOne = ["Germany", "Spain", "Italy", "Poland", "France"]
        self.listTwo = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
        self.listThree = [5, 4, 8, 6]

    def test_hello_semester(self):
        """ Print the string 'Welcome to "Symbolische Programmierung" WS 22/23'.
        Welcome to "Symbolische Programmierung" WS 22/23
        """

        self.assert_stdout(hello_semester, None, None, "Welcome to \"Symbolische Programmierung\" WS 22/23\n")

    def test_modulo(self):
        """ Return the value x modulo y (i.e., do NOT print it)."""
        self.assertEqual(modulo(5, 3), 2)
        self.assertEqual(modulo(100, 24), 4)
        self.assertEqual(modulo(70, 7), 0)

    def test_odd_number(self):
        """ Return True or False whether x is odd or not. """
        self.assertEqual(odd_number(15), True)
        self.assertEqual(odd_number(6), False)
        self.assertEqual(odd_number(-3), True)

    # ===STRING OPERATIONS====================================================

    def test_happy_birthday(self):
        """ Print "Happy >age<th birthday, >name<!". """
        self.assert_stdout(happy_birthday, "Peter", "17", "Happy 17th birthday, Peter!\n")

    def test_word_multiplier(self):
        """ Return a word multiplied n times. """
        self.assertEqual(word_multiplier("Cheese", 3), "CheeseCheeseCheese")

    def test_reverse(self):
        """ Return the reverse of a word. """
        self.assertEqual(reverse("ABCDE"), 'EDCBA')
        self.assertEqual(reverse("Info"), 'ofnI')
        self.assertEqual(reverse("enoD lleW"), 'Well Done')
        self.assertEqual(reverse("12345"), '54321')

    def test_every_nth(self):
        """ Return every nth letter of w word """
        self.assertEqual(every_nth("Ich", 2), 'Ih')

    # ===LIST OPERATIONS====================================================
    def test_second_element(self):
        """ Return the second element of a list. """
        self.assertEqual(second_element(self.listOne), 'Spain')

    def test_concatenate_lists(self):
        """ Return the concatenation of both lists. """
        self.assertEqual(concatenate_lists(self.listOne, self.listTwo),
                         ['Germany', 'Spain', 'Italy', 'Poland', 'France', 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5])

    def test_swap_half(self):
        """ Swaps the first half of a list with the second half of the list.
        If the length of the list is odd, then the first half has one less element than the second half. """
        self.assertEqual(swap_half(self.listOne), ['Italy', 'Poland', 'France', 'Germany', 'Spain'])

    def test_replace_elements(self):
        """ Replace the elements in list_a at the positions given in replacement_indices with new_value, and return the
        result.
        """
        self.assertEqual(replace_elements([1, 2, 3, 4, 5, 6, 7, 8], [0, 4, 3], 0), [0, 2, 3, 0, 0, 6, 7, 8])

    def test_long_strings(self):
        """ Takes a list of strings, and returns a list of booleans. Each boolean indicates whether the length of the
         corresponding string is longer than max_length (True). If a string's length is max_length or shorter, the
         corresponding return value is false.
        """
        self.assertEqual(long_strings(listOne, 5), [True, False, False, True, True])

    # ===LOOP OPERATIONS====================================================

    def test_print_squares(self):
        """ Print the square values of each element in the list. You can use a for-loop for this problem. """
        self.assert_stdout(print_squares, self.listThree, None, "25\n16\n64\n36\n")

    def test_count_to_k(self):
        """ Print out the numbers counting from 0 to k, excluding k.
            If k is negative, count 'down' from 0, excluding 0.
            You can use a while-loop for this problem or the range(x,y,z) function. """
        self.assert_stdout(count_to_k, 3, None, "0\n1\n2\n")
        self.assert_stdout(count_to_k, -2, None, "-1\n-2\n")

    # ===REGULAR EXPRESSIONS====================================================


    def test_no_numbers(self):
        """ Return True or False whether w contains no numbers. """
        self.assertEqual(no_numbers("Guten Tag!"), True)
        self.assertEqual(no_numbers("42 ist eine tolle Zahl"), False)

    def test_contains_substring(self):
        """ Return True or False whether w contains a certain substring. """
        self.assertEqual(contains_substring("Salat", "S a l a t"), False)
        self.assertEqual(contains_substring("Apfel", "Apfelkuchen"), True)

        # =======================================================
