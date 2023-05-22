import unittest

from hw08_text_search.comprehensions import multiply_by, check_division, div_less, map_zip, word_to_length


class TestComprehensions(unittest.TestCase):

    def setUp(self):
        self.numberList = [-2, -3, 4, 5, 7, 43, 2345, 1343, 13, 40, 24, 221, 5942, 7, 9, 113]
        self.wordList = "All my words are unique and therefore not duplicated".split()

    def test_multiply_by(self):
        expected = [4, 6, -8, -10, -14, -86, -4690, -2686, -26, -80, -48, -442, -11884, -14, -18, -226]
        got = multiply_by(-2, self.numberList)
        self.assertEqual(got, expected)

    def test_check_division(self):
        expected = [False, True, False, False, False, False, False, False, False, False, True, False, False, False,
                    True, False]
        got = check_division(3, self.numberList)
        self.assertEqual(got, expected)

    def test_div_less(self):
        expected = {-2, -3, 5, 7, 43, 1343, 13, 113}
        got = div_less(set(self.numberList))
        self.assertEqual(got, expected)

    def test_map_zip(self):
        expected = {'All': -2, 'my': -3, 'words': 4, 'are': 5, 'unique': 7, 'and': 43, 'therefore': 2345, 'not': 1343,
                    'duplicated': 13}
        got = map_zip(self.wordList, self.numberList)
        expected2 = {-2: 'All', -3: 'my', 4: 'words', 5: 'are', 7: 'unique', 43: 'and', 2345: 'therefore', 1343: 'not',
                     13: 'duplicated'}
        got2 = map_zip(self.numberList, self.wordList)
        self.assertEqual(got, expected)
        self.assertEqual(got2, expected2)

    def test_word_to_length(self):
        expected = {'All': 3, 'words': 5, 'are': 3, 'unique': 6, 'and': 3, 'therefore': 9, 'not': 3, 'duplicated': 10}
        got = word_to_length(self.wordList)
        self.assertDictEqual(got, expected)
