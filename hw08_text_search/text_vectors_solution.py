from nltk import FreqDist, word_tokenize
from collections import defaultdict
import os, math


def dot(dictA, dictB):
    """
    >>> dot({"apple":4,"orange":7,"pear":2}, {"apple":4,"orange":5,"pear":8})
    67
    """
    return sum([dictA.get(tok) * dictB.get(tok, 0) for tok in dictA])


def normalized_tokens(text):
    """
    >>> normalized_tokens("The dog IS walking.")
    ['the', 'dog', 'is', 'walking', '.']
    """
    return [token.lower() for token in word_tokenize(text)]


class TextDocument:
    def __init__(self, text, id=None):
        line_break = '-\n'
        self.text = text.replace(line_break, '').replace('\n', " ")
        self.token_counts = FreqDist(normalized_tokens(text))
        self.id = id

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as myfile:
            text = myfile.read().strip()
        return cls(text, filename)


class DocumentCollection:
    def __init__(self, term_to_df, term_to_docids, docid_to_doc):
        # string to int
        self.term_to_df = term_to_df
        # string to set of string
        self.term_to_docids = term_to_docids
        # string to TextDocument
        self.docid_to_doc = docid_to_doc

    @classmethod
    def from_dir(cls, dir, file_suffix):
        files = [(dir + "/" + f) for f in os.listdir(dir) if f.endswith(file_suffix)]
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
        return [self.docid_to_doc[id] for id in docids]
        
    # If there is no result containing all tokens, search for documents containing at least one of the tokens.
    def docs_with_some_tokens(self, tokens):
        docids_for_each_token = [self.term_to_docids[token] for token in tokens]
        docids = set.union(*docids_for_each_token)
        return [self.docid_to_doc[id] for id in docids]

    def tfidf(self, counts):
        N = len(self.docid_to_doc)
        return {tok: tf * math.log(N / self.term_to_df[tok]) for tok, tf in counts.items() if tok in self.term_to_df}

    def cosine_similarity(self, doc_a, doc_b):
        weighted_a = self.tfidf(doc_a.token_counts)
        weighted_b = self.tfidf(doc_b.token_counts)
        dot_ab = dot(weighted_a, weighted_b)
        norm_a = math.sqrt(dot(weighted_a, weighted_a))
        norm_b = math.sqrt(dot(weighted_b, weighted_b))
        if norm_a == 0 or norm_b == 0:
            return 0
        else:
            return dot_ab / (norm_a * norm_b)


class SearchEngine:
    def __init__(self, doc_collection):
        self.doc_collection = doc_collection

    def ranked_documents(self, query):
        query_doc = TextDocument(query)
        query_tokens = query_doc.token_counts.keys()
        docs = self.doc_collection.docs_with_some_tokens(query_tokens)
        docs_sims = [(doc, self.doc_collection.cosine_similarity(query_doc, doc)) for doc in docs]
        return sorted(docs_sims, key=lambda x: -x[1])
        
    def snippets(self, query, document, window=50):
        text = document.text
        if query.lower() in text:
            left, middle, right = self.construct_single_snippet(query, text, window)
            # Change the functionality such that lines are displayed without line breaks.
            yield (left + middle + right).replace('\n', '')
        else:
            tokens = normalized_tokens(query)
            for token in tokens:
                start = text.lower().find(token.lower())
                if start != -1:
                    left, middle, right = self.construct_single_snippet(token, text, window)
                    yield left + middle + right

    def construct_single_snippet(self, token_to_highlight, text, window):
        start = text.lower().find(token_to_highlight.lower())
        end = start + len(token_to_highlight)
        left = "..." + text[start - window: start]
        middle = "[" + text[start: end] + "]"
        right = text[end: end + window] + "..."
        return left, middle, right
