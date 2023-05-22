import argparse
import sys

from hw08_text_search.text_vectors import DocumentCollection, SearchEngine

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', required=True)
    opts = parser.parse_args(argv)
    doc_collection = DocumentCollection.from_dir(opts.dir, ".txt")
    searcher = SearchEngine(doc_collection)
    while True:
        query_str = input("Query: ").strip()
        if not query_str:
            break
        top_docs = searcher.ranked_documents(query_str)
        print("Results: %d" % len(top_docs))
        for doc, sim in top_docs[:3]:
            print("%.4f %s" % (sim, doc.id))
            for snippet in searcher.snippets(query_str, doc):
                print("  %s" % snippet)
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
