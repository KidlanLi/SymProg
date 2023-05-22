from nltk import FreqDist
from nltk import word_tokenize

class Analyzer(object):

    def __init__(self, path):
        """load content from text file specified by path, tokenize text, and construct frequency distribution"""
        with open(path, "r") as fh:
            self.text = [w for line in fh for w in word_tokenize(line.strip())]
        self.token_counts = FreqDist(self.text)


    def numberOfTokens(self):
        """returns number of tokens in the text """
        return len(self.text)

    def vocabularySize(self):
        """returns the size of the vocabulary of the text """
        return len(set(self.text))
    
    def lexicalDiversity(self):
        """returns the lexical diversity on the tex """
        return self.vocabularySize()/self.numberOfTokens()

    def getKeywords(self):
        """
        return words as possible key words, that are longer than seven characters,
        that occur more than seven times (sorted alphabetically)
        """
        return sorted([w for w in set(self.text) if len(w) > 7 and self.token_counts[w] > 7])

    def numberOfHapaxes(self):
        """returns the number of hapaxes in the text"""
        return len(self.token_counts.hapaxes())

    def avWordLength(self):
        """returns the average word length of the text"""
        return sum(len(word) for word in self.token_counts.keys()) / len(self.token_counts.keys())
