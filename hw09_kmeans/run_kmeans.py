from hw09_kmeans.kmeans import Reader
from hw09_kmeans.kmeans import Kmeans



filename= "courses.txt"

reader = Reader(filename)

# returns list of courses
courses = reader.courses

#set of all words from file
words = reader.vocabulary
print("vocabulary size:", len(words))

vectorspaced_data =reader.vector_spaced_data

clusterer = Kmeans(10)
clusterer.train(vectorspaced_data)

data = [(clusterer.classify(vec),course) for vec, course in zip(vectorspaced_data, courses)]
sorted = sorted(data,key=lambda x: x[0])

for cluster, course in sorted:
    print(cluster,course)
