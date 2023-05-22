from unittest import TestCase
from hw03_docs.document import TextDocument, normalized_tokens


class TextDocumentTest(TestCase):
    def setUp(self):
        self.text_id1 = ("the fat cat sat on a mat", "doc1")
        self.text_id2 = ("a rose is a rose", "doc2")
        self.text_id3 = ("a cat is a cat", "doc3")
        self.text = "Dr. Strangelove is the U.S. President's advisor."

    def testTokenizer(self):
        tokens = normalized_tokens(self.text)
        expected_tokens = ['dr.', 'strangelove', 'is', 'the', 'u.s.', 'president', "'s", 'advisor', '.']
        self.assertEqual(tokens, expected_tokens)

    def testConstructor(self):
        doc1 = TextDocument(self.text_id1[0], self.text_id1[1])
        expected_dict1 = {"the": 1, "fat": 1, "cat": 1, "sat": 1, "on": 1, "a": 1, "mat": 1}
        self.assertEqual(doc1.word_to_count, expected_dict1)
        doc2 = TextDocument(self.text_id2[0], self.text_id2[1])
        expected_dict2 = {"a": 2, "rose": 2, "is": 1}
        self.assertEqual(doc2.word_to_count, expected_dict2)

    def testFromFileMethod(self):
        doc1 = TextDocument.from_file("./hw03_docs/example_document1.txt")
        token_set = set(doc1.word_to_count.keys())
        expected_token_set = {'dr.', 'strangelove', 'is', 'the', 'u.s.', 'president',
                              "'s", 'advisor', '.'}
        # we also allow whitespace tokenization
        expected_token_set_whitespace = {'dr.', 'strangelove', 'is', 'the', 'u.s.', "president's", 'advisor.'}
        self.assertTrue(token_set == expected_token_set or token_set == expected_token_set_whitespace)

        doc2 = TextDocument.from_file("./hw03_docs/example_document2.txt")
        self.assertEqual(doc2.word_to_count["die"], 2)
        self.assertTrue("länder" in doc2.word_to_count)

    def testToString(self):
        doc1 = TextDocument(self.text_id1[0], self.text_id1[1])
        self.assertEqual(str(doc1), "the fat cat sat on a mat")

        doc2 = TextDocument(self.text_id2[0], self.text_id2[1])
        self.assertEqual(str(doc2), "a rose is a rose")

        doc3 = TextDocument(self.text)
        self.assertEqual(str(doc3), "Dr. Strangelove is the...")

    def testWordOverlap(self):
        doc_1 = TextDocument(self.text_id1[0], self.text_id1[1])
        doc_2 = TextDocument(self.text_id2[0], self.text_id2[1])
        doc_3 = TextDocument(self.text_id3[0], self.text_id3[1])
        self.assertEqual(doc_1.word_overlap(doc_2), 1)
        self.assertEqual(doc_2.word_overlap(doc_3), 2)
        self.assertEqual(doc_1.word_overlap(doc_3), 2)
