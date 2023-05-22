from nltk import word_tokenize
from collections import Counter

def normalized_tokens(text):
    """ This takes a string and returns lower-case tokens, using nltk for tokenization. """
    # TODO: return list with lower-case tokens.
    return [token.lower() for token in word_tokenize(text)]


class TextDocument:
    def __init__(self, text, id=None):
        """ This creates a TextDocument instance with a string, a dictionary and an identifier. """
        self.text = text
        self.word_to_count = Counter(normalized_tokens(text))  # TODO: Create dictionary that maps words to their counts.
        self.id = id

    @classmethod
    def from_file(cls, filename):
        """ This creates a TextDocument instance by reading a file. """
        # text = "" # TODO: read text from filename
        with open(filename) as f:
            text = "".join(f.readlines())
        return cls(text, filename)

    def __str__(self):
        """ This returns a short string representation, which is at most 25 characters long.
        If the original text is longer than 25 characters, the last 3 characters of the short string should be '...'.
        """
        # TODO: Implement correct return statement.
        if len(self.text) > 25:
            return self.text[:22] + "..."
        return self.text

    def word_overlap(self, other_doc):
        """ This returns the number of words that occur in both documents (self and other_doc) at the same time.
        Every word should be considered only once, irrespective of how often it occurs in either document (i.e. we
        consider word *types*).
        """
        # TODO: Implement correct return statement.
        overlap = 0
        for word in self.word_to_count:
            if word in other_doc.word_to_count:
                overlap += 1
        return overlap

