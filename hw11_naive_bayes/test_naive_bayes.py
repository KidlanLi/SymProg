from unittest import TestCase
from hw11_naive_bayes.naive_bayes_classifier import DataInstance, Dataset, NaiveBayesClassifier

training_inst = [DataInstance.from_list_of_feature_occurrences(sample[0], sample[1]) for sample in
                 [('meeting tomorrow meeting lecture'.split(' '), 'relevant'),
                  ('lecture free free free best best'.split(' '), 'promotions'),
                  ('best free hot hot hot single single beach'.split(' '), 'spam'),
                  ('meeting lecture morning morning'.split(' '), 'relevant'),
                  ('lecture professor work work'.split(' '), 'relevant'),
                  ('single top free hot'.split(' '), 'spam')]]

test_inst_1 = [DataInstance.from_list_of_feature_occurrences(sample[0], sample[1]) for sample in
               [('meeting lecture'.split(' '), 'relevant'),
                ('best lecture best'.split(' '), 'promotions'),
                ('best hot beach'.split(' '), 'spam'),
                ('tomorrow document'.split(' '), 'relevant'),
                ('work'.split(' '), 'relevant'),
                ('cream single beach'.split(' '), 'promotions')]]

training_inst_2 = [DataInstance.from_list_of_feature_occurrences(sample[0], sample[1]) for sample in
                   [('meeting tomorrow meeting lecture'.split(' '), 'relevant'),
                    ('lecture free free free best best'.split(' '), 'promotions'),
                    ('best free hot hot hot single single beach'.split(' '), 'spam'),
                    ('meeting lecture tomorrow tomorrow tomorrow tomorrow morning morning'.split(' '), 'relevant'),
                    ('lecture professor work work work work work work work work work'.split(' '), 'relevant'),
                    ('single top free hot'.split(' '), 'spam')]]

class NaiveBayesTest(TestCase):

    def setUp(self):
        self.data_set_1 = Dataset(training_inst)
        self.data_set_2 = Dataset(test_inst_1)
        self.data_set_3 = Dataset(training_inst_2)
        self.nbc = NaiveBayesClassifier.for_dataset(self.data_set_1, smoothing = 1.0)
        self.nbc2 = NaiveBayesClassifier.for_dataset(self.data_set_3, smoothing = 1.0)

    def test01_from_list_of_feature_occurrences_01(self):
        """Checking if Data instance is created correctly"""
        feature_list= ['buy','free','buy', 'for', 'buy', 'free']
        label = 'promotions'
        instance = DataInstance.from_list_of_feature_occurrences(feature_list,label)
        self.assertEqual(instance.label,label)
        self.assertEqual(instance.feature_counts,{'buy':3,'for':1,'free':2})

    def test02_for_dataset_01(self):
        """Checking if a NaiveBayesClassifier is constructed correctly for a dataset."""
        self.assertEqual(self.nbc.word_and_cat_to_count,{('lecture', 'promotions'): 1, ('morning', 'relevant'): 2, ('single', 'spam'): 3,('work', 'relevant'): 2, ('beach', 'spam'): 1,\
                                                    ('lecture', 'relevant'): 3, ('professor', 'relevant'): 1, ('free', 'spam'): 2, ('best', 'promotions'): 2, ('tomorrow', 'relevant'): 1, \
                                                    ('top', 'spam'): 1, ('best', 'spam'): 1, ('meeting', 'relevant'): 3, ('hot', 'spam'): 4, ('free', 'promotions'): 3})
        self.assertEqual(self.nbc.cat_to_num_words, {'spam': 12, 'promotions': 6, 'relevant': 12})
        self.assertEqual(self.nbc.vocabsize, 12)
        self.assertAlmostEqual(self.nbc.category_to_prior['spam'], 0.33333333)
        self.assertAlmostEqual(self.nbc.category_to_prior['relevant'], 0.5)
        self.assertAlmostEqual(self.nbc.category_to_prior['promotions'], 0.16666667)
        self.assertEqual(self.nbc.smoothing, 1.0)

    def test03_prediction_01(self):
        """Checking if the class 'string' was correctly predicted"""
        self.assertEqual([self.nbc.prediction(inst.feature_counts) for inst in self.data_set_2.instance_list],['relevant','promotions','spam','relevant','relevant','spam'])

    def test04_prediction_accuracy_01(self):
        """Checking if the prediction accuracy of the classifier is correct"""
        self.assertAlmostEqual(self.nbc.prediction_accuracy(self.data_set_2),0.8333333)

    def test05_log_odds_for_word_01(self):
        """Checking if log-odds value of each word is computed correctly"""
        self.assertAlmostEqual(self.nbc.log_odds_for_word('hot', 'spam'), 0.83624802)
        self.assertAlmostEqual(self.nbc.log_odds_for_word('single', 'relevant'), -1.13497993)

    def test06_features_for_category_01(self):
        """Checking if the words with the highest log-odds are retrieved correctly"""
        testPassed = self.nbc2.features_for_category("relevant") == ['work','tomorrow', 'meeting', 'morning', 'lecture', 'professor'] or \
        self.nbc2.features_for_category("relevant") == ['work','tomorrow', 'meeting', 'lecture', 'morning', 'professor']
        self.assertEqual(True,testPassed)
