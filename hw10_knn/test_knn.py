from unittest import TestCase

from hw10_knn.classification import DocumentCollection, KNNClassifier, TextDocument

dir_train= "./data/20news-bydate/20news-bydate-train/"
dir_test = "./data/20news-bydate/20news-bydate-test/"


doc_collection_train = DocumentCollection.from_dir(dir_train)
classifier = KNNClassifier(n_neighbors=4)
classifier.fit(doc_collection_train)


train_docs = doc_collection_train.docid_to_doc.values()
vectorsOfTrainDocs = [(doc, doc_collection_train.tfidf(doc.token_counts)) for doc in train_docs]
test_doc = TextDocument.from_file(dir_test+'alt.atheism/53068', 'alt.atheism')
vecTestDoc = doc_collection_train.tfidf(test_doc.token_counts)
#2.1
dist = classifier.calculate_similarities(vecTestDoc,vectorsOfTrainDocs)
#2.2
ordered = classifier.order_nearest_to_farthest(dist)
#2.3
k_nearest_labels = classifier.labels_k_closest(ordered)
#2.4
label = classifier.choose_one(k_nearest_labels)


class ClassificationTest(TestCase):

    def test_01_calc_sims(self):
        sorted_dist = sorted(dist)
        self.assertEqual(sorted_dist[-1][1], 'alt.atheism')

    def test_02_order_near_to_far(self):
        test_distances=[(0.2,"c"),(0.5,"b"),(0.7,"a")]
        self.assertEqual([(0.7,"a"),(0.5,"b"),(0.2,"c")], classifier.order_nearest_to_farthest(test_distances))
        self.assertEqual(ordered[0][1], 'alt.atheism')

    def test_03_labels_k_closest(self):
        self.assertEqual(k_nearest_labels[0], 'alt.atheism')

    def test_04_choose_neighbor(self):
        winner = classifier.choose_one(['rec.sport.hockey', 'rec.sport.baseball', 'rec.motorcycles', 'rec.sport.hockey'])
        self.assertEqual(winner, 'rec.sport.hockey')

        self.assertEqual(label, 'alt.atheism')

    def test_05_classify(self):
        test_file = dir_test+'alt.atheism/53068'
        self.assertEqual(classifier.classify(test_file), 'alt.atheism')

    def test_06_accuracy(self):

        test_files = [(dir_test+'alt.atheism/53272', 'alt.atheism'),(dir_test+'sci.med/59225', 'sci.med'),
                      (dir_test+'comp.graphics/38758', 'comp.graphics'),(dir_test+'rec.autos/103007', 'rec.autos')]

        predicted_labels = [classifier.classify(file) for file, cat in test_files]

        gold_labels = [cat for _, cat in test_files]
        accuracy = classifier.get_accuracy(gold_labels, predicted_labels)
        self.assertEqual(accuracy, 75)
