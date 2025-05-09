import unittest
from unittest.mock import patch, MagicMock
from resume_parser.parser.reader import extract_text_from_docx

class TestExtractTextFromDocx(unittest.TestCase):
    @patch('resume_parser.parser.reader.Document')
    def test_extract_text_success(self, mock_document):
        mock_doc = MagicMock()
        mock_doc.paragraphs = [
            MagicMock(text='Hello'),
            MagicMock(text=''),
            MagicMock(text='  '),
            MagicMock(text='World')
        ]
        mock_document.return_value = mock_doc
        result = extract_text_from_docx('fake.docx')
        self.assertEqual(result, 'Hello\nWorld')

    @patch('resume_parser.parser.reader.Document', side_effect=Exception('Some error'))
    def test_extract_text_generic_error(self, mock_document):
        with self.assertRaises(ValueError) as cm:
            extract_text_from_docx('fake.docx')
        self.assertIn('An error occurred while reading the .docx file', str(cm.exception))

    @patch('resume_parser.parser.reader.Document', side_effect=ImportError)
    def test_extract_text_package_not_found(self, mock_document):
        from docx.opc.exceptions import PackageNotFoundError
        with patch('resume_parser.parser.reader.Document', side_effect=PackageNotFoundError):
            with self.assertRaises(ValueError) as cm:
                extract_text_from_docx('fake.docx')
            self.assertIn('not a valid .docx file or is corrupted', str(cm.exception))

if __name__ == '__main__':
    unittest.main()
