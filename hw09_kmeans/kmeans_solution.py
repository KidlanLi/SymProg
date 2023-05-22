import string
import numpy as np
import random


class Reader:

    def __init__(self, path):
        self.path = path
        self.punctuation = set(string.punctuation)
        self.courses = self.get_lines()
        self.vocabulary = self.get_vocabulary()
        self.vector_spaced_data = self.data_to_vectorspace()

    def get_lines(self):
        with open(self.path) as courses_file:
            return [line.strip() for line in courses_file.readlines()]

    def normalize_word(self,word):
        punct_removed = ''.join(ch for ch in word if ch not in self.punctuation)
        return punct_removed.lower()

    def get_vocabulary(self):
        words = set()
        for course in self.courses:
            for word in course.split():
                words.add(self.normalize_word(word))
        return sorted(list(words))


    def vectorspaced(self,course):
        """ converts the given course, which is a string, to a one-hot vector,
        i.e., a vector filled with 0s, except for those positions associated with the
        words of the given course in the vocabulary. These positions are filled with 1."""
        course_components = [self.normalize_word(word) for word in course.split()]
        vectors = [int(word in course_components) for word in self.vocabulary]
        return vectors

    def data_to_vectorspace(self):
        """ convert all courses of the Reader to one-hot-vectors"""
        return [self.vectorspaced(course) for course in self.courses if course]


class Kmeans:
    """performs k-means clustering"""

    def __init__(self, k):
        self.k = k
        self.means = None

    def euclidian_distance(self, x,y):
        # Solution without the use of numpy
        # sum((i-j)**2 for i, j in zip(x, y))**(1/2)
        return np.sqrt(np.sum((np.array(x)-np.array(y))**2))

    def classify(self, input):
        """return the index of the cluster
        closest to the input"""
        # centroid = self.means[0]
        # d_min = self.euclidian_distance(input, self.means[0])
        # for i in range(1, self.k):
        #     d = self.euclidian_distance(input, self.means[i])
        #     if d < d_min:
        #         d_min = d
        #         centroid = i
        # return centroid
        return min(range(self.k), key=lambda i: self.euclidian_distance(input, self.means[i]))

    def vector_mean(self,vectors):
        """compute the componentwise mean of a list of (same-sized) vectors"""
        # vec_size = len(vectors[0])
        # avg_vec = []
        # for component in range(vec_size):
        #     values = [vec[component] for vec in vectors]
        #     avg = sum(values) / len(values)
        #     avg_vec.append(avg)
        return np.mean(vectors, axis=0, dtype=np.float64).tolist()

    def train(self, inputs):
        # choose k random points as the initial means
        random_ids = np.random.choice(len(inputs), self.k, replace=False)
        # you can also use the built-in python package random
        # random_ids = random.sample(range(len(inputs)), self.k)
        self.means = [inputs[rid] for rid in random_ids]

        iterations = 0
        while iterations != 100:
            # Find new assignments
            assignments = list(map(self.classify, inputs))

            # compute new means based on the new assignments
            for cluster_i in range(self.k):
                # find all the points assigned to cluster i
                cluster_members = [p for p, a in zip(inputs, assignments) if a == cluster_i]
                # make sure i_points is not empty so don't divide by 0
                if cluster_members:
                    self.means[cluster_i] = self.vector_mean(cluster_members)
            iterations += 1
