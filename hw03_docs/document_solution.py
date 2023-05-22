from collections import defaultdict, Counter

import nltk
from nltk import word_tokenize


def normalized_tokens(text):
    """ This takes a string and returns lower-case tokens, using nltk for tokenization. """
    return [w.lower() for w in word_tokenize(text)]


class TextDocument:
    def __init__(self, text, id=None):
        """ This creates a TextDocument instance with a string, a dictionary and an identifier. """
        self.text = text
        self.id = id

        # Solution 1: plain dictionary
        self.word_to_count = dict()
        for w in normalized_tokens(text):
            if w in self.word_to_count:
                self.word_to_count[w] += 1
            else:
                self.word_to_count[w] = 1

        # Solution 2: use defaultdict
        # self.word_to_count = defaultdict(int)
        # for w in normalized_tokens(text):
        #     self.word_to_count[w] += 1

        # Solution 3: use counter objects
        # self.word_to_count = Counter(normalized_tokens(text))

        # Solution 4: nltk
        # self.word_to_count = nltk.FreqDist(normalized_tokens(text))


    @classmethod
    def from_file(cls, filename):
        """ This creates a TextDocument instance by reading a file. """
        with open(filename) as f:
            text = f.read().strip()
        return cls(text, filename)

    def __str__(self):
        """ This returns a short string representation, which is at most 25 characters long.
        If the original text is longer than 25 characters, the last 3 characters of the short string should be '...'.
        """
        if len(self.text) > 25:
            return self.text[:22] + '...'
        else:
            return self.text

    def word_overlap(self, other_doc):
        """ This returns the number of words that occur in both of the documents (self and other_doc) at the same time.
        Every word should be considered only once, irrespective of how often it occurs in either document (i.e. we
        consider word *types*).
        """
        s1 = set(self.word_to_count.keys())
        s2 = set(other_doc.word_to_count.keys())
        return len(s1.intersection(s2))
