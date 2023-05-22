from unittest import TestCase
# depending on whether your model_lang.py script is found within the same folder with 
# this script and whether you have defined the src folder as the Source Root in PyCharm, you 
# might need to change the following import to remove hw04_nltk
from hw04_nltk.model_lang import LangModeler
import nltk
nltk.download('udhr')
from nltk.corpus import udhr

class LangGuesserTest(TestCase):

  def setUp(self):
    languages = ['English', 'German_Deutsch', 'French_Francais']

    # udhr corpus contains the Universal Declaration of Human Rights in over 300 languages
    language_base = dict((language, udhr.words(language + '-Latin1')) for language in languages)

    # build the language models
    self.langModeler = LangModeler(languages, language_base)

  def test_01_build_language_models(self):
    language_model_cfd = self.langModeler.build_language_models()
    some_word_counts_inEnglish = [language_model_cfd['English'][w] for w in ['universal','declaration','of']]
    self.assertEqual(some_word_counts_inEnglish, [5,6,81])

  def test_02_guess_language(self):
    text1 = "Peter had been to the office before they arrived."
    text2 = "Si tu finis tes devoirs, je te donnerai des bonbons."
    text3 = "Das ist ein schon recht langes deutsches Beispiel."
    language_model_cfd = self.langModeler.build_language_models()

    self.assertEqual(self.langModeler.guess_language(language_model_cfd, text1), 'English')
    self.assertEqual(self.langModeler.guess_language(language_model_cfd, text2), 'French_Francais')
    self.assertEqual(self.langModeler.guess_language(language_model_cfd, text3), 'German_Deutsch')



