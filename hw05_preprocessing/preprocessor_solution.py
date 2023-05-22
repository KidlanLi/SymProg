from nltk.tokenize import *
import nltk.data
from nltk.corpus import inaugural
from nltk import FreqDist
from nltk.corpus import swadesh


class Preprocessor(object):
    def __init__(self, text, text_id):
        """reads the file text as a string"""
        self.text = text
        self.text_id = text_id

    @classmethod
    def from_nltk_book(cls):
        """Reads the inaugural text from the nltk book as a string. Note that this is a @classmethod
        which will be used instead of the default constructor when creating the object. Remember to
         return cls(something)"""
        text = inaugural.raw()
        return cls(text, "inaugural")

    @classmethod
    def from_text_file(cls, path, text_id):
        """Reads the text from given file as a string. Note that this is a @classmethod
        which will be used instead of the default constructor when creating the object.
         Remember to return cls(something)"""
        with open(path, "r") as fh:
            text = fh.read()
        return cls(text, text_id)

    def get_no_of_sents(self):
        """Split the input text into sentences and return the length of the text in sentences."""
        # sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        # sents = sent_detector.tokenize(self.text.strip())
        sents = sent_tokenize(self.text)
        return len(sents)

    def tokenize_text(self):
        """Split the text into tokens. Use an nltk method for that, equivalent to s.split()"""
        return word_tokenize(self.text)

    def lemmatize_token(self, token):
        """Lemmatize the given token, after converting it to lowercase."""
        wnl = nltk.WordNetLemmatizer()
        return wnl.lemmatize(token.lower())

    def get_20_most_frequent_words(self):
        """Return the 20 most frequent words of the text after removing the stopwords and all non-alphanumeric characters
         (in other words, remove all punctuation). Note that the stopwords are stored with their lemmata so you
         will have to make sure you check whether the lemma of each word is contained in the stopwords list.
         Make sure you use the method tokenizeText() that you implemented above"""
        tokens = self.tokenize_text()
        word_freq = FreqDist(tokens)
        stopwords = set(nltk.corpus.stopwords.words("english"))
        
        # Solution using unicode
        # def is_alphanum_unicode(w):
        #     return all([ord('a') <= ord(c) <= ord('z') or ord('0') <= ord(c) <= ord('9') for c in set(w.lower())])
        # filtered_word_freq = dict((word, freq) for word, freq in word_freq.items() if is_alphanum_unicode(word) and self.lemmatize_token(word) not in stopwords)
        
        # Solution using regular expressions
        # def is_alphanum_regex(w):
        #     return bool(re.match('^[a-zA-Z0-9]+$', w))
        # filtered_word_freq = dict((word, freq) for word, freq in word_freq.items() if is_alphanum_regex(word) and self.lemmatize_token(word) not in stopwords)
        
        # Simplest and fastest solution (recommended)
        filtered_word_freq = dict((word, freq) for word, freq in word_freq.items() if word.isalnum() and self.lemmatize_token(word) not in stopwords)
        most_freq_dict = dict(sorted(filtered_word_freq.items(), key=lambda item: item[1], reverse=True))
        return list(most_freq_dict.keys())[:20]

    def get_originality_score(self, most_freq_words):
        """Return the originality score of a text. This score can be measured by counting how many words contained
        in the swadesh list of nltk are also contained in the list with the 20 most frequent words of the text.
        For example, if 10 words can be found in both lists, the originality score is 10.
        The list with the 20 most frequent words should be given to the method as a parameter. """
        english_words = swadesh.words("en")
        common_words = [x for x in most_freq_words if x in english_words]
        return len(common_words)


if __name__ == '__main__':
    """Create two instances of the Preprocessor class. One instance should be created through the text file 
    ada_lovelace.txt and the other one through the inaugural text included in the nltk book. """
    text1 = Preprocessor.from_text_file("ada_lovelace.txt", "ada_lovelace")
    text2 = Preprocessor.from_nltk_book()

    """For each instance of the Preprocessor, do the following:
      a) print out the numbers of sentences of the text
      b) print out the 20 most frequent words of the text
      c) print out the originality score of the text."""
    most_freq_words1 = text1.get_20_most_frequent_words()
    text1.get_originality_score(most_freq_words1)

    most_freq_words2 = text2.get_20_most_frequent_words()
    text2.get_originality_score(most_freq_words2)
