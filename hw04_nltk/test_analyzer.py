import os
from unittest import TestCase
# depending on whether your analyze.py script is found within the same folder with 
# this script and whether you have defined the src folder as the Source Root in PyCharm, you 
# might need to change the following import to remove hw04_nltk
from hw04_nltk.analyze import Analyzer
from nltk import FreqDist

class AnalyzerTest(TestCase):

  def setUp(self):
    # make sure that the path to the folder data corresponds the path in your computer
    path = os.path.join(os.path.dirname(__file__), "ada_lovelace.txt")
    self.analyzer = Analyzer(path)

  def constructor(self):
    self.assertEqual(type(self.analyzer.token_counts), FreqDist)

  def test_01_numberOfTokens(self):
    self.assertEqual(self.analyzer.numberOfTokens(), 4506)

  def test_02_size(self):
    self.assertEqual(self.analyzer.vocabularySize(),1390)

  def test_03_diversity(self):
    self.assertEqual(round(self.analyzer.lexicalDiversity(), 4), 0.3085)

  def test_04_get_keywords(self):
    self.assertEqual(self.analyzer.getKeywords()[:3],['Analytical', 'Annabella', 'Lovelace'])

  def test_05_numberOfHapaxes(self):
    self.assertEqual(self.analyzer.numberOfHapaxes(),936)

  def test_06_avWordLength(self):
    self.assertEqual(int(self.analyzer.avWordLength()),6)
