from collections import defaultdict
from nltk import word_tokenize
import sys
import math


def normalized_tokens(text):
    return [token.lower() for token in word_tokenize(text)]


class DataInstance:
    def __init__(self, feature_counts, label):
        """ A data instance consists of a dictionary with feature counts (string -> int) and a label/category."""
        self.feature_counts = feature_counts
        self.label = label

    @classmethod
    def from_list_of_feature_occurrences(cls, feature_list, label):
        """ Creates feature counts for all features in the list."""
        feature_counts = dict()
        # TODO: Exercise 1: Create a dictionary that contains for each feature in the list the count how often it occurs.
        for feature in feature_list:
            count = feature_counts.get(feature, 0)
            feature_counts[feature] = count + 1
        # or in short (requires "from collections import Counter")
        # feature_counts = Counter(feature_list)
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
        # The following lines are required to compute P(word|category), which in turn is required to compute P(text|category).
        self.word_and_cat_to_count = word_and_category_to_count
        # cat_to_num_words is a dict: how many words occur in each category. 
        # The keys are the categories and the values are the count of all words in that category.
        self.cat_to_num_words = defaultdict(int)
        for (word, cat), count in word_and_category_to_count.items():
            self.cat_to_num_words[cat] += count
        self.vocabsize = vocabsize
        
        # THe following lines are required to compute P(category)
        # total_instances: all instances of all categories
        total_instances = sum(category_to_num_instances.values())
        # category_to_prior is a dict: what is the prior probability for each category. The keys are the categories and 
        # the values the prior probabilities.
        self.category_to_prior = {c: n/total_instances for c, n in category_to_num_instances.items()}
        self.smoothing = smoothing

    @classmethod
    def for_dataset(cls, dataset, smoothing = 1.0):
        """ Creates a NB-Classifier for a dataset."""
        # maps tuples (word, category) to the number of occurences of a word in a that category ((str,str) -> int)
        word_and_category_to_count = defaultdict(int) 
        # maps a category name to the number of instances in that category (str -> int)
        category_to_num_instances = defaultdict(int) 
        vocabsize = len(dataset.feature_set)
        for inst in dataset.instance_list:
            # TODO: Exercise 2.
            category_to_num_instances[inst.label] += 1
            for (word, count) in inst.feature_counts.items():
                word_and_category_to_count[(word, inst.label)] += count
        return cls(word_and_category_to_count, category_to_num_instances, vocabsize, smoothing)

    def log_probability(self, word, category):
        """ This computes the (relative) log probability of a word for a category: log[p(word|category)].
        
        log[p(word|category)] = log[word_occurrences_in_this_category + smoothing] - log[all_words_in_this_category + vocabSize * smoothing]
        
        """
        wordcount = self.word_and_cat_to_count.get((word, category), 0)
        total = self.cat_to_num_words.get(category, 0)
        # Parametrize by overall count added rather than per type.
        return math.log(wordcount + self.smoothing) - math.log(total + self.smoothing * self.vocabsize)

    def score_for_category(self, feature_counts, category):
        """ This computes the log probability of a category for one data instance (i.e., for all words of a data instance)

        score_for_category(text, category) 
            = log( P(text|category) * P(category) ) = log( Π_i P(word_i|category) * P(category) )
            = log( P(text|category) ) + log( P(category) ) 
            = log( Π_i P(word_i|category) ) + log( P(category) )
            = Σ_i log( P(word_i|category) ) + log( P(category) )
            = conditional log probability + prior log probability 
        """
        # conditional probability (in log-space): one for each word occurrence
        score = sum([count * self.log_probability(word, category) for word, count in feature_counts.items()])
        
        # prior probability (in log-space)
        score += math.log(self.category_to_prior[category])
        return score

    def prediction(self, feature_counts):
        """ Goes through all possible categories and predicts the category of the given feature_counts (i.e., of the given data instance)
        feature_counts is a dict (str -> int). To predict the category, the method should use the method 
        score_for_category() and return the category with the highest score."""
        best_category = None
        # TODO: Exercise 3.
        highest_score = float("-inf") 
        for category in self.category_to_prior:
            score = self.score_for_category(feature_counts, category)
            if score > highest_score:
                best_category = category
                highest_score = score
        return best_category

    def prediction_accuracy(self, dataset):
        """ Iterates through all data instances of the given dataset, gets the prediction for that data instance
        (use the previously implemented method prediction()) and calculates the accuracy of the classifier. Note that the
        attribute self.label contained in the class DataInstance contains the gold label of that data instance, so the 
        correct label. You will need this for your comparison."""
        # TODO: Exercise 4.
        num_correct = 0
        for inst in dataset.instance_list:
            prediction = self.prediction(inst.feature_counts)
            # covers True Positives (TP) and True Negatives (TN) 
            if prediction == inst.label:
                num_correct += 1
        acc = num_correct / len(dataset.instance_list)
        return acc

    def log_odds_for_word(self, word, category):
        """ This computes the log-odds for one word only. (have a look at the slides for some help)
        log_odds(word, category) = log( P(category|word) / (1 - P(category|word)) )
            = log( P(word|category)*P(category) ) - log( P(word|other_category1)*P(other_category1) + P(word|other_category2)*P(other_category2) + ...)
            = log( P(word|category)*P(category) ) - log(Σ_i P(word|other_category_i)*P(other_category_i) )
            
        Hint: calculate the first part of this equation ( log( P(word|category)*P(category)] ) ) and the second
        part of it ( log[P(word|other_category1)*P(other_category1) + P(word|other_category2)*P(other_category2) + ...) )
        separately and then subtract them, as shown above. 
        """
        # TODO: Exercise 5.
        # log( P(word|category) * P(category) )
        log_first_part = self.log_probability(word, category) + math.log(self.category_to_prior[category])
        print (log_first_part)
        
        # log( Σ_i P(word|other_category_i) ) + log P(other_category_i) )
        second_part = 0
        for c in self.category_to_prior.keys():
            if c != category:
                word_prob = math.exp(self.log_probability(word, c)) * self.category_to_prior[c]
                # or, do multiplication in the log-space and bring back to linear-space
                # word_prob = math.exp(self.log_probability(word, c) + math.log(self.category_to_prior[c]))
                second_part += word_prob
        log_second_part = math.log(second_part)
        
        # final step: log( P(category|word) / (1 - P(category|word)) ) 
        log_odds = log_first_part - log_second_part
        return log_odds

    def features_for_category(self, category, topn=10):
        """ Returns the topn features, that have the highest log-odds ratio for a category."""
        words = [word for word, cat in self.word_and_cat_to_count if cat == category]
        return sorted(words, key=lambda word: self.log_odds_for_word(word, category), reverse=True)[:topn]
