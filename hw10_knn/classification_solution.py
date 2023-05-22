from nltk import FreqDist, word_tokenize
from collections import defaultdict
import os, math
from collections import Counter

def dot(dictA, dictB):
    return sum([dictA.get(tok) * dictB.get(tok,0) for tok in dictA])

def normalized_tokens(text):
    return [token.lower() for token in word_tokenize(text)]

class TextDocument:
    def __init__(self, text, id=None, category=None):
        self.text = text
        self.token_counts = FreqDist(normalized_tokens(text))
        self.id = id
        self.category = category

    @classmethod
    def from_file(cls, filename, category):
        with open(filename, 'r',encoding="ISO-8859-1") as myfile:
            text=myfile.read().strip()
        return cls(text, filename,category)

class DocumentCollection:
    def __init__(self, term_to_df, term_to_docids, docid_to_doc,doc_to_category):
        # string to int
        self.term_to_df = term_to_df
        # string to set of string
        self.term_to_docids = term_to_docids
        # string to TextDocument
        self.docid_to_doc = docid_to_doc
        # TextDocument to category
        self.doc_to_category = doc_to_category

    @classmethod
    def from_dir(cls, dir):

        files = [(os.path.join(root,name),os.path.relpath(root, dir)) for root,dirs,f in os.walk(dir, topdown=False) for name in f]
        docs = [TextDocument.from_file(f,cat) for f,cat in files]
        for f,cat in files[:3]:
            print(f,cat)
        return cls.from_document_list(docs)

    @classmethod
    def from_document_list(cls, docs):
        term_to_df = defaultdict(int)
        term_to_docids = defaultdict(set)
        docid_to_doc = dict()
        doc_to_category = dict()
        for doc in docs:
            docid_to_doc[doc.id] = doc
            doc_to_category[doc] = doc.category
            for token in doc.token_counts.keys():
                term_to_df[token] += 1
                term_to_docids[token].add(doc.id)
        return cls(term_to_df, term_to_docids, docid_to_doc,doc_to_category)


    def tfidf(self, counts):
        N = len(self.docid_to_doc)
        return {tok: tf * math.log(N/self.term_to_df[tok]) for tok,tf in counts.items() if tok in self.term_to_df}

    def cosine_similarity(self, weightedA, weightedB):

        dotAB = dot(weightedA, weightedB)
        normA = math.sqrt(dot(weightedA, weightedA))
        normB = math.sqrt(dot(weightedB, weightedB))
        if normA == 0 or normB == 0:
        	return 0
        else:
        	return dotAB / (normA * normB)

class KNNClassifier:
    def __init__(self,n_neighbors=1):
        self.n_neighbors = n_neighbors
        self.doc_collection = None
        self.vectorsOfDoc_collection = None

    def fit(self, doc_collection):
        self.doc_collection = doc_collection
        self.vectorsOfDoc_collection = [(doc, self.doc_collection.tfidf(doc.token_counts))
                                   for doc in self.doc_collection.docid_to_doc.values()]


    def calculate_similarities(self,vecTestDoc,vectorsOfTrainDocs):
        #TODO calculate similarities between test and train documents and label them [(similarity, label),...]
        similarities = [(self.doc_collection.cosine_similarity(vec_train_doc,vecTestDoc), self.doc_collection.doc_to_category[train_doc])
                        for train_doc, vec_train_doc in vectorsOfTrainDocs]
        return similarities


    def order_nearest_to_farthest(self,similarities):
        #TODO order the labeled points from nearest to farthest
        sorted_distances= sorted(similarities, key=lambda x: x[0], reverse = True)
        return sorted_distances


    def labels_k_closest(self,sorted_similarities):
        #TODO find the labels for the k closest
        k_nearest_labels=[label for _,label in sorted_similarities[:self.n_neighbors]]
        return k_nearest_labels
        

    def choose_one(self,labels) :
        """returns unique label, assumes that labels are ordered from nearest to farthest"""
        #TODO Exercise 2.4: Reduce k until you find a unique winner
        counts = Counter(labels)
        winner, winner_count = counts.most_common(1)[0]
        num_winners = len([count for count in counts.values() if count == winner_count])
        if num_winners == 1:
            return winner
        else:
            return self.choose_one(labels[:-1])


    def classify(self, test_file):
        '''predicts label for given test file'''
        #TODO: Exercise 2.5: classify test document
        test_doc = TextDocument.from_file(test_file,'unknowcat')

        testVec = self.doc_collection.tfidf(test_doc.token_counts)
        dist = self.calculate_similarities(testVec,self.vectorsOfDoc_collection)
        sorted_distances= self.order_nearest_to_farthest(dist)
        k_nearest_labels= self.labels_k_closest(sorted_distances)
        return self.choose_one(k_nearest_labels)



    def get_accuracy(self, gold, predicted):
        """ returns the accurracy of this classifier on a given test set."""
        #TODO: Exercise 3: calculate accuracy
        correct = 0
        for i in range(len(gold)):
            if gold[i] == predicted[i]:
                correct += 1

        return (correct/float(len(gold))) * 100.0
