from os.path import join, dirname
from unittest import TestCase
from nltk.corpus import wordnet
from hw07_wordnet.noun_similarity import get_similarity_scores
from hw07_wordnet.find_hyponyms import HyponymSearcher


class WordnetTest(TestCase):

    def setUp(self):
        self.hyponymSearcher = HyponymSearcher(join(dirname(__file__), "ada_lovelace.txt"))

    def test_01_noun_similarity(self):
        pairs = [('car', 'automobile'), ('gem', 'jewel'), ('journey', 'voyage'),
                 ('boy', 'lad'), ('coast', 'shore'), ('asylum', 'madhouse'), ('magician', 'wizard'),
                 ('midday', 'noon'), ('furnace', 'stove'), ('food', 'fruit'), ('bird', 'cock'),
                 ('bird', 'crane'), ('tool', 'implement'), ('brother', 'monk'), ('lad', 'brother'),
                 ('crane', 'implement'), ('journey', 'car'), ('monk', 'oracle'), ('cemetery', 'woodland'),
                 ('food', 'rooster'), ('coast', 'hill'), ('forest', 'graveyard'), ('shore', 'woodland'),
                 ('monk', 'slave'), ('coast', 'forest'), ('lad', 'wizard'), ('chord', 'smile'), ('glass', 'magician'),
                 ('rooster', 'voyage'), ('noon', 'string')]
        results = get_similarity_scores(pairs)
        sim_of_car = [(pair, sim) for pair, sim in results if pair =='car-automobile'][0]
        sim_of_voyage = [(pair, sim) for pair, sim in results if pair =='journey-voyage'][0]
        self.assertEqual(sim_of_car,('car-automobile', 1.0))
        self.assertEqual(sim_of_voyage,('journey-voyage', 0.5))


    def test_02_lemma_names(self):
        self.assertEqual(len(self.hyponymSearcher.noun_lemmas), 1262)

    def test_03_hypernymOF(self):
        son = wordnet.synsets("son", pos="n")[0]
        relative = wordnet.synsets("relative", pos='n')[0]
        self.assertTrue(self.hyponymSearcher.hypernym_of(son, relative))

    def test_04_hyponyms(self):
        #find words that are hyponyms to the following three synsets
        relative = wordnet.synsets("relative", pos='n')[0]
        science = wordnet.synsets("science", pos='n')[0]
        illness = wordnet.synsets("illness", pos='n')[0]

        hypos_relative = self.hyponymSearcher.get_hyponyms(relative)
        hypos_science = self.hyponymSearcher.get_hyponyms(science)
        hypos_illness = self.hyponymSearcher.get_hyponyms(illness)

        self.assertTrue("father" in hypos_relative)
        self.assertTrue("half-sister" in hypos_relative)
        self.assertTrue("husband" in hypos_relative)

        self.assertTrue("calculus" in hypos_science)
        self.assertTrue("math" in hypos_science)
        self.assertTrue("anatomy" in hypos_science)

        self.assertTrue("cancer" in hypos_illness)
        self.assertTrue("disease" in hypos_illness)
        self.assertTrue("illness" in hypos_illness)
