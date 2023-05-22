import nltk


def get_similarity_scores(pairs):
    results = []

    for pair in pairs:

        max_score = 0.0
        max_line = () #should look like "('food-fruit', 0.1)"

        #TODO 1. iterate over all combinations of synsets formed by the synsets of the words in the word pair
        #TODO 2. determine the maximum similarity score
        #TODO 3. save max_line in results in form ("pair1-pair2", similarity_value) e.g. ('car-automobile', 1.0)


        for synset1 in nltk.corpus.wordnet.synsets(pair[0]):
            for synset2 in nltk.corpus.wordnet.synsets(pair[1]):
                score = synset1.path_similarity(synset2)

                if score is not None and score > max_score:
                    max_score = score
                    max_line = (pair[0] + "-" + pair[1], score)

        results.append(max_line)
    #TODO 4. return results in order of decreasing similarity
    return sorted(results, key=lambda x: x[1],reverse=True)


