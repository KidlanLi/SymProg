import nltk


class LangModeler(object):
    def __init__(self, languages, words):
        self.languages = languages
        self.words = words

    def build_language_models(self):
        # TODO return ConditionalFrequencyDistribution of words in the UDHR corpus conditioned on each language
        # hint: use nltk.ConditionalFreqDist
        cfd = nltk.ConditionalFreqDist((l,w.lower())
                                       for l in self.languages
                                       for w in udhr.words(l + '-Latin1'))
        return cfd

    def guess_language(self,language_model_cfd, text):
        """Returns the guessed language for the given text"""

        #TODO for each language calculate the overall score of a given text
        #based on the frequency of words accessible by language_model_cfd[language].freq(word) and then
        #identify most likely language for a given text according to this score
        score = {}
        text1 = text.split(" ")
        for language in language_model_cfd.conditions():
            score[language] = 0
            for word in text1:
                score[language] += language_model_cfd[language].freq(word.lower())
        lang = ''
        max = 0
        for (language, score) in score.items():
            if score > max:
                max = score
                lang = language
        return lang
