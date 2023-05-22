import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

class HyponymSearcher(object):
    def __init__(self, text_path):
        # Read in text.
        with open(text_path, encoding="utf-8") as f:
            text = f.read()

        # Option 1.1:
        # Split into sentences, and then into tokens
        # tokens = []
        # for sentence in nltk.sent_tokenize(text):
        #     tokens += nltk.word_tokenize(sentence)

        # Option 1.2:
        # Split the full text into its tokens
        tokens = nltk.word_tokenize(text)

        # POS tagging on all tokens of all sentences
        pos_tags = nltk.pos_tag(tokens)

        # lemmatize nouns (any token whose POS tags starts with "N")
        lemmatizer = WordNetLemmatizer()

        self.noun_lemmas = []
        for token, pos in pos_tags:
            if pos.startswith("N"):
                self.noun_lemmas.append(lemmatizer.lemmatize(word=token, pos=wordnet.NOUN))

    # Option 2.1
    # def hypernym_of(self, synset1, synset2):
    #     """ returns True if synset2 is a hypernym of synset1, or if they are the same synsets """
    #     if synset1 == synset2:
    #         return True
    #
    #     for hypernym in synset1.hypernyms():
    #         if synset2 == hypernym or self.hypernym_of(hypernym, synset2):
    #             return True
    #
    #     return False

    # Option 2.2
    def hypernym_of(self, synset1, synset2):
        """ returns True if synset2 is a hypernym of synset1, or if they are the same synsets """
        for path in synset1.hypernym_paths():
            if synset2 in path:
                return True
        return False

    # Option 2.3
    # def hypernym_of(self, synset1, synset2):
    #     raise any(synset2 in path for path in synset1.hypernym_paths())

    def get_hyponyms(self, hypernym):
        """ Returns the set of noun lemmas in self.noun_lemmas that are hyponyms (subordinates) to the hypernym """
        hyponyms = set()
        # iterate each lemma in ada_lovelace
        for lemma in self.noun_lemmas:
            # iterate each (noun) meaning of that lemma
            for synset in wordnet.synsets(lemma, pos="n"):
                # check if 'hypernym' is a hypernym of 'synset'
                # in other words, check if 'synset' (the current meaning of the current lemma) is a hyponym of 'hypernym'
                if self.hypernym_of(synset, hypernym):
                    hyponyms.add(lemma)

        return hyponyms
