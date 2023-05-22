from nltk import FreqDist, word_tokenize
from collections import defaultdict
import os, math
from os.path import basename

import doctest

def dot(dict_a, dict_b):
    """
    >>> dot({"Deutschland": 2, "Demokratie": 3}, {"England": 4, "Demokratie": 2})
    6
    """
    return sum([dict_a.get(tok) * dict_b.get(tok, 0) for tok in dict_a])


def normalized_tokens(text):
    """
    >>> normalized_tokens("the cat sat on a mat")
    ['the', 'cat', 'sat', 'on', 'a', 'mat']
    """
    return [token.lower() for token in word_tokenize(text)]

if __name__ == "__main__":
    doctest.testmod(verbose=True)






class TextDocument:
    def __init__(self, text, id=None):
        # TODO: Exercise 3.2, remove line breaks (see unittest for example)
        self.text = (text.replace("-\n", "")).replace("\n", " ")
        self.token_counts = FreqDist(normalized_tokens(text))
        self.id = id

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as myfile:
            text = myfile.read().strip()
        return cls(text, basename(filename))


class DocumentCollection:
    def __init__(self, term_to_df, term_to_docids, docid_to_doc):
        # string to int
        self.term_to_df = term_to_df
        # string to set of string
        self.term_to_docids = term_to_docids
        # string to TextDocument
        self.docid_to_doc = docid_to_doc

    @classmethod
    def from_dir(cls, directory, file_suffix):
        files = [(directory + "/" + f) for f in os.listdir(directory) if f.endswith(file_suffix)]
        docs = [TextDocument.from_file(f) for f in files]
        return cls.from_document_list(docs)

    @classmethod
    def from_document_list(cls, docs):
        term_to_df = defaultdict(int)
        term_to_docids = defaultdict(set)
        docid_to_doc = dict()
        for doc in docs:
            docid_to_doc[doc.id] = doc
            for token in doc.token_counts.keys():
                term_to_df[token] += 1
                term_to_docids[token].add(doc.id)
        return cls(term_to_df, term_to_docids, docid_to_doc)

    def docs_with_all_tokens(self, tokens):
        docids_for_each_token = [self.term_to_docids[token] for token in tokens]
        docids = set.intersection(*docids_for_each_token)
        return [self.docid_to_doc[_id] for _id in docids]

    def docs_with_some_tokens(self, tokens):
        docids_for_each_token = [self.term_to_docids[token] for token in tokens]
        docids = set.union(*docids_for_each_token)
        return [self.docid_to_doc[_id] for _id in docids]  # TODO: Exercise 3.3

    def tfidf(self, counts):
        N = len(self.docid_to_doc)
        return {tok: tf * math.log(N / self.term_to_df[tok]) for tok, tf in counts.items() if tok in self.term_to_df}

    def cosine_similarity(self, doc_a, doc_b):
        """Make the existing test pass by changing the functionality of this function"""
        # TODO: Exercise 3.1
        weighted_a = self.tfidf(doc_a.token_counts)
        weighted_b = self.tfidf(doc_b.token_counts)

        if weighted_a != {} and weighted_b != {}:
            dot_ab = dot(weighted_a, weighted_b)
            norm_a = math.sqrt(dot(weighted_a, weighted_a))
            norm_b = math.sqrt(dot(weighted_b, weighted_b))
            return dot_ab / (norm_a * norm_b)
        return 0


class SearchEngine:
    def __init__(self, doc_collection):
        self.doc_collection = doc_collection

    def ranked_documents(self, query):
        query_doc = TextDocument(query)
        query_tokens = query_doc.token_counts.keys()
        docs = self.doc_collection.docs_with_all_tokens(query_tokens)
        # TODO: Exercise 3.3 (replace docs_with_all_tokens with your implementation of docs_with_some_tokens)
        if not docs:
            docs = self.doc_collection.docs_with_some_tokens(query_tokens)

        docs_sims = [(doc, self.doc_collection.cosine_similarity(query_doc, doc)) for doc in docs]
        return sorted(docs_sims, key=lambda x: -x[1])

    def snippets(self, query, document, window=50):
        text = document.text
        # TODO: Exercise 3.4
        query_tokens = normalized_tokens(query)
        token_String = ' '.join(query_tokens)
        str_start = text.lower().find(token_String.lower())

        if str_start == -1:
            for token in query_tokens:
                start = text.lower().find(token.lower())
                if -1 == start:
                    continue
                end = start + len(token)
                line = f"...{text[start - window:start]}[{text[start: end]}]{text[end:end + window]}..."
                yield line
        else:
            str_end = str_start + len(token_String)
            str_left = "..." + text[max(str_start - window, 0):str_start]
            str_middle = "[" + text[str_start: str_end] + "]"
            str_right = text[str_end:str_end + window] + "..."
            yield ' '.join((str_left + str_middle + str_right).split())
