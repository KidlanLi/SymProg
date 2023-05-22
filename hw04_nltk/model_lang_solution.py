import nltk


class LangModeler(object):
    def __init__(self, languages, words):
        self.languages = languages
        self.words = words

    def build_language_models(self):
        """Build a ConditionalFrequencyDistribution of character frequencies in the UDHR corpus conditioned on each language
        hint: use nltk.ConditionalFreqDist """
        return nltk.ConditionalFreqDist(
            (language, word.lower())
            for language in self.languages
            for word in self.words[language])

    def guess_language(self,language_model_cfd, text):
        """Returns the guessed language for the given text"""
        max_score = 0
        max_language = None

        for language in language_model_cfd.conditions():
            #for each language calculate the overall score of a given text
            #based on the frequency of characters accessible by language_model_cfd[language].freq(character)
            score = 0 # initialize the score
            for word in text.split():
                word = word.lower()
                score += language_model_cfd[language].freq(word)

            # identify most likely language for a given text according to the score
            if score > max_score or max_language is None: # check if the score is maximal
                max_language = language
                max_score = score
        return max_language # retrieve the language
