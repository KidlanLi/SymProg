import nltk


class Sentences:
    def __init__(self, sentences):
        """Construct and instance of the class Sentence from a list of
        pos-tagged sentences ([[(word,tag),...],...])"""
        self.sentences = sentences

    def __iter__(self):
        return iter(self.sentences)

    def __getitem__(self, i):
        return self.sentences[i]

    @classmethod
    def from_file(cls, path):
        """Create an instance of the class Sentences from a path. Reads the
        file and pos-tags the sentences in the file. [2 point]"""
        with open(path, 'r', encoding='utf8') as f:
            text = f.read()
        sentences = nltk.sent_tokenize(text)
        return cls([nltk.pos_tag(nltk.word_tokenize(s)) for s in sentences])


class PosExpr:
    def __init__(self, expressions):
        """Construct an instance of the class PosExpr from a list of expressions."""
        self.expressions = expressions

    @classmethod
    def from_string(cls, expr):
        """Create an instance of the class PosExpr from the given
        string.  [1 points]"""
        return cls(expr.split(" "))

    @staticmethod
    def match_expr(expr, pos):
        """This method returns True if expr matches pos. An expression 'XX'
        matches if pos equals 'XX', the expression '*' matches any pos
        and an expression XX* matches if pos starts with 'XX' or is
        equal to 'XX'.  [2 points]"""
        if len(expr) == 0:
            return False
        if expr == "*":
            return True
        if expr[-1] == "*":
            return pos.startswith(expr[0:-1])
        return expr == pos


    def match_seq(self, sequence):
        """This method returns a list of matches in the given sequence
        (a sequence here is a list of (word,pos)-pairs -- see following example).
        A match is a list of (word, pos)-pairs, where the tags in the sequence match
        all expressions provided by PosExpr for all possible positions.
        For example: given p=PosPattern.from_string("X Y"),
        p.match_seq([(a,X),(b,Y),(c,Z),(d,X),(e,Y))]) should return the following list of lists:
        [[(a,X),(b,Y)],[(d,X),(e,Y)]].  [3 points]"""
        matches = []
        for start in range(0, len(sequence) - len(self.expressions) + 1):
            end = start + len(self.expressions)
            subseq_pos = [pos for tok, pos in sequence[start:end]]
            if all(self.match_expr(exp, pos) for pos, exp in zip(subseq_pos, self.expressions)):
                matches.append(sequence[start:end])
        return matches


    # The function below implements the same logic as match_seq above, but is written in a more verbose way
    #
    # def match_seq(self, sequence):
    #     """This method returns a list of matches in the given sequence
    #     (a sequence here is a list of (word,pos)-pairs -- see following example).
    #     A match is a list of (word, pos)-pairs, where the tags in the sequence match
    #     all expressions provided by PosExpr for all possible positions.
    #     For example: given p=PosPattern.from_string("X Y"),
    #     p.match_seq([(a,X),(b,Y),(c,Z),(d,X),(e,Y))]) should return the following list of lists:
    #     [[(a,X),(b,Y)],[(d,X),(e,Y)]].  [3 points]"""
    #     matches = []
    #     for i in range(0, len(sequence) - len(self.expressions) + 1):
    #         # perform matching
    #         match = True
    #         for j, expression in enumerate(self.expressions):
    #             if not self.match_expr(expression, sequence[i+j][1]):
    #                 match = False
    #                 break
    #
    #         # record match
    #         if match: matches.append(sequence[i:i+len(self.expressions)])
    #
    #     return matches


    @staticmethod
    def find_str(sentences, expr):
        """Return a list of strings that match the given expression. E.g.
        `find(sentences, "JJ NN") should return the list
        [...,"prior year",...].  [2 points]"""
        list_to_return = []
        p = PosExpr.from_string(expr)
        for sent in sentences:
            sent_matches = p.match_seq(sent)
            for match in sent_matches:
                tokens = [tok for tok, pos in match]
                list_to_return.append(' '.join(tokens))
        return list_to_return


if __name__ == '__main__':
    p = PosExpr.from_string("X Y")
    seq = [('a','X'), ('b', 'Y'), ('c', 'Z'),('d', 'X'), ('e', 'Y')]
    matches = p.match_seq(seq)