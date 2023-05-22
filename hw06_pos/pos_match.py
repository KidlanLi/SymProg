import nltk


class Sentences:
    def __init__(self, sentences):
        """Construct an instance of the class Sentence from a list of
        pos-tagged sentences ([[(word,tag),...],...])"""
        self.sentences = sentences

    def __iter__(self):
        return iter(self.sentences)

    def __getitem__(self, i):
        return self.sentences[i]

    @classmethod
    def from_file(cls, path):
        """Create an instance of the class Sentences from a
        path. Reads the file and pos-tags the sentences in the
        file. [2 point]"""
        with open(path) as f:
            document = f.read()
        sentences = nltk.sent_tokenize(document)
        return cls(nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences)


class PosExpr:
    def __init__(self, expressions):
        """Construct an instance of the class PosExpr from a list of
        expressions."""
        self.expressions = expressions

    @classmethod
    def from_string(cls, expr):
        """Create an instance of the class PosExpr from the given
        string.  [1 points]"""
        print(expr.split(' '))
        return cls(expr.split(' '))

    @staticmethod
    def match_expr(expr, pos):
        """This method returns True if expr matches pos. An expression
        'XX' matches if pos equals 'XX', the expression '*' matches
        any pos and an expression XX* matches if pos starts with 'XX'
        or is equal to 'XX'.  [2 points]"""
        if expr[:1] == pos[:1] or expr == "*":
            return True
        else:
            return False

    def match_seq(self, sequence):
        """This method returns a list of matches in the given sequence
        (a sequence here is a list of (word,pos)-pairs -- see following example).
        A match is a list of (word, pos)-pairs, where the tags in the sequence match
        all expressions provided by PosExpr for all possible positions.
        For example: given p=PosPattern.from_string("X Y"),
        p.match_seq([(a,X),(b,Y),(c,Z),(d,X),(e,Y))]) should return the following list of lists:
        [[(a,X),(b,Y)],[(d,X),(e,Y)]].  [3 points]"""
        matches = []
        n = len(self.expressions)
        for i in range(0, len(sequence) - n + 1):
            signal = True
            if not PosExpr.match_expr(self.expressions[0], sequence[i][1]):
                continue
            for j in range(0, n):
                if not PosExpr.match_expr(self.expressions[j], sequence[i + j][1]):
                    signal = False
                    break
            if signal:
                matches.append(sequence[i:i + n])
        return matches

    @staticmethod
    def find_str(sentences, expr):
        """Return a list of strings that match the given expression. E.g.
        `find_str(sentences, "JJ NN") should return the list
        [...,"prior year",...].  [2 points]"""
        matches = [m for s in sentences for m in PosExpr.from_string(expr).match_seq(s)]
        return [" ".join([e[0] for e in a]) for a in matches]
