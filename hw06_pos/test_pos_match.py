from os.path import join
from os.path import dirname
from unittest import TestCase

# from hw06_pos.pos_match import Sentences, PosExpr
from pos_match_solution import Sentences, PosExpr


report = join(dirname(__file__), "hydrogenics_report.txt")


class SentenceTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = report

    def test_01_from_file(self):
        s = Sentences.from_file(self.path)
        tokens = [t for sent in s for t in sent]
        self.assertIn(('Selling', 'VBG'), tokens)
        self.assertIn(('Toronto', 'NNP'), tokens)


class PosExprTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sentences = Sentences.from_file(report)

    def test_02_from_string(self):
        m = PosExpr.from_string("NN VB NN")
        self.assertIn("NN", m.expressions)
        self.assertIn("VB", m.expressions)

    def test_03_match_expr(self):
        self.assertTrue(PosExpr.match_expr("*", "NN"))
        self.assertTrue(PosExpr.match_expr("*", "VB"))
        self.assertTrue(PosExpr.match_expr("NN", "NN"))
        self.assertTrue(PosExpr.match_expr("NN*", "NNPS"))
        self.assertFalse(PosExpr.match_expr("NN", "VB"))
        self.assertFalse(PosExpr.match_expr("NN*", "VBS"))

    def test_04_match_seq(self):
        def all_matches(expr):
            return [m for s in self.sentences for m in PosExpr.from_string(expr).match_seq(s)]
        print("1 sentence",self.sentences)
        self.assertIn([("Toronto", "NNP")], all_matches("NNP"))
        print("2 sentence",self.sentences)
        self.assertIn([("prior", "JJ"), ("year", "NN")], all_matches("JJ NN"))
        self.assertIn([("venture", "NN"), ("in", "IN"), ("Toronto", "NNP")], all_matches("NN IN NN*"))

    def test_05_find_str(self):
        self.assertIn("prior year", PosExpr.find_str(self.sentences, "JJ NN"))
        self.assertIn("$ 13.7 million", PosExpr.find_str(self.sentences, "$ CD CD"))
