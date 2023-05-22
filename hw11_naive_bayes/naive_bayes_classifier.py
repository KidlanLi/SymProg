from collections import defaultdict
from nltk import word_tokenize
from nltk import FreqDist
import sys
import math

def normalized_tokens(text):
    return [token.lower() for token in word_tokenize(text)]

class DataInstance:
    def __init__(self, feature_counts, label):
        """ A data instance consists of a dictionary with feature counts (string -> int) and a label (True or False)."""
        self.feature_counts = feature_counts
        self.label = label

    @classmethod
    def from_list_of_feature_occurrences(cls, feature_list, label):
        """ Creates feature counts for all features in the list."""
        feature_counts = FreqDist(feature_list)
        # TODO: Exercise 1: Create a dictionary that contains for each feature in the list the count how often it occurs.
        return cls(feature_counts, label)

    @classmethod
    def from_text_file(cls, filename, label):
        with open(filename, 'r') as myfile:
            token_list = normalized_tokens(myfile.read().strip())
        return cls.from_list_of_feature_occurrences(token_list, label)

class Dataset:
    def __init__(self, instance_list):
        """ A data set is defined by a list of instances. Here, each instance of the list
        is accessed and the keys of its feature_counts dictionary are added to the set feature_set.
        So, the attribute feature_set contains all words of all data instances (i.e., of all documents)"""
        self.instance_list = instance_list
        self.feature_set = set.union(*[set(inst.feature_counts.keys()) for inst in instance_list])


class NaiveBayesClassifier:
    def __init__(self, word_and_category_to_count, category_to_num_instances, vocabsize, smoothing):
        """ Creates a Naive Bayes-Classifier. The following parameters are used:
        word_and_category_to_count: (dict) how often does a word occur in a category. The keys are pairs of (word, category) and the values are the frequency of (word,category).
        category_to_num_instances: (dict) how many instances/words are there per category. The keys are the categories and the values the number of instances.
        vocabsize: overall size of feature set (= vocabulary)
        smoothing: laplace parameter, added to counts for each word when calculating probabilities
        """
        self.word_and_cat_to_count = word_and_category_to_count
        # cat_to_num_words is a dict: how many words occur in each category. The keys are the categories and the values are the count of all words in that category.
        self.cat_to_num_words = defaultdict(int)
        for (word, cat), count in word_and_category_to_count.items():
            self.cat_to_num_words[cat] += count
        self.vocabsize = vocabsize
        # total_instances: all instances of all categories
        total_instances = sum(category_to_num_instances.values())
        # category_to_prior is a dict: what is the prior probability for each category. The keys are the categories and the values the prior probabilities.
        self.category_to_prior = {c: n/total_instances for c, n in category_to_num_instances.items()}
        self.smoothing = smoothing

    @classmethod
    def for_dataset(cls, dataset, smoothing = 1.0):
        """ Creates a NB-Classifier for a dataset."""
        # (str,str) -> int
        word_and_category_to_count = defaultdict(int) # maps tuples (word, category) to the number of occurences (of a word in a that category)
        # str -> int
        category_to_num_instances = defaultdict(int) # maps a category name to the number of instances in that category
        vocabsize = len(dataset.feature_set)
        for inst in dataset.instance_list:
            # TODO: Exercise 2.
            for (word, counts) in inst.feature_counts.items():
                word_and_category_to_count[(word, inst.label)] += counts
            category_to_num_instances[inst.label] += 1

        return cls(word_and_category_to_count, category_to_num_instances, vocabsize, smoothing)

    def log_probability(self, word, category):
        """ This computes the (relative) log probability of a word for a category: log[p(word|category)].
        
        log[p(word|category)] = log[word_occurrences_in_this_category + smoothing] - log[all_words_in_this_category + vocabSize * smoothing]
        
        """
        wordcount = self.word_and_cat_to_count.get((word, category), 0)
        total = self.cat_to_num_words.get(category, 0)
        return math.log(wordcount + self.smoothing) - math.log(total + self.smoothing * self.vocabsize)

    def score_for_category(self, feature_counts, category):
        """ This computes the log probability of a category for one data instance (i.e., for all words of a data instance)

        score_for_category(instance, category) = log( P(instance|category) * P(category) )
            = log[P(instance|category)] + log[P(category)]
        """
        # language model probability
        score = sum([count * self.log_probability(word, category) for word, count in feature_counts.items()])
        # prior probability
        score += math.log(self.category_to_prior[category])
        return score

    def prediction(self, feature_counts):
        """ Goes through all possible categories and predicts the category of the given feature_counts (i.e., of the given data instance)
        feature_counts is a dict (str -> int). To predict the category, the method should use the method 
        score_for_category() and return the category with the highest score."""
        best_category = None
        highest_score = - 100000
        # TODO: Exercise 3.
        categories = self.cat_to_num_words.keys()
        for category in categories:
            if self.score_for_category(feature_counts, category) > highest_score:
                highest_score = self.score_for_category(feature_counts, category)
                best_category = category
        return best_category

    def prediction_accuracy(self, dataset):
        """ Iterates through all data instances of the given dataset, gets the prediction for that data instance
        (use the previously implemented method prediction()) and calculates the accuracy of the classifier. Note that the
        attribute self.label contained in the class DataInstance contains the gold label of that data instance, so the 
        correct label. You will need this for your comparison."""
        # TODO: Exercise 4.
        total_number = len(dataset.instance_list)
        correct_predition_number = 0
        for instance in dataset.instance_list:
            if self.prediction(instance.feature_counts) == instance.label:
                correct_predition_number += 1
        return correct_predition_number/total_number

    def log_odds_for_word(self, word, category):
        """ This computes the log-odds for one word only. (have a look at the slides for some help)
        log_odds(word, category) = log( P(category|word) / (1 - P(category|word)) )
            = log[P(word|category)*P(category)] - log[P(word|other_category1)*P(other_category1)
              + P(word|other_category2)*P(other_category2) + ...]
              
        Hint: calculate the first part of this equality ( log[P(word|category)*P(category)] ) and the second 
        part of it ( log[P(word|other_category1)*P(other_category1) + P(word|other_category2)*P(other_category2) + ...]  )
        separately and then subtract them, as shown above.
        """
        # TODO: Exercise 5.
        # wordcount = self.word_and_cat_to_count[(word, category)]
        # total = self.cat_to_num_words[category]
        log_word_category = self.score_for_category({word: 1}, category)
        # log_word_category = math.log((wordcount/total)*self.category_to_prior[category])
        word_other_categories = sum(math.exp(self.score_for_category({word:1}, noncategory)) for noncategory in self.category_to_prior if noncategory != category)
        # for cat in self.cat_to_num_words.keys():
        #     if category == cat:
        #         continue
        #     total = self.cat_to_num_words[cat]
        #     word_other_categories += (wordcount/total)*self.category_to_prior[cat]

        return log_word_category-math.log(word_other_categories)

    def features_for_category(self, category, topn=10):
        """ Returns the topn features, that have the highest log-odds ratio for a category."""
        words = [word for word, cat in self.word_and_cat_to_count if cat == category]
        return sorted(words, key=lambda word: self.log_odds_for_word(word, category), reverse=True)[:topn]
