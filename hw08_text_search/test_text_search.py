import doctest

from unittest import TestCase
from hw08_text_search.text_vectors import TextDocument, DocumentCollection, dot, normalized_tokens, SearchEngine


class DoctestTest(TestCase):
    # Exercise 2
    def test_doctest(self):
        finder = doctest.DocTestFinder(verbose=False, recurse=False)
        runner = doctest.DocTestRunner(verbose=False, optionflags=0)
        number_of_functions_tested = 0
        functions_to_test = [dot, normalized_tokens]
        for fn in functions_to_test:
            for test in finder.find(fn, "NoName", globs=globals()):
                test_result = runner.run(test, compileflags=None)
                self.assertGreater(test_result.attempted, 0)
                self.assertEqual(test_result.failed, 0)
                number_of_functions_tested += 1
        self.assertEqual(number_of_functions_tested, len(functions_to_test))


class DocumentCollectionTest(TestCase):

    def setUp(self):
        test_doc_list = [TextDocument(text_and_id[0], text_and_id[1]) for text_and_id in
                         [("the cat sat on a mat", "doc1"),
                          ("a rose is a rose", "doc2")]]
        self.small_collection = DocumentCollection.from_document_list(test_doc_list)

    # Exercose 3.1
    def test_cosine(self):
        # Document that only contains words that never occurred in the document collection.
        oov_query_doc = TextDocument(text="unknownwords", id=None)
        inv_query_doc = TextDocument(text="rose", id=None)
        # Some document from collection.
        collection_doc = self.small_collection.docid_to_doc["doc1"]
        # Similarity should be zero (instead of undefined).
        self.assertEqual(self.small_collection.cosine_similarity(oov_query_doc, collection_doc), 0.)
        # Test search with in-vocabulary query terms
        collection_doc_2 = self.small_collection.docid_to_doc["doc2"]
        self.assertEqual(round(self.small_collection.cosine_similarity(inv_query_doc, collection_doc_2), 3), 0.894)


class TextDocumentTest(TestCase):
    def setUp(self):
        test_text1 = "we are be-\nginning to see some dis-\nturbing behavior in cer-\ntain animals in this\narea."
        self.doc1 = TextDocument(test_text1, 1)
    
    # Exercise 3.2
    def test_preprocessing(self):
        self.assertEqual(self.doc1.text, "we are beginning to see some disturbing behavior in certain animals in this area.")


class SearchEngineTest(TestCase):
    def setUp(self):
        doc_a = TextDocument("the cat sat on a mat", "doc1")
        doc_b = TextDocument("a rose is a \nvery beautiful rose", "doc2")
        self.small_collection = DocumentCollection.from_document_list([doc_a, doc_b])

    # Exercise 3.3
    def test_docs_with_some_tokens(self):
        large_collection = DocumentCollection.from_dir("data/enron/enron1/ham", ".txt")
        searcher = SearchEngine(large_collection)
        results = searcher.ranked_documents("test goal")
        self.assertEqual(len(results), 32)

    # Exercise 3.4 
    def test_display_entire(self):
        """ Change the code such that only one text snippet is displayed, if it contains the entire search string. """
        searcher = SearchEngine(self.small_collection)
        self.assertEqual(
            [
                snippet for doc, sim in searcher.ranked_documents("sat on") for snippet in searcher.snippets("sat on", doc, window=5)
            ], ["... cat [sat on] a ma..."]
        )
        self.assertEqual(
            [
                snippet for doc, sim in searcher.ranked_documents("cat on") for snippet in searcher.snippets("cat on", doc, window=5)
            ], ["...[cat] sat ...", "... sat [on] a ma..."]
        )
        
