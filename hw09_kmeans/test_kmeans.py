from unittest import TestCase
from hw09_kmeans.kmeans import Reader
from hw09_kmeans.kmeans import Kmeans

filename= "hw09_kmeans/courses.txt"

class ClusteringTest(TestCase):


    def setUp(self):
        self.reader = Reader(filename)
        self.clusterer = Kmeans(3)

    def test_01_courses(self):
        courses = self.reader.courses #returns list of courses
        self.assertEqual(courses[:3], ['Bioinformatik', 'Didaktik der Informatik', 'Didaktik der Mathematik'])

    def test_02_normalize(self):
        word = "(Studienrichtung"
        normalized_word = self.reader.normalize_word(word) #returns list of courses
        self.assertEqual(normalized_word, "studienrichtung")

    def test_03_vocabulary(self):
        words = self.reader.vocabulary
        self.assertEqual(words[:3], ['albanologie', 'allgemeine', 'als'])

    def test_04_distance(self):
        a = [1, 2, 3]
        b = [4, 5, 6]
        euclidean_dist = self.clusterer.euclidian_distance(a,b)
        self.assertEqual(int(euclidean_dist), 5)

    def test_05_vector_mean(self):
        vectors = [[1, 2, 3],[4, 5, 6]]
        mean = self.clusterer.vector_mean(vectors)
        self.assertEqual(mean, [2.5, 3.5, 4.5])


    def test_06_classify(self):
        vectorspaced_data = self.reader.vector_spaced_data

        #clusters are always differrent
        self.clusterer.train(vectorspaced_data)
        clusters = [self.clusterer.classify(vec) for vec in vectorspaced_data]
        self.assertEqual(len(clusters), len(vectorspaced_data))
