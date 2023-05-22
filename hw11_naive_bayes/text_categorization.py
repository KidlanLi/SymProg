import sys

from sklearn.datasets import fetch_20newsgroups
from hw11_naive_bayes.naive_bayes_classifier import NaiveBayesClassifier, DataInstance, Dataset, normalized_tokens

def dataset_for_20newsgroups_subset(subset):
    # Download data set.
    newsgroups_subset = fetch_20newsgroups(subset=subset)
    # Get the newsgroups messages.
    texts = newsgroups_subset['data']
    # Get the corresponding labels.
    categories = newsgroups_subset['target']
    category_names = newsgroups_subset['target_names']
    print ("Please wait ...")
    # Make an instance for each combination of pairs and labels.
    instance_list = []
    for t, c in zip(texts, categories):
        inst = DataInstance.from_list_of_feature_occurrences(normalized_tokens(t), category_names[c])
        instance_list.append(inst)
    return Dataset(instance_list)

def main(argv):
    print ("Preparing training set")
    training_set = dataset_for_20newsgroups_subset("train")
    print ("Preparing test set")
    test_set = dataset_for_20newsgroups_subset("test")

    print('Training classifier...')
    classifier = NaiveBayesClassifier.for_dataset(training_set)

    # find best hyper-parameters
    best_dev_acc = 0.0
    best_smoothing = 0
    for smoothing in [0.0001,0.5,1]:
        print('Training with smoothing:',smoothing, '...')
        classifier.smoothing = smoothing
        train_accuracy = classifier.prediction_accuracy(training_set)
        test_accuracy = classifier.prediction_accuracy(test_set)
        print("Train Accuracy: %.4f Test Accuracy: %.4f" % (train_accuracy, test_accuracy))

        for cat in classifier.category_to_prior:
            print("Top features for category %s:" %cat)
            print(classifier.features_for_category(cat))

        print(len(training_set.instance_list))
        print(len(test_set.instance_list))

        #if dev_accuracy > best_dev_acc:
        #    best_dev_acc = dev_accuracy
        #    best_smoothing = smoothing

    # Calculate test scores
    #classifier.smoothing = best_smoothing
    #testing_accuracy = classifier.test_accuracy(testing_set)
    #print("Test Accuracy: %.4f (for smoothing of %f)" % (testing_accuracy, classifier.smoothing))

if __name__ == "__main__":
    main(sys.argv[1:])
