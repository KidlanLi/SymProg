from nltk import FreqDist
from nltk import word_tokenize

class Analyzer(object):
    def __init__(self, path):
        '''reads the file text, creates the list of words (use nltk.word_tokenize to tokenize the text),
            and calculates frequency distribution '''
        self.text = None #TODO the list of words from text file
                with open(path, mode='r') as f:
                str = "".join(f.readlines())
        self.text = nltk.word_tokenize(str)
        self.token_counts = None #TODO frequency distribution of words from text file
        self.token_counts = nltk.FreqDist(self.text)

    def numberOfTokens(self):
        '''returns number of tokens in the text '''
        return len(self.text)

    def vocabularySize(self):
        '''returns the size of the vocabulary of the text '''
        return len(set(self.text))

    def lexicalDiversity(self):
        '''returns the lexical diversity of the text '''
        return len(self.token_counts)/len(self.text)

    def getKeywords(self):
        '''return words as possible key words, that are longer than seven characters, that occur more than seven times (sorted alphabetically)'''
        keywords = []
        for (word,frequent) in self.token_counts.items():
            if len(word) > 7 and frequent > 7:
                keywords = keywords + [word]
        return sorted(keywords)

    def numberOfHapaxes(self):
        '''returns the number of hapaxes in the text'''
        num = 0
        for (word, frequence) in self.token_counts.items():
            if frequence == 1:
                num += 1
        return num

    def avWordLength(self):
        '''returns the average word length of the text'''
        sumlen = 0
        for (word, frequent) in self.token_counts.items():
            sumlen = sumlen + len(word)
        return sumlen/len(set(self.text))

