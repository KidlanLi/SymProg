import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet


class HyponymSearcher(object):
    def __init__(self, text_path):
        self.noun_lemmas = []

        # TODO Read text as a string

        # TODO Split into sentences: use nltk.sent_tokenize

        # TODO Split into tokens: use nltk.word_tokenize

        # TODO Perform POS tagging on all tokens of all sentences (not on each sentence separately)

        # TODO lemmatize nouns (any token whose POS tags starts with "N"): use WordNetLemmatizer()

        # TODO determine all noun lemmas and save it in self.noun_lemmas

        with open(text_path, encoding="utf-8") as f:
            text = f.read()

        sentences = nltk.sent_tokenize(text)

        tokens = [t for s in sentences for t in nltk.word_tokenize(s)]

        pos = nltk.pos_tag(tokens)

        self.noun_lemmas = [WordNetLemmatizer().lemmatize(tok, wordnet.NOUN) for tok, p in pos if p.startswith("N")]

        """noun_lemmas = [WordNetLemmatizer().lemmatize(x) for x, y in g if y.startswith("N")]"""

        """self.noun_lemmas = noun_lemmas"""

    def hypernym_of(self, synset1, synset2):
        # TODO Is synset2 a hypernym of synset 1? (Or the same synset), return True or False
        if synset1 == synset2:
            return True
        for h in synset1.hypernyms():
            if HyponymSearcher.hypernym_of(self, h, synset2):
                return True
        return False

    def get_hyponyms(self, hypernym):
        # TODO determine set of noun lemmas in ada_lovelace.txt that are hyponyms of the given hypernym
        # use the implemented method hypernymOf(self, synset1, synset2)
        return set(n for n in self.noun_lemmas if any(HyponymSearcher.hypernym_of(self, s, hypernym) for s in wordnet.synsets(n)))
