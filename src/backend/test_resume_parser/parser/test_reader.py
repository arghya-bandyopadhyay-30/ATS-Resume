import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from docx import Document

from src.backend.resume_parser.parser.reader import extract_text_from_docx


def create_docx(path, paragraphs):
    doc = Document()
    for p in paragraphs:
        doc.add_paragraph(p)
    doc.save(path)


class TestDocxReader(unittest.TestCase):

    def test_extract_text_success(self):
        with TemporaryDirectory() as tmpdir:
            docx_path = Path(tmpdir) / "test.docx"
            paragraphs = ["Hello World", "  Second paragraph  "]
            create_docx(str(docx_path), paragraphs)

            result = extract_text_from_docx(str(docx_path))
            self.assertEqual(result, "Hello World\nSecond paragraph")

    def test_extract_text_invalid_docx(self):
        with TemporaryDirectory() as tmpdir:
            fake_path = Path(tmpdir) / "invalid.docx"
            fake_path.write_text("I'm not a docx")

            with self.assertRaises(ValueError) as ctx:
                extract_text_from_docx(str(fake_path))

            self.assertIn("not a valid .docx file", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
