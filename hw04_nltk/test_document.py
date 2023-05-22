import inspect
import os

from unittest import TestCase
from hw04_nltk.document import PDFDocument, TextDocument


class DocumentTest(TestCase):

  @staticmethod
  def _get_constructor_args(cls):
    return dict(inspect.signature(cls.__init__).parameters)

  def test_inheritance(self):
    self.assertTrue(issubclass(PDFDocument, TextDocument))

  def test_constructor(self):
    constructor_args = DocumentTest._get_constructor_args(PDFDocument)
    for arg in ["docid", "filepath", "author"]:
      self.assertIn(arg, constructor_args)
    filepath_dummy_pdf = os.path.join(os.path.dirname(__file__), "dummy.pdf")
    pdf = PDFDocument(docid=1, filepath=filepath_dummy_pdf, author=None)
    self.assertTrue(hasattr(pdf, "text"))
    self.assertTrue(
      pdf.text.startswith("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur imperdiet libero")
    )

  def test_author(self):
    from hw04_nltk.document import Author
    author_constructor_args = DocumentTest._get_constructor_args(Author)
    for arg in ["firstname", "lastname", "age"]:
      self.assertIn(arg, author_constructor_args)
    self.assertIn("author", DocumentTest._get_constructor_args(PDFDocument))
